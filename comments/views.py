from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentCreationForm, CommentEditForm
from .models import Comment



class CommentListView(CreateView):
	model = Comment
	template_name = 'comments/comment_list.html'
	form_class = CommentCreationForm
	success_url = reverse_lazy('comments')

	
	def form_valid(self, form):
		form.instance.user = self.request.user
		super().form_valid(form)
		return redirect('comments')


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		comment = Comment.objects.all().order_by('-date')
		context['comments'] = comment
		return context


@login_required
def delete_comment(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	if request.method == 'POST' and request.user == comment.user:
		comment.delete()
	else:
		return render(request, '403.html', status=403)

	return redirect('comments')



class CommentEditView(UpdateView):
    model = Comment
    template_name = "comments/comment_edit.html"
    form_class = CommentEditForm
    success_url = reverse_lazy('comments')

    def get_object(self, queryset=None):
    	pk = self.kwargs.get('pk')
    	return get_object_or_404(Comment, pk=pk, user=self.request.user)