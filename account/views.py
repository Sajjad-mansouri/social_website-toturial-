from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
from .forms import LoginForm


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
