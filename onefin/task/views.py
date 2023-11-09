from collections import OrderedDict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Collection, Movie
from .serializers import (
    CollectionSerializer,
    MovieSerializer,
    CollectionDetailSerializer,
    CollectionUpdateSerializer,
    )
from .third_party_api import get_data_from_credy

from rest_framework.permissions import IsAuthenticated


class Movies(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_data_from_credy()
        return Response(data)


class CollectionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CollectionSerializer

    def get(self, request):
        user_collections = Collection.objects.filter(user=request.user)
        serializer = CollectionSerializer(user_collections, many=True)

        movie_set = set()
        flat_movie_list = []

        for movie_data in serializer.data:
            unique_movies = []
            for movie in movie_data['movies']:
                if movie['uuid'] not in movie_set:
                    unique_movie = {key: value for key, value in movie.items() if key != 'id'}
                    unique_movies.append(unique_movie)
                    movie_set.add(movie['uuid'])

            flat_movie_list.extend(unique_movies)


        all_genres = []
        for collection in user_collections:
            all_genres.extend(collection.movies.values_list('genres', flat=True))


        genre_counts = {}
        for genre in all_genres:
            if genre in genre_counts:
                genre_counts[genre] += 1
            else:
                genre_counts[genre] = 1

        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)

        top_3_genres = []
        for genre in sorted_genres[:3]:
            top_3_genres.append(genre[0])

        response_data = {
            "is_success": True,
            "data": {
                "collections": flat_movie_list,
                "favourite_genres": ", ".join(top_3_genres),
            }
        }
        return Response(response_data)

    def post(self, request):
        data = request.data
        collection_serializer = CollectionSerializer(data=data)

        if not collection_serializer.is_valid():
            return Response(collection_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        movies_data = data.get('movies', [])

        collection_data = {
            'title': data.get('title'),
            'description': data.get('description'),
            'user': request.user
        }

        movies = []
        for movie_data in movies_data:

            existing_movie = Movie.objects.filter(uuid=movie_data.get('uuid')).first()

            if existing_movie:
                movies.append(existing_movie)
            else:
                movie_serializer = MovieSerializer(data=movie_data)
                if not movie_serializer.is_valid():
                    return Response(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                movie = movie_serializer.save()
                movies.append(movie)

        collection = Collection.objects.create(**collection_data)
        collection.movies.set(movies)

        return Response({'collection_uuid': collection.uuid}, status=status.HTTP_201_CREATED)


class CollectionEditView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, collection_uuid):
        try:
            collection = Collection.objects.get(uuid=collection_uuid)
        except Collection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionDetailSerializer(collection)
        return Response(serializer.data)

    def delete(self, request, collection_uuid):
        try:
            collection = Collection.objects.get(uuid=collection_uuid)
        except Collection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

        collection.delete()
        return Response({'message': 'Collection deleted'}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, collection_uuid):
        try:
            collection = Collection.objects.get(uuid=collection_uuid)
        except Collection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionUpdateSerializer(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





