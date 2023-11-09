from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Movie, Collection


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)

    class Meta:
        model = Collection
        exclude = ["uuid", "user"]


class MovieDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        exclude = ["id"]


class CollectionDetailSerializer(serializers.ModelSerializer):
    movies = MovieDetailSerializer(many=True, required=False)

    class Meta:
        model = Collection
        exclude = ["uuid", "user", "id"]


class CollectionUpdateSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)
    title = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Collection
        exclude = ["uuid", "user", "id"]

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        if 'movies' in validated_data:
            updated_movies_data = validated_data.pop('movies')

            instance.movies.clear()

            for movie_data in updated_movies_data:
                movie, created = Movie.objects.get_or_create(**movie_data)
                instance.movies.add(movie)

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
