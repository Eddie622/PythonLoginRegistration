from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('success/', views.success),
    path('process/', views.process),
    path('verify/', views.verify),
    path('logout/', views.logout),
    path('success/postMessage/', views.postMessage),
    path('success/postComment/', views.postComment),
]
