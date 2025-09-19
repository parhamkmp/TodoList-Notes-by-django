from django.urls import path
from .views import SignUpView, ProfileView

urlpatterns = [
	path('signup/', SignUpView.as_view(), name='sign_up_page'),
	path('profile/', ProfileView.as_view(), name='profile_page'),
]