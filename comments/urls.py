from django.urls import path
from .views import CommentListView, delete_comment, CommentEditView


urlpatterns = [
	path('', CommentListView.as_view(), name='comments'),
	path('delete/<int:pk>/', delete_comment, name='delete_comment'),
	path('edit_comment/<int:pk>/', CommentEditView.as_view(), name='edit_comment'),
]