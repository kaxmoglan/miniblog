from django.contrib import admin
from .models import BlogPost, Comment

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'description', 'published',]
    fields = ['title', 'description', 'user', 'published', 'post']
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog_post', 'published', 'pk']