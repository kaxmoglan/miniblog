from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm

from blog.models import *
from blog.forms import *
from blog.views import *

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

        cls.view = BlogListView()

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

    def test_bloglistview_attrs(self):
        self.assertEqual(self.view.model, BlogPost)

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

    def test_bloglistview_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('blog-list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogpost_list']) == 3)

"""
BLOGGER LIST VIEW
"""

class BloggerListViewTest(TestCase):
    """
    SET UP 8 BLOGGERS
    """

    @classmethod
    def setUpTestData(cls):

        cls.view = BloggerListView()

        num_bloggers = 8

        for blogger in range(num_bloggers):
            test_user = User.objects.create_user(
                username=f'testuser{blogger}',
                password='top_secrets'
            )

            test_blogger = Blogger.objects.create(
                user = test_user,
                first_name = 'Test',
                last_name = 'User',
                bio = 'This is the bio',
                nickname = f'testies{blogger}'
            )

    """
    TESTS
    """

    def test_bloggerlistview_attrs(self):
        self.assertEqual(self.view.model, Blogger)

    def test_bloggerlistview_url(self):
        response = self.client.get('/blog/allbloggers/')
        self.assertEqual(response.status_code, 200)

    def test_bloggerlistview_url_accessible_by_name(self):
        response = self.client.get(reverse('blogger-list'))
        self.assertEqual(response.status_code, 200)

    def test_bloggerlistview_uses_correct_template(self):
        response = self.client.get(reverse('blogger-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogger_list.html')

    def test_bloggerlistview_pagination_is_five(self):
        response = self.client.get(reverse('blogger-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogger_list']) == 5)

    def test_bloggerlistview_lists_all_authors(self):
        # GET SECOND PAGE AND CONFIRM IT HAS EXACTLY REMAINING 3 BLOGGERS
        response = self.client.get(reverse('blogger-list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogger_list']) == 3)


"""
BLOGGER DETAIL VIEW
"""

