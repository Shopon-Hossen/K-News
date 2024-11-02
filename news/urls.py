from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home_view, name='news_home'),
    path('<int:pk>/', views.detail_view, name='news_detail'),
]