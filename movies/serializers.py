from rest_framework import serializers
from .models import Movie


class MovieListSerializer(serializers.ModelSerializer):
    '''Список фільмів'''

    class Meta:
        model = Movie
        fields = ('title', 'tagline')


class MovieDetailSerializer(serializers.ModelSerializer):
    '''Повний опис'''
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)  # Щоб вивести імя категоріії а не її id
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True,
                                             many=True)  # many=True, because it's Many To Many field
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)
