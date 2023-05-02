from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .models import Image
from .forms import ImageCreateForm
from common.decorators import ajax_required,is_ajax
from actions.utils import create_action


@login_required
def image_create(request):
	if request.method=='POST':
		form=ImageCreateForm(request.POST)
		if form.is_valid():
			
			new_form=form.save(commit=False)
			new_form.user=request.user
			new_form.save()
			create_action(request.user,'bookmarked_image',new_form)
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
				create_action(request.user,'likes',image)
				
			else:
				image.like_image.remove(request.user)
				
			return JsonResponse({'status':'ok'})
		except:
			pass
	return JsonResponse({'status':'error'})



@login_required
def image_list(request):
	images=Image.objects.all()
	#popularity_image=Image.objects.order_by('-total_likes')
	paginator=Paginator(images,2)
	page_num=request.GET.get('page')
	page_obj=paginator.get_page(page_num)
	
	try:
			number = paginator.validate_number(page_num)
	except PageNotAnInteger:
			number = 1
	except EmptyPage:
			if is_ajax(request):
				return HttpResponse('')
	if is_ajax(request):
		return render(request,'images/list_ajax.html',{'page_obj':page_obj})

	return render(request,'images/list.html',{'page_obj':page_obj})