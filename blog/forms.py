from django import forms
from .models import Comment, Blogger

# class CommentForm(forms.Form):
#     comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
          'comment': forms.Textarea(attrs={'rows':3, 'cols':40}),
        }

class BloggerSignUpForm(forms.ModelForm):
  class Meta:
    model = Blogger
    fields = ('first_name', 'last_name', 'nickname', 'bio',)

class DeleteUserForm(forms.Form):
  username = forms.CharField()