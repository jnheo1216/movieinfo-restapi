
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Post, Comment
from .serializers import (
                            PostListSerializer,
                            PostSerializer,
                            CommentListSerializer,
                            CommentSerializer,
                        )

from django.contrib.auth import get_user_model


@api_view(['GET', 'POST'])
def post_list_create(request):
    if request.method == 'GET':
        posts = get_list_or_404(Post)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ## 포스트맨으로 확인용 : 유저를 강제적으로 넣어서
            # User = get_user_model()
            # user = get_object_or_404(User,pk=11)
            # serializer.save(user=user)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE', 'GET', 'POST'])
def post_delete_update_detail_comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'PUT':
        # if post.user == request.user:
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        # if post.user == request.user:
        post.delete()
        data = {
            'delete': f'{post_pk}번 게시글이 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'GET':
        User = get_user_model()
        user = get_object_or_404(User,pk=post.user.pk)
        # print(user.username)
        # print(type(user))
        serializer_post = PostSerializer(post)
        print(post.comment_set.all())
        if post.comment_set.all():
            comments = get_list_or_404(Comment, post=post)
            serializer_comments = CommentListSerializer(comments, many=True)
            serializer_comments = serializer_comments.data
        else:
            serializer_comments = []
        data = {
            'serializer_post': serializer_post.data,
            'serializer_comments': serializer_comments,
            'username': user.username
        }
        return Response(data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def comment_update_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        # if comment.user == request.user:
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        # if comment.user == request.user:
        comment.delete()
        data = {
            'delete': f'{comment_pk}번 댓글이 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)



## 커뮤니티글 좋아요기능
@api_view(['GET'])
def like_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # 포스트맨으로 확인용 : 유저를 강제적으로 넣어서
    # User = get_user_model()
    # user = get_object_or_404(User,pk=11)
    # if not post.like_user.filter(pk=11).exists():
    if not post.like_user.filter(pk=request.user.pk).exists():
        # post.like_user.add(user)
        post.like_user.add(request.user)
        return Response({'message': f'{ post.title } 글 좋아요 누르셨습니다'}, status = status.HTTP_200_OK)
    else:
        # post.like_user.remove(user)
        post.like_user.remove(request.user)
        return Response({'message': f'{ post.title } 글 좋아요 취소했습니다'}, status = status.HTTP_200_OK)


@api_view(['GET'])
def post_like_list(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    likeUser = post.like_user.all()
    like_list = []
    for like in likeUser:
        like_list.append(like.id)
    data = {
        'like_list': like_list
    }
    return Response(data, status=status.HTTP_200_OK)
