from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class Profile(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
	birth_day=models.DateField(blank=True,null=True)
	image=models.ImageField(upload_to='users/%Y/%m/%d/')

	def __str__(self):
		return f'profile for {self.user}'


class Contact(models.Model):
	user_from=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='rel_from')
	following=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='rel_to')
	created=models.DateTimeField(auto_now_add=True,db_index=True)

	class Meta:
		ordering=['-created']
	def __str__(self):
		return f'{self.user_from} follow {self.following}'




user_model=get_user_model()
user_model.add_to_class('following',models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False))