from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Image
from .forms import ImageCreateForm
from common.decorators import ajax_required


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

@ajax_required
@login_required
@require_POST
def like(request):
	image_id=request.POST.get('id')
	action=request.POST.get('action')
	
	if id and action:
		try:
			image=Image.objects.get(id=image_id)

			user=request.user
			if action == 'like':
				image.like_image.add(request.user)
				
			else:
				image.like_image.remove(request.user)
				
			return JsonResponse({'status':'ok'})
		except:
			pass
	return JsonResponse({'status':'error'})