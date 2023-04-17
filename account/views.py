from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
from .forms import LoginForm,RegisterForm,EditProfileForm,EditUserForm
from django.contrib.auth.models import User
from .models import Profile


def login(request):
	if request.method=='POST':
		form=LoginForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			user=authenticate(request,username=cd['username'], password=cd['password'])
			if user is not None:
				auth_login(request,user)
				return redirect('dashboard')

			else:
				messages.error(request,"username or password isn't correct!")


	form=LoginForm()
	return render(request,'account/login.html',{'form':form})


@login_required
def dashboard(request):
	return render(request,'account/dashboard.html')


def register(request):
	if request.method=='POST':
		form=RegisterForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			new_user=form.save(commit=False)
			new_user.set_password(cd['password1'])
			new_user.save()
			return redirect('login')

	

	form=RegisterForm()
	return render(request,'registration/signup.html',{'form':form})

def create_profile(request):
	if request.method=='POST':
		form=EditProfileForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request,'successfully edited')

	else:
			form=EditProfileForm()


	return render(request,'account/edit_profile.html',{'form':form})
def edit_profile(request):
	# user_instance=User.objects.get(pk=request.user.id)
	# profile_instance=Profile.objects.get(user=user_instance)
	print('before post')
	if request.method=='POST':
		profile=EditProfileForm(instance=request.user.profile,data=request.POST, files=request.FILES)
		user_form=EditUserForm(instance=request.user,data=request.POST)
		if profile.is_valid() and user_form.is_valid():
			profile.save()
			user_form.save()
			messages.success(request,'successfully edited')

	else:
			
			profile=EditProfileForm(instance=request.user.profile)
			user_form=EditUserForm(instance=request.user)
			


	return render(request,'account/edit_profile.html',{'form':profile,'user_form':user_form})