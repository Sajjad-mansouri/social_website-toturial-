from django.contrib.contenttypes.models import ContentType
import datetime
from django.utils import timezone
from .models import Action


def create_action(user,verb,target=None):
	now=timezone.now()
	last_minute=now-datetime.timedelta(minutes=1)

	similar_actions=Action.objects.filter(user_id=user.id,verb=verb,created__gte=last_minute)
	if target:
		
		target_ct=ContentType.objects.get_for_model(target)
		similar_actions=similar_actions.filter(target_ct=target_ct,target_id=target.id)
		
	if not similar_actions:
		action=Action(user=user,target=target,verb=verb)
		action.save()
	return False