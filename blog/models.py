from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

# Create your models here.

class Blogger(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    bio = models.TextField(null=True)
    nickname = models.CharField(max_length=100, null=True)

    # METHODS
    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return reverse("blogger-detail", args=[str(self.id)])

    # META
    class Meta:
        permissions = [('is_blogger', 'is Blogger'),]
    


class BlogPost(models.Model):
    # FIELDS
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Blogger', on_delete=models.CASCADE, null=True)
    post = models.TextField()
    description = models.CharField(max_length=500)
    published = models.DateTimeField(default=timezone.now)

    # METHODS
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-published']
        # num_comments = Comment.objects.count()

    

class Comment(models.Model):
    # FIELDS
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now=True)

    # METHODS
    def __str__(self):
        return str(self.pk)

    # META
    class Meta:
        ordering = ['-published']



    