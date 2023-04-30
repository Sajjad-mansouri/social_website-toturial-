from django.contrib import admin
from .models import Action
# Register your models here.
class ActionAdmin(admin.ModelAdmin):
	list_display=['user','verb','target_ct','target_id']
	search_fields=['verb']
	list_filter=['created']


admin.site.register(Action,ActionAdmin)