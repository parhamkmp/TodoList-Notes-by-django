from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import TodoList, TodoListItem

User = get_user_model()


class TodoAppTests(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user1 = User.objects.create_user(username="user1", password="pass123", phone_number="09120000000")
        cls.user2 = User.objects.create_user(username="user2", password="pass456", phone_number="09120000001")


        cls.todo_list = TodoList.objects.create(
            owner=cls.user1,
            todo_list_name="My Todo List",
            todo_list_caption="Caption",
        )


        cls.task = TodoListItem.objects.create(
            item_name="Task 1",
            caption_name="Task caption",
            todo_list=cls.todo_list,
        )



    def test_todo_list_view_authenticated(self):
        self.client.login(username="user1", password="pass123")
        response = self.client.get(reverse("todo_lists"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo_app/todo_lists.html")
        self.assertContains(response, "My Todo List")



    def test_todo_list_view_unauthenticated_redirect(self):
        response = self.client.get(reverse("todo_lists"))
        self.assertEqual(response.status_code, 302) 



    def test_todo_list_detail_view_owner(self):
        self.client.login(username="user1", password="pass123")
        response = self.client.get(reverse("todo_list_detail", args=[self.todo_list.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo_app/todo_list_detail.html")
        self.assertContains(response, "Task 1")




    def test_todo_list_detail_view_other_user_forbidden(self):
        self.client.login(username="user2", password="pass456")
        response = self.client.get(reverse("todo_list_detail", args=[self.todo_list.pk]))
        self.assertEqual(response.status_code, 403)





    def test_add_task_to_todo_list(self):
        self.client.login(username="user1", password="pass123")
        data = {"item_name": "New Task", "caption_name": "New caption"}
        response = self.client.post(reverse("todo_list_detail", args=[self.todo_list.pk]), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(TodoListItem.objects.filter(item_name="New Task").exists())




    def test_do_task_owner(self):
        self.client.login(username="user1", password="pass123")
        response = self.client.post(reverse("do_task", args=[self.task.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_done)





    def test_do_task_other_user_forbidden(self):
        self.client.login(username="user2", password="pass456")
        response = self.client.post(reverse("do_task", args=[self.task.pk]))
        self.assertEqual(response.status_code, 403)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_done)




    def test_delete_task_owner(self):
        self.client.login(username="user1", password="pass123")
        response = self.client.post(reverse("delete_task", args=[self.task.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(TodoListItem.objects.filter(pk=self.task.pk).exists())




    def test_delete_task_other_user_forbidden(self):
        self.client.login(username="user2", password="pass456")
        response = self.client.post(reverse("delete_task", args=[self.task.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(TodoListItem.objects.filter(pk=self.task.pk).exists())




    def test_create_todo_list(self):
        self.client.login(username="user1", password="pass123")
        data = {"todo_list_name": "Second List", "todo_list_caption": "Second caption"}
        response = self.client.post(reverse("create_todo_list"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(TodoList.objects.filter(todo_list_name="Second List").exists())




    def test_delete_todo_list_owner(self):
        self.client.login(username="user1", password="pass123")
        response = self.client.post(reverse("delete_todo_list", args=[self.todo_list.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(TodoList.objects.filter(pk=self.todo_list.pk).exists())




    def test_delete_todo_list_other_user_forbidden(self):
        self.client.login(username="user2", password="pass456")
        response = self.client.post(reverse("delete_todo_list", args=[self.todo_list.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(TodoList.objects.filter(pk=self.todo_list.pk).exists())




    def test_do_todo_list_owner_marks_all_done(self):
        self.client.login(username="user1", password="pass123")
        response = self.client.post(reverse("do_todo_list", args=[self.todo_list.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.todo_list.refresh_from_db()
        self.assertTrue(self.todo_list.is_done)

        for item in self.todo_list.items.all():
            self.assertTrue(item.is_done)
