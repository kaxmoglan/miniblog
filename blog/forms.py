from django import forms
from .models import Comment

# class CommentForm(forms.Form):
#     comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
          'comment': forms.Textarea(attrs={'rows':3, 'cols':40}),
        }