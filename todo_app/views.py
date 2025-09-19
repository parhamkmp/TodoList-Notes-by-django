from django.views.generic import ListView, TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import TodoListCreateForm, TodoListItemCreationForm
from .models import TodoList, TodoListItem



class TodoListView(LoginRequiredMixin, ListView):
	model = TodoList
	template_name = 'todo_app/todo_lists.html'
	context_object_name = 'TodoList'

	def get_queryset(self):
		return TodoList.objects.filter(owner=self.request.user)



class TodoListDetailView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = TodoList
	template_name = 'todo_app/todo_list_detail.html'
	form_class = TodoListItemCreationForm
	success_url = reverse_lazy('todo_lists')


	# for create item
	def form_valid(self, form):
		todo_list = get_object_or_404(TodoList, pk=self.kwargs.get('pk'))
		item = form.save(commit=False)
		item.todo_list = todo_list
		item.save()
		super().form_valid(form)
		return redirect('todo_list_detail', pk=self.kwargs.get('pk'))

	# access condition
	def test_func(self):
		pk = self.kwargs.get('pk') # Give pk from url
		todo_list = get_object_or_404(TodoList, pk=pk)
		return todo_list.owner == self.request.user


	# If the condition was not met
	def handel_no_permission(self):
		return HttpResponseForbidden(self.request, '403.html')
	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # Give pk from url
		todo_list = get_object_or_404(TodoList, pk=pk)
		
		context['TodoList'] = todo_list
		context['TodoListItem'] = TodoListItem.objects.filter(todo_list=todo_list)
		
		return context



@login_required
def do_task(request, pk):
	task = get_object_or_404(TodoListItem, pk=pk)
	if request.method == 'POST' and task.todo_list.owner == request.user:
		task.is_done = True
		task.save()
	else:
		return render(request, '403.html', status=403)

	return redirect('todo_list_detail', pk=task.todo_list.pk)




@login_required
def delete_task(request, pk):
	task = get_object_or_404(TodoListItem, pk=pk)
	task_pk = task.todo_list.pk
	if request.method == 'POST' and task.todo_list.owner == request.user:
		task.delete()
	else:
		return render(request, '403.html', status=403)

	return redirect('todo_list_detail', pk=task_pk)




class CreateTodoListView(CreateView):
	model = TodoList
	form_class = TodoListCreateForm
	template_name = 'todo_app/create_todo_list.html'
	success_url = reverse_lazy('todo_lists')

	def form_valid(self, form):
		# OLD CODE:
		
		# todo_list = form.save(commit=False)
		# todo_list.owner = self.request.user
		# todo_list.save()
		# return super().form_valid(form)

		# CLEAN CODE:

		form.instance.owner = self.request.user
		return super().form_valid(form)


@login_required
def delete_todo_list(request, pk):
	todo_list = get_object_or_404(TodoList, pk=pk)
	if request.method == 'POST' and todo_list.owner == request.user:
		todo_list.delete()

	else:
		return render(request, '403.html', status=403)

	return redirect('todo_lists')



@login_required
def do_todo_list(request, pk):
	todo_list = get_object_or_404(TodoList, pk=pk)
	if request.method == 'POST' and todo_list.owner == request.user:
		todo_list.is_done = True
		todo_list.save()

	else:
		return render(request, '403.html', status=403)

	return redirect('todo_list_detail', pk=todo_list.pk)



