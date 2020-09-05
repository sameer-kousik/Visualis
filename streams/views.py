'''
        Spanav 0.1v
        Copyright (C) 2020 SpanavEdTech.private.limited
        
        Created By : NayanRaj Adhikary  (github : https://github.com/nayanraj210401)
                     Sameer Kasivajhula (github : https://github.com/sameerkousik)

'''


from django.shortcuts import render
from .models import ExperimentDevelopment,Stream,Branch,JobRole
# Create your views here.

def branch(request):
    branch_id = request.POST['branch_id']
    branch = Branch.objects.get(branch_id=branch_id)
    roles = JobRole.objects.filter(branch_id=branch_id)
    context={
        'branch':branch,
        'roles':roles
    }
    return render(request,'branch.html',context)

def role_details(request):
    role_id = request.POST['role_id']
    role = JobRole.objects.get(role_id=role_id)
    context={
        'role':role
    }
    return render(request,'role_details.html',context)

def cse(request):
    dev = ExperimentDevelopment.objects.all()
    return render(request,'cse.html',{'development' : dev})

def ece(request):
    dev = ExperimentDevelopment.objects.all()
    return render(request,'ece.html',{'development' : dev})

def mech(request):
    dev = ExperimentDevelopment.objects.all()
    return render(request,'mech.html',{'development' : dev})

def it(request):
    dev = ExperimentDevelopment.objects.all()
    return render(request,'it.html',{'development' : dev})

def che(request):
    dev = ExperimentDevelopment.objects.all()
    return render(request,'che.html',{'development' : dev})