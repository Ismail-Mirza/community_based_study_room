from .models import Post, Post
from django.forms import ModelForm



class PostForm(ModelForm):
    class Meta:
        model = Post
        fields ='__all__'
        exclude = ['host','slug','view']

