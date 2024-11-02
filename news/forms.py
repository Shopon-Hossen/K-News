from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=300, label='', widget=forms.Textarea(attrs={'rows': 2}))
    class Meta:
        model = Comment
        fields = ['content']
