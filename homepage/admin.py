'''
        
        Created By : NayanRaj Adhikary  (github : https://github.com/nayanraj210401)
                     Sameer Kasivajhula (github : https://github.com/sameerkousik)

'''

from django.contrib import admin

from .models import Courses,Mentor,ProfileEdit,Weeks,Questions,ExperimentDevelopment,PsychoQues,Blogs,ContactPersons,OurTeam,Carousel


# Register your models here.
admin.site.register(Courses)
admin.site.register(Mentor)
admin.site.register(ProfileEdit)
admin.site.register(Weeks)
admin.site.register(Questions)
admin.site.register(ExperimentDevelopment)
admin.site.register(PsychoQues)
admin.site.register(Blogs)
admin.site.register(ContactPersons)
admin.site.register(OurTeam)
admin.site.register(Carousel)

