from django.shortcuts import render
from django.views import generic

from .models import BlogPost, Comment, Blogger

# Create your views here.

def home(request):
    num_blog_posts = BlogPost.objects.all().count()
    num_comments = Comment.objects.all().count()

    context = {
        'num_blog_posts': num_blog_posts,
        'num_comments': num_comments,
    }

    return render(request, 'home.html', context=context)

class BlogListView(generic.ListView):
    model = BlogPost


class BloggerListView(generic.ListView):
    model = Blogger

class BloggerDetailView(generic.DetailView):
    model = Blogger