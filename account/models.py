from django.db import models
from django.conf import settings

class Profile(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	birth_day=models.DateField(blank=True,null=True)
	image=models.ImageField(upload_to='users/%Y/%m/%d/')

	def __str__(self):
		return f'profile for {self.user}'
