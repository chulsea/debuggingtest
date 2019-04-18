from django import forms
from .models import *

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content',]
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        field = ['content',]