from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Image
from .forms import ImageCreateForm



@login_required
def image_create(request):
	if request.method=='POST':
		form=ImageCreateForm(request.POST)
		if form.is_valid():
			
			new_form=form.save(commit=False)
			new_form.user=request.user
			new_form.save()
			messages.success(request,'image added successfuly')
			return redirect(new_form.get_absolute_url())
	else:
		print(request.GET)
		form=ImageCreateForm(request.GET)

	return render(request,'images/create.html',{'form':form,'section':'image'})


@login_required
def detail(request,id,slug):

	image=get_object_or_404(Image,id=id,slug=slug)
	return render(request,'images/detail.html',{'image':image})