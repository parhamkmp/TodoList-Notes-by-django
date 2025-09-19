from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse





class TodoList(models.Model):
	owner = models.ForeignKey(get_user_model(), related_name='owner', on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	todo_list_name = models.CharField(max_length=50, blank=False, null=False, unique=True)
	todo_list_caption = models.TextField(max_length=100)
	is_done = models.BooleanField(default=False)

	def __str__(self):
		return f'Todo List -> {self.todo_list_name}'

	def get_absolute_url(self):
		return reverse('todo_list_detail', kwargs={'pk':self.pk})

	def save(self, *args, **kwargs):
		previous_is_done = None
		if self.pk:
			previous_is_done = TodoList.objects.filter(pk=self.pk).values_list('is_done', flat=True).first()

		super().save(*args, **kwargs)

		if previous_is_done is False and self.is_done is True:
			self.items.update(is_done=True)


class TodoListItem(models.Model):
	item_name = models.CharField(max_length=150, unique=True)
	caption_name = models.TextField(max_length=200)
	todo_list = models.ForeignKey(TodoList, related_name='items', on_delete=models.CASCADE)
	is_done = models.BooleanField(default=False)


	def save(self, *args, **kwargs):
		super(TodoListItem, self).save(*args, **kwargs)
		todo = self.todo_list
		all_done = todo.items.filter(is_done=False).count() == 0	
		if todo.is_done != all_done:
			TodoList.objects.filter(pk=todo.pk).update(is_done=all_done)
	

	def __str__(self):
		return f'Item -> {self.item_name} | todo list -> {self.todo_list.todo_list_name}'