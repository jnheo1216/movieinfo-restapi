import re
from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls.conf import path
from rest_framework import serializers, status
from rest_framework.response import Response
from .models import Movie, Review, Genre
from .serializers import (
                            MovieListSerializer,
                            MovieSerializer, 
                            ReviewListSerializer, 
                            ReviewSerializer,
                            GenreListSerializer
                            )
from rest_framework.decorators import api_view

from django.contrib.auth import get_user_model


@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializers = MovieListSerializer(movies, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def bestFive(request):
    movies = Movie.objects.all().order_by('-vote_average')[:5]
    # print(movies)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def movie_detail_review_list_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        serializer_movie = MovieSerializer(movie)
        if movie.review_set.all():
            review = get_list_or_404(Review, movie=movie)
            serializer = ReviewListSerializer(review, many=True)
            serializer = serializer.data
        else:
            serializer = []
        is_liked = movie.like_user.filter(pk=request.user.pk).exists()
        data = {
            'movie': serializer_movie.data,
            'review_list': serializer,
            'is_liked': is_liked
        }
        return Response(data)
        
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ## 포스트맨으로 확인용 : 유저를 강제적으로 넣어서
            # User = get_user_model()
            # user = get_object_or_404(User,pk=11)
            # serializer.save(user=user, movie=movie)
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def review_delete_update(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'PUT':
        # if review.user == request.user:
        serializer = ReviewListSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    elif request.method == 'DELETE':
        # if review.user == request.user:
        review.delete()
        data = {
            'delete': f'리뷰 {review_pk}번이 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


## 영화 좋아요기능
@api_view(['GET'])
def like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # 포스트맨으로 확인용 : 유저를 강제적으로 넣어서
    # User = get_user_model()
    # user = get_object_or_404(User,pk=11)
    # if not movie.like_user.filter(pk=11).exists():
    if not movie.like_user.filter(pk=request.user.pk).exists():
        # movie.like_user.add(user)
        movie.like_user.add(request.user)
        return Response({'message': f'{ movie.title } 영화 좋아요 누르셨습니다'}, status = status.HTTP_200_OK)
    else:
        # movie.like_user.remove(user)
        movie.like_user.remove(request.user)
        return Response({'message': f'{ movie.title } 영화 좋아요 취소했습니다'}, status = status.HTTP_200_OK)


## 영화 좋아요기능
@api_view(['GET'])
def like_genre(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    ## 포스트맨으로 확인용 : 유저를 강제적으로 넣어서
    # User = get_user_model()
    # user = get_object_or_404(User,pk=21)
    # if not genre.like_user.filter(pk=21).exists():
    if not genre.like_user.filter(pk=request.user.pk).exists():
        # genre.like_user.add(user)
        genre.like_user.add(request.user)
        return Response({'message': f'{ genre.name } 장르 좋아요 누르셨습니다'}, status = status.HTTP_200_OK)
    else:
        # genre.like_user.remove(user)
        genre.like_user.remove(request.user)
        return Response({'message': f'{ genre.name } 장르 좋아요 취소했습니다'}, status = status.HTTP_200_OK)


@api_view(['GET'])
def get_genre(request):    
    genres = Genre.objects.all()
    serializers = GenreListSerializer(genres, many=True)
    return Response(serializers.data)
