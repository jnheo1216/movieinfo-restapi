from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list_create),
    path('<int:post_pk>/likelist/', views.post_like_list),
    path('<int:post_pk>/', views.post_delete_update_detail_comment_create),
    path('<int:post_pk>/like/', views.like_post),
    path('<int:post_pk>/<comment_pk>/', views.comment_update_delete),
]

