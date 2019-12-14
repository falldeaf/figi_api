"""figi_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
	#index
	path('', views.index, name='index'),

	#Static html front end to collect bonds
	path('cusip_search/', views.cusip_search, name='search'),

	#API to Add new bonds by cusip value as CSV string
	path('add/', views.add, name='add'),

	#JSON API to return bonds, flag for Municipal only
	path('get_bonds/<int:muni>/<int:json>', views.get_bonds, name='get')
]
