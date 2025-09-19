from django import forms
from .models import TodoList, TodoListItem

class TodoListCreateForm(forms.ModelForm):
	class Meta:
		model = TodoList
		fields = ['todo_list_name', 'todo_list_caption']

class TodoListItemCreationForm(forms.ModelForm):
	class Meta:
		model = TodoListItem
		fields = ['item_name', 'caption_name']