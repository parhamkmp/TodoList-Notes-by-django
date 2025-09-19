from django.contrib import admin
from .models import TodoListItem, TodoList

class TodoListItemLine(admin.StackedInline):
	model = TodoListItem
	extera = 1

class TodoListAdmin(admin.ModelAdmin):
	list_display = ['todo_list_name', 'owner' , 'is_done']
	inlines = [TodoListItemLine]


admin.site.register(TodoList,TodoListAdmin)


@admin.register(TodoListItem)
class TodoListItemAdmin(admin.ModelAdmin):
	list_display = ['item_name', 'todo_list' , 'is_done']



