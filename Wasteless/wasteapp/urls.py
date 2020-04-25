from django.urls import path

from . import views

app_name = 'wasteapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('addForm', views.addForm, name='addForm'),
    path('addNewList', views.addNewList, name='addNewList'),
    path('login', views.login, name='login')

]