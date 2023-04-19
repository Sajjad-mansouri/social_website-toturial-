from django.urls import path
from . import views

urlpatterns=[
path('create/',views.image_create,name='image_create'),
path('detail/<int:id>/<slug:slug>/',views.detail,name='detail'),

]