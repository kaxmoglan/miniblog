from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from blog.models import Blogger, BlogPost, Comment

"""
HOME PAGE VIEW
"""

class HomePageViewTest(TestCase):

    """
    SET UP 2 USERS, 2 POSTS, 2 COMMENTS
    """

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username='johndoe', password='top_secret'
        )
        test_user2 = User.objects.create_user(
            username='janedoe', password='top_secret'
        )
        test_blogger1 = Blogger.objects.create(
            user = test_user1,
            first_name = 'John',
            last_name = 'Doe',
            bio = "This is John Doe's bio",
            nickname = 'johndoe66'
        )
        test_blogger2 = Blogger.objects.create(
            user = test_user2,
            first_name = 'Jane',
            last_name = 'Doe',
            bio = "This is Jane Doe's bio",
            nickname = 'janedoe77'
        )
        test_blogpost1 = BlogPost.objects.create(
            title = 'Blog Post Title 1',
            author = test_blogger1,
            post = 'This is the blog post test 1',
            description = 'This is the blog post 1 description',
            published = timezone.now()
        )
        test_blogpost2 = BlogPost.objects.create(
            title = 'Blog Post Title 2',
            author = test_blogger2,
            post = 'This is the blog post test 2',
            description = 'This is the blog post 2 description',
            published = timezone.now()
        )
        test_comment1 = Comment.objects.create(
            user = test_user2,
            comment = 'This is the test comment 1',
            blog_post = test_blogpost1,
            published = timezone.now()
        )
        test_comment2 = Comment.objects.create(
            user = test_user1,
            comment = 'This is the test comment 2',
            blog_post = test_blogpost2,
            published = timezone.now()
        )

    """
    GENERIC TESTS || NOT LOGGED IN
    """


    def test_homepageview_redirect_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 301)

    def test_homepageview_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_homepageview_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_homepageview_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    # CONTEXT COUNT
    def test_homepageview_posts_count(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['num_blog_posts'] == 2)
    
    def test_homepageview_blogger_count(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['num_bloggers'] == 2)
    
    def test_homepageview_comment_count(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['num_comments'] == 2)


