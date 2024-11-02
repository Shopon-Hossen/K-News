from django.contrib import admin
from .models import NewsArticle, Comment

admin.site.register(NewsArticle)
admin.site.register(Comment)