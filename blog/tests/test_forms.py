from django.test import TestCase

# Create your tests here.
from blog.forms import CommentForm, BloggerSignUpForm, DeleteUserForm


"""
COMMENT FORM
"""

class CommentFormTest(TestCase):

    def test_commentform_comment_field_label(self):
        form = CommentForm()
        self.assertTrue(
            form.fields['comment'].label == 'Comment' or
            form.fields['comment'].label == None
        )

"""
BLOGGER SIGN UP FORM
"""

class BloggerSignUpFormTest(TestCase):

    """
    LABELS
    """

    def test_signupform_first_name_label(self):
        form = BloggerSignUpForm()
        self.assertTrue(
            form.fields['first_name'].label == 'First name' or
            form.fields['first_name'].label == None
        )

    def test_signupform_last_name_label(self):
        form = BloggerSignUpForm()
        self.assertTrue(
            form.fields['last_name'].label == 'Last name' or
            form.fields['last_name'].label == None
        )

    def test_signupform_nickname_label(self):
        form = BloggerSignUpForm()
        self.assertTrue(
            form.fields['nickname'].label == 'Nickname' or
            form.fields['nickname'].label == None
        )

    def test_signupform_bio_label(self):
        form = BloggerSignUpForm()
        self.assertTrue(
            form.fields['bio'].label == 'Bio' or 
            form.fields['bio'].label == None
        )

"""
DELETE USER FORM
"""

class DeleteUserFormTest(TestCase):

    """
    LABELS
    """

    def test_deleteuserform_username_label(self):
        form = DeleteUserForm()
        self.assertTrue(
            form.fields['username'].label == 'Username' or
            form.fields['username'].label == None
            
        )