from django.urls import path
from . import views


urlpatterns = [    
    path('', views.movie_list),
    path('bestFive/', views.bestFive),
    path('genre/', views.get_genre),
    path('genre/<int:genre_pk>/like/', views.like_genre),
    path('<int:movie_pk>/', views.movie_detail_review_list_create),
    path('<int:movie_pk>/like/', views.like),
    path('<int:movie_pk>/<int:review_pk>/', views.review_delete_update),
]