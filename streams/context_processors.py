'''
        Spanav 0.1v
        Copyright (C) 2020 SpanavEdTech.private.limited
        
        Created By : NayanRaj Adhikary  (github : https://github.com/nayanraj210401)
                     Sameer Kasivajhula (github : https://github.com/sameerkousik)

'''

from django.shortcuts import render
from .models import ExperimentDevelopment,Stream,Branch,JobRole

def branch_processor(request):
 branches = Branch.objects.all()            
 return {'branches': branches}