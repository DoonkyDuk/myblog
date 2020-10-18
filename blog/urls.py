from django.urls import path, include

from . import views

app_name='blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('article/new/', views.create_article, name='create_article'),
    path('profile/', views.profile, name='profile'),
    path('article/<int:article_id>/', views.article, name='article'),
    path('article/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('authorization', views.authorization, name='authorization'),
    # path('create', views.create, name='create'),
    path('register', views.register, name ='register'),
    path('article/<int:article_id>/like', views.like, name='like'),
    path('article/<int:article_id>/dislike', views.dislike, name='dislike')
]
