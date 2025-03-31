from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('result', views.result, name='result'),
    path('second_page', views.second_page, name='second_page'),
    path('third_page', views.third_page, name='third_page')
]
