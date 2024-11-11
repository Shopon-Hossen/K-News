from django.contrib import admin
from .models import NewsArticle, NewsCategory

admin.site.register(NewsArticle)
admin.site.register(NewsCategory)