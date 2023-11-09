from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from rest_framework.response import Response

from onefin.factories import AccessTokenFactory, CollectionFactory, MovieFactory
from onefin.factories import UserFactory
from task.middleware import RequestCounterMiddleware
from task.models import Collection

# Test For Register User
class RegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration_success(self):

        user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        response = self.client.post('/register/', user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('access_token', response.data)

    def test_registration_failure_invalid_data(self):
        response = self.client.post('/register/', {'username': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('password', response.data)

    def test_registration_failure_existing_user(self):

        existing_user = UserFactory()

        response = self.client.post('/register/', {
            'username': existing_user.username,
            'password': 'testpassword',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('username', response.data)


# Test For Login User
class LoginViewTestCase(TestCase):
    @patch('task.account_view.TokenObtainPairView.post')
    def test_login_view(self, mock_super_post):
        mock_super_post.return_value = Response({'access': 'mocked_access_token'}, status=status.HTTP_200_OK)

        client = APIClient()
        data = {'username': 'test_user', 'password': 'test_password'}
        response = client.post('/login/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('access_token', response.data)
        self.assertEqual(response.data['access_token'], 'mocked_access_token')

        mock_super_post.assert_called_once()


# Test To Fetch Data from credy API
class MoviesAPITestCase(TestCase):

    @patch('task.views.get_data_from_credy')
    def test_get_movies(self, mock_get_data_from_credy):
        mock_token = AccessTokenFactory()
        mock_data = {
                "count": 45466,
                "next": "https://demo.credy.in/api/v1/maya/movies/?page=2",
                "previous": None,
                "results": [
                    {
                        "title": "Queerama",
                        "description": "50 years after decriminalisation of homosexuality in the UK, director Daisy Asquith mines the jewels of the BFI archive to take us into the relationships, desires, fears and expressions of gay men and women in the 20th century.",
                        "genres": "",
                        "uuid": "57baf4f4-c9ef-4197-9e4f-acf04eae5b4d"
                    }
                ]
                }
        mock_get_data_from_credy.return_value = mock_data

        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {mock_token}')

        response = client.get('/movies/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("https://demo.credy.in/api/v1/maya/movies/?page=2", response.data['next'])
        assert isinstance(response.data['results'], list)


# Test For GET/List & POST Collection
class CollectionViewTestCase(TestCase):
    def setUp(self):
        mock_token = AccessTokenFactory()
        self.client = APIClient()
        self.user = UserFactory()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {mock_token}')

    def test_create_collection(self):
        movie1_data = MovieFactory.build()
        movie2_data = MovieFactory.build()

        data = {
            'title': 'My Collection',
            'description': 'Description of my collection',
            'movies': [
                {
                    'title': movie1_data.title,
                    'description': movie1_data.description,
                    'genres': movie1_data.genres,
                    'uuid': movie1_data.uuid,
                },
                {
                    'title': movie2_data.title,
                    'description': movie2_data.description,
                    'genres': movie2_data.genres,
                    'uuid': movie2_data.uuid,
                },
            ],
        }

        response = self.client.post('/collection/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_collections(self):
        response = self.client.get('/collection/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('collections', response.data['data'])
        self.assertIsInstance(response.data['data']['collections'], list)
        self.assertEqual(len(response.data['data']['collections']), 0)


# Test For GET PUT & DELETE Collection
class CollectionDetailTestCase(TestCase):
    def setUp(self):
        mock_token = AccessTokenFactory()
        self.client = APIClient()
        self.user = UserFactory()
        self.collection = CollectionFactory(user=self.user)
        self.movie = MovieFactory()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {mock_token}')

    def test_get_collection_detail(self):
        response = self.client.get(f'/collection/{self.collection.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_collection(self):
        response = self.client.delete(f'/collection/{self.collection.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Collection.objects.filter(uuid=self.collection.uuid).exists(), False)

    def test_update_collection(self):
        updated_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'movies': [
                {
                    'title': 'Updated Movie 1',
                    'description': 'Updated Description 1',
                    'genres': 'Action',
                    'uuid': 'cc51020f-1bd6-42ad-84e7-e5c0396435a9'
                },
            ]
        }
        response = self.client.put(f'/collection/{self.collection.uuid}/', updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Test For RequestCounterMiddleware
class RequestCounterMiddlewareViewTestCase(TestCase):
    def setUp(self):
        mock_token = AccessTokenFactory()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {mock_token}')

    @patch('task.middleware.RequestCounterMiddleware._request_count', 42)
    def test_get_request_count(self):
        response = self.client.get('/request-count/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('requests', response.data)
        self.assertEqual(response.data['requests'], 43)

    @patch('task.middleware.RequestCounterMiddleware._request_count', 42)
    def test_reset_request_count(self):
        response = self.client.post('/request-count/reset/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Request count reset successfully')

        self.assertEqual(RequestCounterMiddleware._request_count, 0)