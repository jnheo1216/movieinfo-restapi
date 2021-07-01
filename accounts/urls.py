from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('returnuserpk/', views.return_user_pk),
    path('likelist/', views.like_list),
    path('profile/<int:user_pk>/', views.profile),
    # path('profile/<int:user_pk>/followings/', views.followings, name='followings'),
    # path('profile/<int:person_pk>/follow/', views.follow, name='follow'),
]
