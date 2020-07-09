from django.contrib import admin
from .models import Blogger, BlogPost, Comment
from django.contrib.auth.models import User

# Register your models here.

"""
BLOG POST ADMIN PAGE WITH INLINE COMMENTS
"""
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'description', 'published',]
    fields = ['title', 'description', 'author', 'published', 'post']
    inlines = [CommentInline]

"""
ALL COMMENTS ADMIN SECTION
"""

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog_post', 'published', 'pk']

"""
BLOGGER ADMIN PAGE WITH INLINE POSTS BY BLOGGER
"""

class BlogPostsInline(admin.TabularInline):
    model = BlogPost
    extra = 0

@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname', 'first_name', 'last_name', 'pk']
    fields = ['user', 'first_name', 'last_name', 'nickname', 'bio']
    inlines = [BlogPostsInline]

admin.site.site_header = "Max's Mini Blog Admin Portal"