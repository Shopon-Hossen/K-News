from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import NewsArticle, NewsArticleLike
from .forms import CommentForm
from django.db.models import Q
import datetime
from django.utils import timezone
from django.db.models import Count


def home_view(request: HttpRequest):
    query = request.GET.get('q')
    if query:
        news_list = NewsArticle.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct().order_by('-published_date')[:100]
    else:
        news_list = NewsArticle.objects.order_by('-published_date')[:50]

    return render(request, 'news/index.html', {"news_list": news_list, "query": query})

def detail_view(request: HttpRequest, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    comments = article.comments.all().order_by('-created_at')[:100]
    has_liked = article.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
    related_articles = (
        NewsArticle.objects
        .filter(tags__in=article.tags.all())
        .exclude(pk=article.pk)  # Exclude the current article
        .filter(published_date__gte=thirty_days_ago)  # Filter for articles published in the last 30 days
        .distinct()  # Remove duplicate articles
        .order_by('-published_date')[:5]  # Order by date and limit to 5 articles
    )    
    form = CommentForm()

    if request.method == 'POST':
        if 'like' in request.POST and request.user.is_authenticated:
            if not NewsArticleLike.objects.filter(article=article, user=request.user).exists():
                NewsArticleLike.objects.create(article=article, user=request.user)

            return redirect('news_detail', pk=article.pk)

        if 'comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.user = request.user
                comment.save()

                return redirect('news_detail', pk=article.pk)

    print(related_articles)
    return render(request, 'news/detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
        'has_liked': has_liked,
        'related_articles': related_articles
    })