class BloggerDetailViewTest(TestCase):

    """
    SET UP 2 BLOGGERS WITH 1 POST EACH
    """
    
    @classmethod
    def setUpTestData(cls):

        cls.view = BloggerDetailView()

        test_user1 = User.objects.create_user(
                username='testuser',
                password='top_secrets'
        )
        
        test_blogger1 = Blogger.objects.create(
            user = test_user1,
            first_name = 'Test',
            last_name = 'User',
            bio = 'This is the bio',
            nickname = 'Testies'
        )     

    """
    TESTS
    """

    def test_blogdetailview_attrs(self):
        self.assertEqual(self.view.model, Blogger)

    def test_bloggerdetailview_url(self):
        response = self.client.get('/blog/blogger/1')
        self.assertEqual(response.status_code, 200)

    def test_bloggerdetailview_url_accessible_by_name(self):
        response = self.client.get(reverse('blogger-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_bloggerdetailview_uses_correct_template(self):
        response = self.client.get(reverse('blogger-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogger_detail.html')

    
"""
BLOGGER UPDATE VIEW
"""

class BloggerUpdateViewTest(TestCase):
    """
    SET UP BLOGGER
    """
    @classmethod
    def setUpTestData(cls):

        cls.view = BloggerUpdate()

        test_user = User.objects.create_user(
            username='testuser',
            password='top_secrets'
        )
            
        test_blogger = Blogger.objects.create(
            user = test_user,
            first_name = 'Test',
            last_name = 'User',
            bio = 'This is the bio',
            nickname = 'Testies'
        )  

        permission = Permission.objects.get(name='is Blogger')
        test_user.user_permissions.add(permission)  
        

    """
    TESTS
    """
    def test_bloggerupdateview_attrs(self):
        self.assertEqual(self.view.model, Blogger)
    
    def test_blogupdateview_url(self):
        login = self.client.login(username='testuser', password='top_secrets')
        response = self.client.get('/blog/blogger/1/update/')
        self.assertEqual(response.status_code, 200)

    def test_blogupdateview_accessible_by_name(self):
        login = self.client.login(username='testuser', password='top_secrets')
        response = self.client.get(reverse('blogger-update', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_blogupdateview_not_accessible_for_anon_user(self):
        response = self.client.get(reverse('blogger-update', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_blogupdateview_uses_correct_template(self):
        login = self.client.login(username='testuser', password='top_secrets')
        response = self.client.get(reverse('blogger-update', args=[1]))
        self.assertTemplateUsed(response, 'blog/blogger_form.html')

"""
BLOG POST CREATE VIEW
"""

class BlogPostCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.view = BlogPostCreate()
   
    """
    TESTS
    """
    def test_blogpostcreateview_attrs(self):
        self.assertEqual(self.view.model, BlogPost)

    def test_blogpostcreateview_url(self):
        response = self.client.get('/blog/blogpost/create/')
        self.assertEqual(response.status_code, 200)

    def test_blogpostcreateview_accessible_by_name(self):
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)

    def test_blogpostcreateview_uses_correct_template(self):
        response = self.client.get(reverse('post-create'))
        self.assertTemplateUsed(response, 'blog/blogpost_form.html')

"""
BLOG POST UPDATE VIEW
"""

class BlogPostUpdateViewTest(TestCase):
    """
    SET UP BLOGGER
    """
    @classmethod
    def setUpTestData(cls):

        cls.view = BlogPostUpdate()

        test_user = User.objects.create_user(
            username='testuser',
            password='top_secrets'
        )
            
        test_blogger = Blogger.objects.create(
            user = test_user,
            first_name = 'Test',
            last_name = 'User',
            bio = 'This is the bio',
            nickname = 'Testies'
        )  

        permission = Permission.objects.get(name='is Blogger')
        test_user.user_permissions.add(permission)  
        
        test_post = BlogPost.objects.create(
            title = 'Blog Post Title',
            author = test_blogger,
            post = 'This is the blog post',
            description = 'This is the blog post description',
            published = timezone.now()
        )

    """
    TESTS
    """
    
    def test_blogpostupdateview_attrs(self):
        self.assertEqual(self.view.model, BlogPost)
    
    def test_blogpostupdateview_url(self):
        login = self.client.login(username='testuser', password='top_secrets')
        response = self.client.get('/blog/blogpost/1/update/')
        self.assertEqual(response.status_code, 200)

    def test_blogpostupdateview_accessible_by_name(self):
        login = self.client.login(username='testuser', password='top_secrets')
        response = self.client.get(reverse('post-update', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_blogpostupdateview_not_accessible_for_anon_user(self):
        response = self.client.get(reverse('post-update', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_blogpostupdateview_uses_correct_template(self):
        login = self.client.login(username='testuser', password='top_secrets')
        response = self.client.get(reverse('post-update', args=[1]))
        self.assertTemplateUsed(response, 'blog/blogpost_form.html')

"""
BLOG POST DELETE VIEW
"""

class BlogPostDeleteViewTest(TestCase):
    """
    SET UP BLOGGER
    """
    @classmethod
    def setUpTestData(cls):

        cls.view = BlogPostDelete()

        test_user = User.objects.create_user(
            username='testuser',
            password='top_secrets'
        )
            
        test_blogger = Blogger.objects.create(
            user = test_user,
            first_name = 'Test',
            last_name = 'User',
            bio = 'This is the bio',
            nickname = 'Testies'
        )  

        permission = Permission.objects.get(name='is Blogger')
        test_user.user_permissions.add(permission)  
        
        test_post = BlogPost.objects.create(
            title = 'Blog Post Title',
            author = test_blogger,
            post = 'This is the blog post',
            description = 'This is the blog post description',
            published = timezone.now()
        )

    """
    TESTS
    """

    def test_blogpostdeleteview_attrs(self):
        self.assertEqual(self.view.model, BlogPost)

    def test_blogpostdeleteview_url(self):
        login = self.client.login(username='testuser', password='top_secrets')
        response = self.client.get('/blog/blogpost/1/delete/')
        self.assertEqual(response.status_code, 200)

    def test_blogpostdeleteview_accessible_by_name(self):
        login = self.client.login(username='testuser', password='top_secrets')
        response = self.client.get(reverse('post-delete', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_blogpostdeleteview_not_accessible_for_anon_user(self):
        response = self.client.get(reverse('post-delete', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_blogpostdeleteview_uses_correct_template(self):
        login = self.client.login(username='testuser', password='top_secrets')
        response = self.client.get(reverse('post-delete', args=[1]))
        self.assertTemplateUsed(response, 'blog/blogpost_confirm_delete.html')

"""
BLOG DETAIL VIEW 
"""

class BlogDetailViewTest(TestCase):

    """
    SET UP BLOGGER WITH POST AND BLOGGER WITHOUT POST
    """
    @classmethod
    def setUpTestData(cls):

        test_user = User.objects.create_user(
            username='testuser',
            password='top_secrets'
        )
            
        test_blogger = Blogger.objects.create(
            user = test_user,
            first_name = 'Test',
            last_name = 'User',
            bio = 'This is the bio',
            nickname = 'Testies'
        )  

        permission = Permission.objects.get(name='is Blogger')
        test_user.user_permissions.add(permission)  
        
        test_post = BlogPost.objects.create(
            title = 'Blog Post Title',
            author = test_blogger,
            post = 'This is the blog post',
            description = 'This is the blog post description',
            published = timezone.now()
        )

        test_user2 = User.objects.create_user(
            username='testuser2',
            password='top_secrets'
        )
            
        test_blogger2 = Blogger.objects.create(
            user = test_user2,
            first_name = 'Test',
            last_name = 'User',
            bio = 'This is the bio',
            nickname = 'Testies2'
        )  
        permission = Permission.objects.get(name='is Blogger')
        test_user2.user_permissions.add(permission)  

    """
    GENERIC TESTS
    """

    def test_blogdetailview_url(self):
        response = self.client.get('/blog/blogpost/1')
        self.assertEqual(response.status_code, 200)

    def test_blogdetailview_accessible_by_name(self):
        response = self.client.get(reverse('blog-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_blogdetailview_not_accessible_for_anon_user(self):
        response = self.client.get(reverse('blog-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_blogdetailview_uses_correct_template(self):
        response = self.client.get(reverse('blog-detail', args=[1]))
        self.assertTemplateUsed(response, 'blog/blogpost_detail.html')

    """
    CONTEXT TESTS
    """
    def test_blogdetailview_accesses_blog(self):
        response = self.client.get(reverse('blog-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['blogpost'], BlogPost.objects.get(pk='1'))

    def test_blogdetailview_accesses_form(self):
        response = self.client.get(reverse('blog-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'], CommentForm)

    
"""
REGISTER VIEW 
"""

class RegisterViewTests(TestCase):

    """
    TESTS
    """

    def test_registerview_url(self):
        response = self.client.get('/blog/register/')
        self.assertEqual(response.status_code, 200)

    def test_registerview_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_registerview_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/register.html')

    def test_registerview_uses_correct_form(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'] == UserCreationForm)

"""
DELETE USER VIEW
"""

class DeleteUserView(TestCase):
  
    """
    SET UP BLOGGER
    """

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser',
            password='top_secrets'
        )
            
        test_blogger = Blogger.objects.create(
            user = test_user,
            first_name = 'Test',
            last_name = 'User',
            bio = 'This is the bio',
            nickname = 'Testies'
        )  

        permission = Permission.objects.get(name='is Blogger')
        test_user.user_permissions.add(permission)  

    """
    GENERIC TESTS
    """

    def test_deleteuserview_url(self):
        login = self.client.login(username='testuser', password='top_secrets')
        response = self.client.get('/blog/blogger/delete/')
        self.assertEqual(response.status_code, 200)
    
    def test_deleteuserview_accessible_by_name(self):
        login = self.client.login(username='testuser', password='top_secrets')
        response = self.client.get(reverse('blogger-delete'))
        self.assertEqual(response.status_code, 200)
    
    def test_deleteuserview_uses_correct_template(self):
        login = self.client.login(username='testuser', password='top_secrets')
        response = self.client.get(reverse('blogger-delete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogger_delete.html')


"""
DELETE USER SUCCESS VIEW
"""

class DeleteUserSuccessViewTest(TestCase):

    """
    TESTS
    """

    def test_deleteusersuccessview_url(self):
        response = self.client.get('/blog/blogger/delete/success/')
        self.assertEqual(response.status_code, 200)

    def test_deleteusersuccessview_url_accessible_by_name(self):
        response = self.client.get(reverse('blogger-delete-sucess'))
        self.assertEqual(response.status_code, 200)

    def test_deleteusersuccessview_uses_correct_template(self):
        response = self.client.get(reverse('blogger-delete-sucess'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogger_delete_success.html')