from django import forms
from blogs.models import Blog, Post
import os


class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description']


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'content', 'summary', 'thumbnail', 'category']
