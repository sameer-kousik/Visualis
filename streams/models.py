'''
        Spanav 0.1v
        Copyright (C) 2020 SpanavEdTech.private.limited
        
        Created By : NayanRaj Adhikary  (github : https://github.com/nayanraj210401)
                     Sameer Kasivajhula (github : https://github.com/sameerkousik)

'''

from django.db import models

# Create your models here.
class ExperimentDevelopment(models.Model):
        development = models.BooleanField(default=False)

class Stream(models.Model):
        stream_id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=20)

class Branch(models.Model):
        branch_id = models.AutoField(primary_key=True)
        stream_id = models.ForeignKey(Stream,on_delete=models.CASCADE)
        name = models.CharField(max_length=30,blank=True) #EXAMPLE: CSE
        title = models.CharField(max_length=50,blank=True) #Example: Computer Science Engineering
        def __str__(self):
            return self.name


class JobRole(models.Model):
        role_id = models.AutoField(primary_key=True)
        branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE)
        image = models.ImageField(blank=True,null=True,upload_to='pics')
        title = models.CharField(max_length=30,blank=True)
        html_enabled = models.BooleanField(default=False)
        description = models.TextField(blank=True)
        responsibilities=models.TextField()
        salary=models.TextField()
        working_hrs=models.TextField(blank=True)
        qualifications=models.TextField(blank=True)
        skills=models.TextField(blank=True)
        experience=models.TextField(blank=True)
        employer=models.TextField(blank=True)
        prospects=models.TextField(blank=True)