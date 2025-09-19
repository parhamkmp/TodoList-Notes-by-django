from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Note(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=100, null=False, blank=False, unique=True)
	body = models.TextField(max_length=1024, null=False, blank=False)
	owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='owner_note')

	def __str__(self):
		return self.title

	@property
	def body_summary(self):
		return f'{self.body[:20]} ...'

	def get_absolute_url(self):
		return reverse('note_detail', kwargs={'pk':self.pk})