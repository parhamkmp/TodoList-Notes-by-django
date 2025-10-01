from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Comment

User = get_user_model()


class CommentViewTests(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user1 = User.objects.create_user(username='user1', password='pass123', phone_number='09124434598')
		cls.user2 = User.objects.create_user(username='user2', password='pass456', phone_number='09458898783')


	def test_comment_list_view(self):
		Comment.objects.create(user=self.user1, rate='5', title='Test Title', body='Test body')
		self.client.login(username='user1', password='pass123')

		response = self.client.get(reverse('comments'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'comments/comment_list.html')
		self.assertIn('comments', response.context)
		self.assertEqual(response.context['comments'].count(), 1)
		self.assertContains(response, 'Test Title')


	def test_create_comment(self):
		self.client.login(username='user1', password='pass123')
		data = {
			'rate':'4',
			'title':'New Comment',
			'body':'This is a test comment',
		}
		response = self.client.post(reverse('comments'), data, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(Comment.objects.filter(title='New Comment').exists())



	def test_edit_comment_by_owner(self):
		comment = Comment.objects.create(user=self.user1, rate='3', title='Edit Me', body='Old Body')
		self.client.login(username='user1', password='pass123')

		response = self.client.post(
			reverse('edit_comment', args=[comment.pk]),
			{'rate':'5', 'title':'Edited', 'body':'New Body'},
			follow=True,
		)


		response_for_found_template_used = self.client.get(reverse('edit_comment', args=[comment.pk]),)

		self.assertEqual(response.status_code, 200)

		self.assertTemplateUsed(response_for_found_template_used, 'comments/comment_edit.html')

		comment.refresh_from_db()
		self.assertEqual(comment.title, 'Edited')
		self.assertEqual(comment.body,'New Body')


	def test_edit_comment_by_other_user(self):
		comment = Comment.objects.create(user=self.user1, rate='3', title='Edit Me', body='Old Body')
		self.client.login(username='user2', password='pass456')

		response = self.client.get(reverse('edit_comment', args=[comment.pk]))
		self.assertEqual(response.status_code, 404)



	def test_delete_comment_by_owner(self):
		comment = Comment.objects.create(user=self.user1, rate="2", title="ToDelete", body="Body")		
		self.client.login(username='user1', password='pass123')

		response = self.client.post(reverse('delete_comment', args=[comment.pk]))
		self.assertEqual(response.status_code, 302)
		self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())



	def test_delete_comment_by_other(self):
		comment = Comment.objects.create(user=self.user1, rate='2', title='ToDelete', body='Body')
		self.client.login(username='user2', password='pass456')

		response = self.client.post(reverse('delete_comment', args=[comment.pk]))
		self.assertEqual(response.status_code, 403)
		self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())


	def test_delete_comment_by_anonymouse(self):
		comment = Comment.objects.create(user=self.user1, rate='2', title='AnonDelete', body='Body')

		response = self.client.post(reverse('delete_comment', args=[comment.pk]))
		self.assertEqual(response.status_code, 302)
		self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())

