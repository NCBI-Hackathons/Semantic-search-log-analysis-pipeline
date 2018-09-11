from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('instructions-status.html', views.instructions, name='instructions'),
    path('fuzzyVetter', views.vetter, name='vetter'),
]
