from django.db import models
from django.contrib.auth import get_user_model

RATE_CHOICES = (
	('1','1'),
	('2','2'),
	('3','3'),
	('4','4'),
	('5','5'),
)

class Comment(models.Model):
	user = models.ForeignKey(get_user_model(), related_name='user', on_delete=models.CASCADE)
	rate = models.CharField(choices=RATE_CHOICES, null=False, blank=False)
	title = models.CharField(max_length=50, null=False, blank=False)
	body = models.TextField(max_length=100, null=False, blank=False)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


