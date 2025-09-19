from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model



class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = CustomUser
		fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'job', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = UserChangeForm.Meta.fields




# class EditProfileForm(forms.ModelForm):
# 	class Meta:
# 		User = get_user_model()
# 		model = User
# 		fields = ('first_name', 'last_name', 'email', 'phone_number', 'job')

