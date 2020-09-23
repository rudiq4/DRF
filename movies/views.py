from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer


class MovieListView(APIView):
    '''Виводить список фільмів'''

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    '''Виводить повний опис'''

    def get(self, request, pk):
        movie = Movie.objects.filter(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie, many=True)
        return Response(serializer.data)


