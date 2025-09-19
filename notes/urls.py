from django.urls import path
from .views import NoteListView, NoteDetailView, CreateNoteView, delete_note


urlpatterns = [
	path('', NoteListView.as_view(), name='notes'),
	path('note_detail/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
	path('create_note/', CreateNoteView.as_view(), name='create_note'),
	path('delete_note/<int:pk>/', delete_note, name='delete_note'),
]