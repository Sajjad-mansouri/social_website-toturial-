from django.urls import path
from . import views

urlpatterns=[
path('',views.image_list,name='image-list'),
path('create/',views.image_create,name='image_create'),
path('detail/<int:id>/<slug:slug>/',views.detail,name='detail'),
path('detail/like/',views.like,name='like')

]