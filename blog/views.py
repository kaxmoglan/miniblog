from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.forms import ModelForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


from .models import BlogPost, Comment, Blogger
from .forms import CommentForm

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

class BlogListView(generic.ListView):
    model = BlogPost
    paginate_by = 5

# class BlogDetailView(generic.DetailView):
    # model = BlogPost


class BloggerListView(generic.ListView):
    model = Blogger

class BloggerDetailView(generic.DetailView):
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