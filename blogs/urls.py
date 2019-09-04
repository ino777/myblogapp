"""myblogapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path


from . import views


app_name = 'blogs'


urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('about/<uuid:pk>', views.PostDetailView.as_view(), name='detail'),
    # path('about/<uuid:pk>/eval', views.post_eval_view, name='post_eval'),
    path('post/', views.PostCreateView.as_view(), name='post'),
    path('edit/<uuid:pk>', views.PostUpdateView.as_view(), name='edit'),
    path('delete/<uuid:pk>', views.PostDeleteView.as_view(), name='delete'),
    path('result/', views.SeaechResultPostView.as_view(), name='result'),
    # path('result/filter', views.SearchFilterView.as_view(), name='search_filter'),
    path('user/<uuid:pk>/home', views.UserPageView.as_view(), name='user_page'),
    path('user/<uuid:pk>/posts', views.UserPostListView.as_view(), name='user_posts'),
    path('user/<uuid:pk>/profile', views.UserProfileView.as_view(), name='profile'),
]
