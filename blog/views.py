from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


from .models import BlogPost, Comment, Blogger
from .forms import CommentForm, BloggerSignUpForm

# Create your views here.

def home(request):
    num_blog_posts = BlogPost.objects.all().count()
    num_comments = Comment.objects.all().count()
    num_bloggers = Blogger.objects.all().count()

    context = {
        'num_blog_posts': num_blog_posts,
        'num_comments': num_comments,
        'num_bloggers': num_bloggers,
    }

    return render(request, 'home.html', context=context)

class BlogListView(ListView):
    model = BlogPost
    paginate_by = 5

# class BlogDetailView(generic.DetailView):
    # model = BlogPost


class BloggerListView(ListView):
    model = Blogger

class BloggerDetailView(DetailView):
    model = Blogger



"""
BLOGGER FEATURES
"""

class BloggerUpdate(PermissionRequiredMixin, UpdateView):
    model = Blogger
    fields = ['first_name', 'last_name', 'nickname', 'bio']
    permission_required = 'blog.is_blogger'

class BlogPostCreate(CreateView):
    model = BlogPost
    fields = ['title', 'description', 'post']
    # permission_required = 'blog.is_blogger'

    def form_valid(self, form):
        author = self.request.user.blogger
        form.instance.author = author
        return super(BlogPostCreate, self).form_valid(form)

class BlogPostUpdate(PermissionRequiredMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'description', 'post']
    permission_required = 'blog.is_blogger'

class BlogPostDelete(PermissionRequiredMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog-list')
    permission_required = 'blog.is_blogger'


def blog_detail(request, pk):
    blogpost = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post = blogpost
            comment.user = request.user
            comment.save()
            
            url = reverse('blog-detail', kwargs={'pk': pk})
            
            return HttpResponseRedirect(url)

    else:
        form = CommentForm

    context = {
        'blogpost': blogpost,
        'form': form,
    }

    return render(request, 'blog/blogpost_detail.html', context=context)

"""
SIGN UP AND CREATE PROFILE
"""

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

def register(response):
    form = UserCreationForm

    if response.method == 'POST':
        form = UserCreationForm(response.POST)

        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Blogger')
            user.groups.add(group)            

            # Redirect to profile login
            url = reverse('login')
            return HttpResponseRedirect(url)
    else:
        form = UserCreationForm


    context = {
        'form': form,
    }

    return render(response, 'blog/register.html', context=context)

from django.contrib.auth.models import User

def blogger_sign_up(request):
    if request.method == 'POST':
        form = BloggerSignUpForm(request.POST)
        
        if form.is_valid():
            form_complete = form.save(commit=False)
            form_complete.user = request.user
            form_complete.save()
            
            url = reverse('home')

            return HttpResponseRedirect(url)

    else:
        form = BloggerSignUpForm

    context = {
        'form': form,
    }

    return render(request, 'blog/blogger_register.html', context=context)


"""
DELETE PROFILE
"""

from .forms import DeleteUser

def delete_user(request):
    if request.method == 'POST':
        form = DeleteUser(request.POST)

        if form.is_valid():
            delete_user = User.objects.get(username=form.cleaned_data['username'])
            if delete_user == request.user:
                delete_user.delete()
                url = reverse('home')
                return HttpResponseRedirect(url)
    else:
        form = DeleteUser()
    
    context = {'form': form}

    return render(request, 'blog/blogger_delete.html', context=context)