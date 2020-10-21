from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Article, User, Like
from .serializers import ArticleSerializer
from rest_framework import viewsets
from django.utils import timezone
from django.urls import reverse
from .forms import ArticleForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def index(request):
    latest_articles = Article.objects.all()
    context = {'latest_articles': latest_articles}
    return render(request, 'blog/index.html', context)

def profile(request, user_id):
    user = User.objects.get(id = user_id)
    user_articles = Article.objects.filter(author = user)
    return render(request, 'blog/profile.html', {'user_id': user_id, 'user_articles':user_articles, 'user':user})

def article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    show_edit = article.author == request.user

    try:
        like = Like.objects.get(article = article, user = request.user)
        show_liked = like.like_or_dislike
    except Like.DoesNotExist:
        show_liked = False

    return render (request, 'blog/article.html', {'article':article, 'show_edit':show_edit, 'show_liked': show_liked})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:profile', args={request.user}))
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.author = request.user
            new_article.publish_date = timezone.now()
            new_article.save()
            return HttpResponseRedirect(reverse('blog:article', args={new_article.id}))
    else:
        form = ArticleForm()
    return render(request, 'blog/article_edit.html', {'form': form})

def edit_article(request, article_id):
    article = get_object_or_404(Article, pk = article_id)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author=request.user
            article.publish_date = timezone.now()
            article.save()
            return HttpResponseRedirect(reverse('blog:article', args={article.id}))
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_edit.html', {'form': form})

def like(request, article_id):
     article = get_object_or_404(Article, pk=article_id)
     try:
         rate = Like.objects.get(user=request.user, article = article)
         if rate.like_or_dislike == 'like':
             rate.delete()
             article.likes -=1
             article.save()
         elif rate.like_or_dislike == 'dislike':
             rate.like_or_dislike = 'like'
             rate.save()
             article.likes +=1
             article.dislikes -=1
             article.save()
     except Like.DoesNotExist:
        new_like = Like(user = request.user, article = article, like_or_dislike = 'like')
        new_like.save()
        article.likes+=1
        article.save()
     return HttpResponseRedirect(reverse('blog:article', args={article.id}))

def dislike(request, article_id):
    article = get_object_or_404(Article, pk = article_id)
    try:
        rate = Like.objects.get(user=request.user, article = article)
        if rate.like_or_dislike == 'dislike':
            rate.delete()
            article.dislikes -=1
            article.save()
        elif rate.like_or_dislike == 'like':
            rate.like_or_dislike = 'dislike'
            rate.save()
            article.likes -=1
            article.dislikes +=1
            article.save()
    except Like.DoesNotExist:
         new_dislike = Like(user = request.user, article = article, like_or_dislike='dislike')
         new_dislike.save()
         article.dislikes +=1
         article.save()
    return HttpResponseRedirect(reverse('blog:article', args={article.id}))

def home(request):
    user_articles = Article.objects.filter(author = request.user)
    return render(request, 'blog/home.html', {'user': request.user, 'user_articles':user_articles})
