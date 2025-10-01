from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import NoteCreationForm, NoteEditForm
from .models import Note




class NoteListView(LoginRequiredMixin, ListView):
	model = Note
	template_name = 'note/note_list.html'
	context_object_name = 'note'

	def get_queryset(self):
		return Note.objects.filter(owner=self.request.user)



class NoteDetailView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Note
	template_name = 'note/note_detail.html'
	form_class = NoteEditForm
	success_url = reverse_lazy('notes')


	def test_func(self):
		pk = self.kwargs.get('pk')
		note = get_object_or_404(Note, pk=pk)
		return note.owner == self.request.user

	def handel_no_permission(self):
		return HttpResponseForbidden(self.request, '403.html')


	def get_object(self, queryset=None):
		pk = self.kwargs.get('pk')
		return get_object_or_404(Note, pk=pk, owner=self.request.user)


	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		note_detail = get_object_or_404(Note, pk=self.kwargs.get('pk'))
		context['note_detail'] = note_detail

		return context





class CreateNoteView(CreateView):
	model = Note
	template_name = 'note/create_note.html'
	form_class = NoteCreationForm
	success_url = reverse_lazy('notes')


	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)



@login_required
def delete_note(request, pk):
	note = get_object_or_404(Note, pk=pk)
	if request.method == 'POST' and note.owner == request.user:
		note.delete()
	else:
		return HttpResponseForbidden(request,'403.html')

	return redirect('notes')




