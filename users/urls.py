from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index_View.as_view(), name='index'),
    path('register/', views.Register_View.as_view(), name='register'),
]