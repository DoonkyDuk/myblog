from django import forms

from .models import Article
from django.conf import settings

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'text',)
