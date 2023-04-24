from django.db import models
from django.utils.text import slugify
from django.urls import reverse_lazy,reverse
from django.conf import settings
class Image(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='images_created',on_delete=models.CASCADE)
	title=models.CharField(max_length=50)
	slug=models.SlugField(max_length=50)
	url=models.URLField()
	image=models.ImageField(upload_to='images/%Y/%m/%d')
	description=models.TextField()
	created=models.DateTimeField(auto_now_add=True,db_index=True)
	like_image=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='images_liked',blank=True)

	def __str__(self):
		return self.title

	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=slugify(self.title)

		return super().save(*args,**kwargs)


	def get_absolute_url(self):
		return reverse('detail',args=[self.id,self.slug])
