"""The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('allblogs/', views.BlogListView.as_view(), name='blog-list'),
    path('allbloggers/', views.BloggerListView.as_view(), name='blogger-list'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),

    path('blogger/<int:pk>/update/', views.BloggerUpdate.as_view(), name='blogger-update'),
    path('blogpost/create/', views.BlogPostCreate.as_view(), name='post-create'),
    path('blogpost/<int:pk>/update/', views.BlogPostUpdate.as_view(), name='post-update'),
    path('blogpost/<int:pk>/delete/', views.BlogPostDelete.as_view(), name='post-delete'),

    path('blogpost/<int:pk>', views.blog_detail, name='blog-detail'),

    path('register/', views.register, name='register'),
    path('blogger/create/', views.blogger_sign_up, name='blogger-create'),
    path('blogger/delete/', views.delete_user, name='blogger-delete'),
]
