'''
        Spanav 0.1v
        Copyright (C) 2020 SpanavEdTech.private.limited
        
        Created By : NayanRaj Adhikary  (github : https://github.com/nayanraj210401)
                     Sameer Kasivajhula (github : https://github.com/sameerkousik)

'''

from django.urls import path
from . import views

urlpatterns =[
    path('branch', views.branch,name="branch"),
    path('role_details', views.role_details,name="role_details"),
]