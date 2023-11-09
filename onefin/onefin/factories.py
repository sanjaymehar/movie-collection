import factory
from django.contrib.auth import get_user_model
from factory import post_generation
from rest_framework_simplejwt.tokens import RefreshToken
from factory.django import DjangoModelFactory
from task.models import Movie, Collection


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class AccessTokenFactory(factory.Factory):
    class Meta:
        model = str

    @classmethod
    def create(cls, **kwargs):
        user = UserFactory()
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')
    genres = factory.Faker('word')
    uuid = factory.Faker('uuid4')


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')
    uuid = factory.Faker('uuid4')
    user = factory.SubFactory(UserFactory)

    @post_generation
    def movies(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:

            for movie in extracted:
                self.movies.add(movie)
        else:

            movie1 = MovieFactory()
            movie2 = MovieFactory()
            self.movies.add(movie1, movie2)