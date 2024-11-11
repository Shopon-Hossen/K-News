from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import NewsArticle, NewsArticleLike
from .forms import CommentForm
from django.db.models import Q

def home_view(request: HttpRequest):
    search_query = request.GET.get('q')
    category_query = request.GET.get('category')

    if category_query:
        news_list = NewsArticle.objects.filter(category__name=category_query).order_by('-published_date')[:50]
    elif search_query:
        news_list = NewsArticle.objects.filter(Q(title__icontains=search_query) | Q(tags__name__icontains=search_query)).distinct().order_by('-published_date')[:100]
    else:
        news_list = NewsArticle.objects.order_by('-published_date')[:50]

    return render(request, 'news/index.html', {"news_list": news_list})

def detail_view(request: HttpRequest, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    comments = article.comments.all().order_by('-created_at')[:50]
    has_liked = article.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    related_articles = NewsArticle.objects.filter(
        tags__in=article.tags.all()
    ).exclude(pk=pk).distinct().order_by('-published_date')[:5]
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'like' in request.POST and request.htmx:
            if request.user.is_authenticated and not NewsArticleLike.objects.filter(article=article, user=request.user).exists():
                NewsArticleLike.objects.create(article=article, user=request.user)

            return render(request, 'partial/article_like.html', {'has_liked': True, 'article': article})

        if 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.article = article
                comment.user = request.user
                comment.save()

                return redirect('news_detail', pk=article.pk)

    return render(request, 'news/detail.html', {
        'article': article,
        'comments': comments,
        'form': comment_form,
        'has_liked': has_liked,
        'related_articles': related_articles
    })