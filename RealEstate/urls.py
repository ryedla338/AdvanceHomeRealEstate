from django.urls import path
from . import views
from django.contrib.auth.mixins import LoginRequiredMixin

urlpatterns = [
    path('', views.index, name='index'),
]
