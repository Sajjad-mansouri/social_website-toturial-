from django import forms
from .models import Profile
from django.contrib.auth.models import User
class LoginForm(forms.Form):
	username=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.ModelForm):
	password1=forms.CharField(label='password',widget=forms.PasswordInput)
	password2=forms.CharField(label='retype password',widget=forms.PasswordInput)

	class Meta:
		model=User
		fields=['first_name','username','email']

	def clean_password2(self):
		cd=self.cleaned_data
		if cd['password1'] != cd['password2']:
			raise forms.ValidationError("passwords don't match")
		else:
			return cd['password1']


class EditProfileForm(forms.ModelForm):

	class Meta:
		model=Profile
		fields=['user','birth_day','image']

class EditUserForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['first_name','username','email']

