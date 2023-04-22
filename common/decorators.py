from django.http import HttpResponseBadRequest

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def ajax_required(function):
	def wrapper(request,*args,**kwargs):
		if not is_ajax(request):
			return HttpResponseBadRequest()
		else:
			return function(request,*args,**kwargs)

	wrapper.__doc__=function.__doc__
	wrapper.__name__=function.__name__
	return wrapper