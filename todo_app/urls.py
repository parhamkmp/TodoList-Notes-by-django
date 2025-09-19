from django.urls import path
from .views import (TodoListView, TodoListDetailView,
 do_task, delete_task, CreateTodoListView, delete_todo_list, do_todo_list)


urlpatterns = [
	path('', TodoListView.as_view(), name='todo_lists'),
	path('todo_list_detail/<int:pk>/', TodoListDetailView.as_view(), name='todo_list_detail'),
	path('todo_list_detail/do_task/<int:pk>/', do_task, name='do_task'),
	path('todo_list_detail/delete_task/<int:pk>/', delete_task, name='delete_task'),
	path('create_new_todo_list/', CreateTodoListView.as_view(), name='create_todo_list'),
	path('delete_todo_list/<int:pk>/', delete_todo_list, name='delete_todo_list'),
	path('do_todo_list/<int:pk>/', do_todo_list, name='do_todo_list'),
]