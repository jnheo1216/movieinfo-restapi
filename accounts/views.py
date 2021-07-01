from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST  
)
from .serializers import UserSerializer
from rest_framework import status
from django.contrib.auth import get_user_model


@api_view(['POST'])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')

    if password != password_confirmation:
        return Response({ 'error': '비밀번호가 일치하지 않습니다' }, HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
    
        return Response(serializer.data, HTTP_201_CREATED)


@api_view(['GET'])
def profile(request, user_pk):    
    User = get_user_model()
    user = get_object_or_404(User,pk=user_pk)
    # 좋아요 누른 영화 : 좋아요 누른 글이나 유저도 이런식으로 보기 가능할 듯
    likeMovie = user.like_movie.all()
    likeGenre = user.like_genre.all()
    posts = user.post_set.all()
    comments = user.comment_set.all()
    reviews = user.review_set.all()
    data = {
        'user_id': user.username,
        'post': [],
        'comment': [],
        'review': [],
        'like_movies': [], 
        'like_genres': [],
        'like_genre_numbers': []
        }
    for movie in likeMovie:
        tmp = {'movie_pk': movie.movie_id, 'movie_title': movie.title}
        data['like_movies'].append(tmp)
    for genre in likeGenre:
        tmp = {'genre_pk': genre.pk, 'genre_name': genre.name}
        data['like_genres'].append(tmp)
    for genreNum in likeGenre:
        tmp = genreNum.pk
        data['like_genre_numbers'].append(tmp)
    for post in posts:
        tmp = {'post_pk': post.pk, 'post_title': post.title}
        data['post'].append(tmp)
    for comment in comments:
        tmp = {'comment_pk': comment.pk, 'comment_content': comment.content}
        data['comment'].append(tmp)
    for review in reviews:
        tmp = {'review_pk': review.pk, 'review_movie': review.movie.title, 'review_movie_pk': review.movie.pk}
        data['review'].append(tmp)
    return Response(data, status = status.HTTP_200_OK)


@api_view(['GET'])
def return_user_pk(request):
    user = request.user
    data = {
        'user_id': user.pk
    }
    return Response(data, status = status.HTTP_200_OK)


@api_view(['GET'])
def like_list(request):
    userpk = request.user  
    User = get_user_model()
    user = get_object_or_404(User,pk=userpk.pk)
    likeMovie = user.like_movie.all()
    likeGenre = user.like_genre.all()
    like_movie_list = []
    for movie in likeMovie:
        like_movie_list.append(movie.movie_id)
    like_genre_list = []
    for genre in likeGenre:
        like_genre_list.append(genre.id)
    data = {
        'like_movie_list': like_movie_list,
        'like_genre_list': like_genre_list
    }
    return Response(data, status = status.HTTP_200_OK)

# @api_view(['GET'])
# def followings(request, user_pk):
#     User = get_user_model()
#     # user = get_object_or_404(User, pk=11)
#     user = get_object_or_404(User, pk=user_pk)
#     data = {
#         'followings': user.followings.all()
#     }

#     return Response(data, status= status.HTTP_200_OK)


# @api_view(['GET'])
# def follow(request, person_pk):
#     User = get_user_model()
#     person = get_object_or_404(User, pk=person_pk)
#     # user = get_object_or_404(User, pk=1)
    
#     if person != request.user:
#         # if person.followers.filter(pk=11).exists():
#         if person.followers.filter(pk=request.user.pk).exists():
#             person.followers.remove(request.user)
#             return Response ({'message': f'{person_pk} 팔로우 해제'}, status = status.HTTP_200_OK)
#         else:
#             person.followers.add(request.user)
#             return Response ({'message': f'{person_pk} 팔로우'}, status = status.HTTP_200_OK)
        