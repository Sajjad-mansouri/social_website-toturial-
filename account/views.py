from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import F
from django.http import JsonResponse
from django.db import connection
from .forms import LoginForm,RegisterForm,EditProfileForm,EditUserForm
from django.contrib.auth.models import User
from .models import Profile,Contact
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action


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

	

	actions=Action.objects.exclude(user=request.user)
	following_ids=request.user.following.values_list('id',flat=True)

	if following_ids:
		actions=actions.filter(user_id__in=following_ids,user__following__created__lt=F('created'))
		actions=actions.select_related('user__profile').prefetch_related('target')[:10]
	else:
		actions=None
	
	
	return render(request,'account/dashboard.html',{'actions':actions})


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


@login_required
def create_profile(request):
	if request.method=='POST':
		form=EditProfileForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			form.save()
			create_action(request.user,'create profile')
			messages.success(request,'successfully edited')

	else:
			form=EditProfileForm()


	return render(request,'account/edit_profile.html',{'form':form})

	
@login_required	
def edit_profile(request):
	# user_instance=User.objects.get(pk=request.user.id)
	# profile_instance=Profile.objects.get(user=user_instance)
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



@login_required	
def user_list(request):
	users=User.objects.filter(is_active=True)
	return render(request,'account/user/user_list.html',{'users':users})

@login_required	
def user_detail(request,username):
	account_user=get_object_or_404(User,username=username)
	return render(request,'account/user/user_detail.html',{'account_user':account_user})

@ajax_required
@require_POST
@login_required
def user_follow(request):
	active_user=request.user
	following_username=request.POST.get('username')
	try:
			following=User.objects.get(username=following_username)
			if following.username not in active_user.following.values_list('username',flat=True):
				Contact.objects.create(user_from=active_user,following=following)
				create_action(request.user,'follow',following)
				return JsonResponse({'status':'ok','action':'follow'})
			else:
				active_user.following.remove(following)
				create_action(request.user,'follow',following)
				
				return JsonResponse({'status':'ok','action':'unfollow'})
	except User.DoesNotExist:
		return JsonResponse({'status':'error'})
	

