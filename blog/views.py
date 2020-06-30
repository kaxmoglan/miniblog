from django.shortcuts import render
from .models import BlogPost, Comment

# Create your views here.

def home(request):
    num_blog_posts = BlogPost.objects.all().count()
    num_comments = Comment.objects.all().count()

    context = {
        'num_blog_posts': num_blog_posts,
        'num_comments': num_comments,
    }

    return render(request, 'home.html', context=context)