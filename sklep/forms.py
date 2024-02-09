from django import forms
from .models import Review, BlogPost

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']

class BlogPostForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Content'}))

    class Meta:
        model = BlogPost
        fields = ['title', 'content']