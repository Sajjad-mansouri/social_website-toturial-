from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from .models import Image


@receiver(m2m_changed,sender=Image.like_image.through)
def user_like_change(sender,instance,**kwargs):
	instance.total_likes=instance.like_image.count()
	instance.save()