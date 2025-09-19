from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from todo_app.models import TodoList
from notes.models import Note



class SignUpView(CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/signup.html'

class ProfileView(LoginRequiredMixin, TemplateView):
	template_name = 'registration/profile.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		todo_list = TodoList.objects.filter(owner=self.request.user)
		completed_todo_list = todo_list.filter(is_done=True)
		pending_todo_list = todo_list.filter(is_done=False)
		todo_list = TodoList.objects.filter(owner=self.request.user)
		notes = Note.objects.filter(owner=self.request.user)
		context['user'] = user
		context['todo_list'] = todo_list
		context['completed_todo_list'] = completed_todo_list
		context['pending_todo_list'] = pending_todo_list
		context['notes'] = notes

		return context



