from django.shortcuts import render, redirect
from django.http import HttpRequest
from news.models import NewsArticle
from .models import Review
from .forms import ReviewForm
from django.db.models import Count
import datetime
from django.utils import timezone

def home_view(request: HttpRequest):
    popular_articles = (
        NewsArticle.objects
        .annotate(like_count=Count('likes'))
        .filter(like_count__gt=0)
        .filter(published_date__gte=timezone.now() - datetime.timedelta(weeks=7))
    )[:10]
    
    latest_articles = NewsArticle.objects.all().order_by("-published_date")[:10]
    latest_reviews = Review.objects.all().order_by("-published_date")[:15]

    form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save() 
            return redirect('home') 

    return render(request, "home/index.html", {
        "latest_articles": latest_articles,
        "latest_reviews": latest_reviews,
        "popular_articles": popular_articles,
        "form": form
    })