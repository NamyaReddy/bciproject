from django.urls import path
from django.contrib import admin
from bci import views

urlpatterns=[
	
	path('home',views.home,name='home'),
	path('training',views.training,name='training'),
	path('testing',views.testing,name='testing'),
	path('testing_res',views.testing_res,name='testing_res'),
	path('results',views.results,name='results'),

]


