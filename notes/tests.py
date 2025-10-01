from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Note

User = get_user_model()


class NoteViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user1 = User.objects.create_user(username='user1', password='pass123', phone_number='09123456789')
        cls.user2 = User.objects.create_user(username='user2', password='pass456', phone_number='09198765432')

        cls.note1 = Note.objects.create(owner=cls.user1, title='Note 1', body='Body of Note 1')



    def test_note_list_view_authenticated(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('notes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'note/note_list.html')
        self.assertIn(self.note1, response.context['note'])

    def test_note_list_view_unauthenticated(self):
        response = self.client.get(reverse('notes'))
        self.assertEqual(response.status_code, 302)



    def test_note_detail_view_owner(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('note_detail', args=[self.note1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'note/note_detail.html')
        self.assertContains(response, self.note1.title)



    def test_note_detail_view_other_user_forbidden(self):
        self.client.login(username='user2', password='pass456')
        response = self.client.get(reverse('note_detail', args=[self.note1.pk]))
        self.assertEqual(response.status_code, 403)



    def test_note_edit_by_owner(self):
        self.client.login(username='user1', password='pass123')
        data = {'title': 'Updated Note', 'body': 'Updated Body'}
        response = self.client.post(reverse('note_detail', args=[self.note1.pk]), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, 'Updated Note')
        self.assertEqual(self.note1.body, 'Updated Body')





    def test_create_note_view(self):
        self.client.login(username='user1', password='pass123')
        data = {'title': 'New Note', 'body': 'New note body'}
        response = self.client.post(reverse('create_note'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Note.objects.filter(title='New Note').exists())




    def test_delete_note_by_owner(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('delete_note', args=[self.note1.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Note.objects.filter(pk=self.note1.pk).exists())

 

    def test_delete_note_by_other_user_forbidden(self):
        self.client.login(username='user2', password='pass456')
        response = self.client.post(reverse('delete_note', args=[self.note1.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Note.objects.filter(pk=self.note1.pk).exists())

 


    def test_delete_note_unauthenticated_redirect(self):
        response = self.client.post(reverse('delete_note', args=[self.note1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(pk=self.note1.pk).exists())
