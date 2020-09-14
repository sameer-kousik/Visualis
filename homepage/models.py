'''
        Spanav 0.1v
        Copyright (C) 2020 SpanavEdTech.private.limited
        
        Created By : NayanRaj Adhikary  (github : https://github.com/nayanraj210401)
                     Sameer Kasivajhula (github : https://github.com/sameerkousik)

'''

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Mentor(models.Model):
    mentor_name = models.CharField(max_length = 30)
    description = models.TextField()
    mentor_image = models.ImageField(upload_to = 'pics')
    
    def __str__(self):
            return self.mentor_name
    
    
class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    mentor_name = models.ForeignKey(
            Mentor,on_delete=models.CASCADE
    )
    title = models.CharField(max_length = 50)
    description = models.TextField()
    html_enabled = models.BooleanField(default=False)
    course_prequesites_details = models.TextField()
    content_details = models.TextField()
    course_img = models.ImageField(upload_to = 'pics')
    overview = models.CharField(max_length = 50)
    intro = models.URLField(max_length = 730)
    no_of_weeks = models.CharField(max_length = 50)
    course_level = models.CharField(max_length = 50)
    skills = models.TextField()
    popular = models.BooleanField(default=False)
    stike_price = models.IntegerField()
    price = models.IntegerField()
    offer = models.BooleanField(default = False)
    def __str__(self):
            return self.title
    
    
class Enrollement(models.Model):
        registration_id = models.CharField(max_length = 1000,primary_key=True)
        id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
        course_id = models.ForeignKey(Courses,on_delete=models.CASCADE)
        date_of_enrollement = models.DateField(auto_now_add =True)
        date_of_completion = models.DateField(auto_now_add=False)
        token_id = models.CharField(max_length = 1000)
        
        
class ProfileEdit(models.Model):
        user = models.OneToOneField(User,on_delete=models.CASCADE)
        user_img = models.ImageField(
                upload_to = 'profileImages'
        )
        user_contact_number = models.CharField(max_length = 12)
        user_college_name = models.CharField(max_length = 50)
        user_branch_name = models.CharField(max_length = 30)
        onces = models.BooleanField(default=False)
        
      
class Weeks(models.Model):
        week_id = models.AutoField(primary_key=True)
        course_id = models.ForeignKey(Courses,on_delete=models.CASCADE)
        week_no = models.IntegerField()
        link = models.TextField(default="""<div id="extdiv">
<div  class="embed-responsive embed-responsive-16by9 ">
<iframe style="max-height: 750px;  width=40%; "  class="embed-responsive-item"  src="https://www.youtube.com/embed/Lcxm0jCgQs0" frameborder="1" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
<h2 style="margin-top:20px;">Conversion of NFA to Equivalent DFA</h2>
<p>This video instructs students on how to convert NFA into it's equivalent DFA</p>
</div>
<style>
#extdiv{
margin-left:30%;
}

@media screen and (max-width: 700px) {
  #extdiv {
padding: 0;
margin: 0;
    width: 100%;
    height: auto;

  }
}
</style> """)
        test_available = models.BooleanField(default=False)
        def __str__(self):
                mentor_name = str(self.course_id.mentor_name)
                week_no = str(self.week_id)
                course_title = str(self.course_id)
                s = str(mentor_name+' '+week_no+' '+course_title)
                return s        

class Questions(models.Model):
        question_id = models.AutoField(primary_key=True)
        week_id = models.ForeignKey(Weeks,on_delete=models.CASCADE)
        description = models.TextField()
        choice_1 = models.TextField()
        choice_2 = models.TextField()
        choice_3 = models.TextField()
        choice_4 = models.TextField()
        correct_answer = models.TextField()
        question_image = models.ImageField(blank=True,null=True,upload_to='pics')


class CourseTest(models.Model):
        registration_id = models.CharField(max_length = 1000)
        week_id = models.IntegerField()
        attempt = models.BooleanField(default=False)
        result = models.IntegerField()

class profileEditQuestions(models.Model):
        user = models.OneToOneField(User,on_delete=models.CASCADE)
        answer1 = models.TextField(max_length=1000)
        answer2 = models.TextField(max_length=1000)
        answer3 = models.TextField(max_length=1000)
        
class ExperimentDevelopment(models.Model):
        section = models.CharField(max_length = 30,blank=True)
        development = models.BooleanField(default=False)
        
        def __str__(self):
                return self.section
    
class PsychoTest(models.Model):
        user_id = models.OneToOneField(User,on_delete = models.CASCADE)
        result = models.IntegerField()
        choices = models.TextField(null=True) 

class PsychoQues(models.Model):
        question_id = models.AutoField(primary_key=True)
        description = models.TextField()
        choice_1 = models.TextField()
        choice_2 = models.TextField()
        choice_3 = models.TextField()
        choice_4 = models.TextField()
        choice_5 = models.TextField(blank=True)
        correct_answer = models.TextField()
        question_image = models.ImageField(blank=True,null=True,upload_to='pics')

class Blogs(models.Model):
        blog_title=models.CharField(max_length=20,blank=True)
        blog_img = models.ImageField(upload_to = 'pics')
        blog_desc = models.CharField(max_length=200,blank=True)
        blog_author = models.CharField(max_length=20,blank=True)
        html_enabled = models.BooleanField(default=False)
        blog_content = models.TextField(blank=True)
        

class ContactPersons(models.Model):
        contact_id = models.CharField(max_length = 50)
        name = models.CharField(max_length = 1000)
        email = models.CharField(max_length = 500)
        message_given = models.CharField(max_length = 500)
        resolved = models.BooleanField(default=False)
        def __str__(self):
            return self.contact_id
    
class OurTeam(models.Model):
        name = models.CharField(max_length = 30)
        role = models.CharField(max_length = 30)
        subtitle = models.TextField()
        facebook_link = models.CharField(max_length = 50)
        linkedin_link = models.CharField(max_length = 40)
        instagram_link = models.CharField(max_length = 30)
        image_team = models.ImageField(
                upload_to = 'OurTeam'
        )
        
        def __str__(self):
                name = str(self.name)
                s = str(name+' '+self.role)
                return s
        

class Carousel(models.Model):
        carousel_image = models.ImageField(
                upload_to = 'Carosels'
        )
        carousel_link = models.URLField(max_length = 730)
        
