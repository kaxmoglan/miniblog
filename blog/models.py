from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

# Create your models here.

class BlogPost(models.Model):
    # FIELDS
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField()
    description = models.CharField(max_length=500)
    published = models.DateTimeField(default=timezone.now)

    # METHODS
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={"pk": self.pk})
    

class Comment(models.Model):
    # FIELDS
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    blog_post = models.ForeignKey(BlogPost, on_delete=models.SET_NULL, null=True)

    # METHODS
    def __str__(self):
        return f'Comment: {self.pk} on {self.blog_post.title} by {self.user}'



    