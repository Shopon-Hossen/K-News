from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from news.models import NewsArticle, NewsCategory
from .models import Review
from .forms import ReviewForm
from django.db.models import Count
from django.utils import timezone


def get_trending_news():
    return NewsArticle.objects.filter(
        published_date__gte=timezone.now()-timezone.timedelta(days=7)
    ).annotate(likes_count=Count('likes')).filter(
        likes_count__gte=1
    ).order_by('-likes_count')


def home_view(request: HttpRequest):
    trending_list = get_trending_news()
    most_liked_list = NewsArticle.objects.filter(
        published_date__gte=timezone.now()-timezone.timedelta(days=7)
    ).annotate(likes_count=Count('likes')).order_by('-likes_count')[:5]

    latest_reviews = Review.objects.all().order_by("-published_date")[:15]
    category_list = NewsCategory.objects.all()

    form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save() 
            return redirect('home') 

    return render(request, "home/index.html", {
        "category_list": category_list,
        "trending_news": trending_list,
        "most_liked_news": most_liked_list,
        "latest_reviews": latest_reviews,
        "form": form
    })