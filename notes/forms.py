from django import forms
from .models import Note


class NoteCreationForm(forms.ModelForm):
	class Meta:
		model = Note
		fields = ['title', 'body']


class NoteEditForm(forms.ModelForm):
	class Meta:
		model = Note
		fields = ['title', 'body']