from django import forms
from .models import Comment


class CommentCreationForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['rate', 'title', 'body']


class CommentEditForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['rate', 'title', 'body']