from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
from urllib import request
from .models import Image

class ImageCreateForm(forms.ModelForm):

	class Meta:
		model=Image
		fields=['title','url','description']
		widgets = {
			'url': forms.HiddenInput,
		}


	def clean_url(self):
		url=self.cleaned_data['url']
		extension=url.rsplit('.',1)[1]
		valid_extenstion=['jpg','png']
		if extension not in valid_extenstion:
			raise ValidationError("this given url does't match valid image extension ")

		return url

	def save(self,force_insert=False,force_update=False,commit=True):
		image=super().save(commit=False)
		url=self.cleaned_data['url']
		extension=url.rsplit('.',1)[1]
		name=slugify(self.cleaned_data['title'])
		image_name=f'{name}.{extension}'
		response=request.urlopen(url)
		image.image.save(image_name,ContentFile(response.read()),save=False)
		if commit:
			image.save()

		return image