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
    TESTS
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

    """
    CONTEXT
    """

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


"""
BLOG LIST VIEW
"""

class BlogListViewTest(TestCase):
    """
    SET UP 2 BLOGGERS WITH 4 POSTS EACH
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

        number_of_posts = 4

        for post in range(number_of_posts):
            BlogPost.objects.create(
                title = f'Blog Post {post}',
                author = test_blogger1,
                post = f'This is post content for Post {post}',
                description = f'Test Post {post}',
                published = timezone.now()
            )

        for post in range(number_of_posts):
            BlogPost.objects.create(
                title = f"Jane's Blog Post {post}",
                author = test_blogger2,
                post = f"This is post content for Jane's Post {post}",
                description = f"Jane's Test Post {post}",
                published = timezone.now()
            )

    """
    TESTS
    """

    def test_bloglistview_url(self):
        response = self.client.get('/blog/allblogs/')
        self.assertEqual(response.status_code, 200)

    def test_bloglistview_accessible_by_name(self):
        response = self.client.get(reverse('blog-list'))
        self.assertEqual(response.status_code, 200)

    def test_bloglistview_uses_correct_template(self):
        response = self.client.get(reverse('blog-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogpost_list.html')
    
    def test_bloglistview_pagination_is_five(self):
        response = self.client.get(reverse('blog-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogpost_list']) == 5)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('blog-list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogpost_list']) == 3)