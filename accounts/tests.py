from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()



class SignUpViewTests(TestCase):
	
	def test_signup_page_loads(self):
		response = self.client.get(reverse('sign_up_page'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'registration/signup.html')

	def test_user_can_signup(self):
		response = self.client.post(
			reverse('sign_up_page'),
			{
				'username':'testuser',
				'password1':'StrongPassword123',
				'password2':'StrongPassword123',
				'phone_number':'09123345678',
				'job':'Doctor',
			},
		)

		self.assertRedirects(response, reverse('login'))
		self.assertTrue(User.objects.filter(username='testuser').exists())


class ProfileViewTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create_user(
			username='mrtest',
			password='password123',
			phone_number='09123345678',
			job='programmer',
		)

	def test_profile_context_data(self):
		self.client.login(username='mrtest', password='password123')
		response = self.client.get(reverse('profile_page'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['user'], self.user)
		self.assertIn('todo_list', response.context)
		self.assertIn('notes', response.context)