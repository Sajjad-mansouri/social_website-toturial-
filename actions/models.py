from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='actions')
	verb=models.CharField(max_length=100)
	target_ct=models.ForeignKey(ContentType,on_delete=models.CASCADE,blank=True,null=True,related_name='target_obj')
	target_id=models.PositiveIntegerField(null=True,blank=True)
	target=GenericForeignKey('target_ct','target_id')
	created=models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering=['-created']
		indexes = [
			models.Index(fields=["target_ct","target_id"]),

		]
	def __str__(self):
		return f'{self.user} {self.verb} {self.target}'
