from django.test import TestCase

# Create your tests here.
from blog.models import Blogger, BlogPost, Comment
from django.contrib.auth.models import  User
from django.utils import timezone

# BLOGGER MODEL TESTS

class BloggerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='johndoe', password='top_secret'
        )
        Blogger.objects.create(
            user = test_user,
            first_name = 'John',
            last_name = 'Doe',
            bio = "This is John Doe's bio",
            nickname = 'johndoe66'
        )

    """
    LABELS
    """

    def test_blogger_first_name_label(self):
        blogger = Blogger.objects.get(id=1)
        field_label = blogger._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_blogger_last_name_label(self):
        blogger = Blogger.objects.get(id=1)
        field_label = blogger._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')

    def test_blogger_bio_label(self):
        blogger = Blogger.objects.get(id=1)
        field_label = blogger._meta.get_field('bio').verbose_name
        self.assertEquals(field_label, 'bio')

    def test_blogger_nickname_label(self):
        blogger = Blogger.objects.get(id=1)
        field_label = blogger._meta.get_field('nickname').verbose_name
        self.assertEquals(field_label, 'nickname')


    """
    MAX_LENGTHS
    """

    def test_blogger_first_name_maxlength(self):
        blogger = Blogger.objects.get(id=1)
        max_length = blogger._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_blogger_last_name_maxlength(self):
        blogger = Blogger.objects.get(id=1)
        max_length = blogger._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 100)
    
    def test_blogger_nickname_maxlength(self):
        blogger = Blogger.objects.get(id=1)
        max_length = blogger._meta.get_field('nickname').max_length
        self.assertEquals(max_length, 100)

    """
    OBJECT NAME
    """

    def test_blogger_object_name(self):
        blogger = Blogger.objects.get(id=1)
        expected_object_name = str(blogger.nickname)
        self.assertEquals(expected_object_name, str(blogger))

    """
    URL
    """
    def test_blogger_get_absolute_url(self):
        blogger = Blogger.objects.get(id=1)
        self.assertEquals(blogger.get_absolute_url(), '/blog/blogger/1')

# BLOGPOST MODEL TESTS

class BlogPostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='johndoe', password='top_secret'
        )
        test_blogger = Blogger.objects.create(
            user = test_user,
            first_name = 'John',
            last_name = 'Doe',
            bio = "This is John Doe's bio",
            nickname = 'johndoe66'
        )
        BlogPost.objects.create(
            title = 'Blog Post Title',
            author = test_blogger,
            post = 'This is the blog post test',
            description = 'This is the blog post description',
            published = timezone.now()
        )

    """
    LABELS
    """

    def test_blogpost_title_label(self):
        blogpost = BlogPost.objects.get(id=1)
        field_label = blogpost._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_blogpost_author_label(self):
        blogpost = BlogPost.objects.get(id=1)
        field_label = blogpost._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_blogpost_post_label(self):
        blogpost = BlogPost.objects.get(id=1)
        field_label = blogpost._meta.get_field('post').verbose_name
        self.assertEquals(field_label, 'post')

    def test_blogpost_description_label(self):
        blogpost = BlogPost.objects.get(id=1)
        field_label = blogpost._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_blogpost_published_label(self):
        blogpost = BlogPost.objects.get(id=1)
        field_label = blogpost._meta.get_field('published').verbose_name
        self.assertEquals(field_label, 'published')


    """
    MAX_LENGTHS
    """

    def test_blogpost_title_max_length(self):
        blogpost = BlogPost.objects.get(id=1)
        max_length = blogpost._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)
    
    def test_blogpost_description_max_length(self):
        blogpost = BlogPost.objects.get(id=1)
        max_length = blogpost._meta.get_field('description').max_length
        self.assertEquals(max_length, 500)

    """
    OBJECT NAME
    """

    def test_blogpost_object_name(self):
        blogpost = BlogPost.objects.get(id=1)
        expected_object_name = 'Blog Post Title'
        self.assertEquals(expected_object_name, str(blogpost.title))

    """
    URL
    """

    def test_blogpost_get_absolute_url(self):
        blogpost = BlogPost.objects.get(id=1)
        self.assertEquals(blogpost.get_absolute_url(), '/blog/blogpost/1')


# COMMENT MODEL TESTS

class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='johndoe', password='top_secret'
        )
        test_blogger = Blogger.objects.create(
            user = test_user,
            first_name = 'John',
            last_name = 'Doe',
            bio = "This is John Doe's bio",
            nickname = 'johndoe66'
        )
        test_blogpost = BlogPost.objects.create(
            title = 'Blog Post Title',
            author = test_blogger,
            post = 'This is the blog post test',
            description = 'This is the blog post description',
            published = timezone.now()
        )
        Comment.objects.create(
            user = test_user,
            comment = 'This is the test comment',
            blog_post = test_blogpost,
            published = timezone.now()
        )

    """
    LABELS
    """

    def test_comment_user_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_comment_comment_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('comment').verbose_name
        self.assertEquals(field_label, 'comment')

    def test_comment_blogpost_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('blog_post').verbose_name
        self.assertEquals(field_label, 'blog post')

    def test_blogpost_published_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('published').verbose_name
        self.assertEquals(field_label, 'published')

    """
    OBJECT NAME
    """

    def test_comment_object_name(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = '1'
        self.assertEquals(expected_object_name, str(comment.pk))

