from django.views.generic import TemplateView
from todo_app.models import TodoList
from notes.models import Note
from comments.models import Comment

class HomePageView(TemplateView):
    template_name = 'root/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.all().order_by('-date')

        if self.request.user.is_authenticated:
            todo_list = TodoList.objects.filter(owner=self.request.user).order_by('-date')
            notes = Note.objects.filter(owner=self.request.user).order_by('-date')
        else:
            todo_list = TodoList.objects.none()
            notes = Note.objects.none()

        context['todo_list'] = todo_list
        context['notes'] = notes
        context['comments'] = comments

        return context



class HelpPageView(TemplateView):
	template_name = 'root/help_page.html'


