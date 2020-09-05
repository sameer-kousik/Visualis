'''
        Spanav 0.1v
        Copyright (C) 2020 SpanavEdTech.private.limited
        
        Created By : NayanRaj Adhikary  (github : https://github.com/nayanraj210401)
                     Sameer Kasivajhula (github : https://github.com/sameerkousik)

'''

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('',views.index,name = "index"),
    path('register',views.register,name = "register"),
    path('login',views.login,name = "login"),
    path('logout',views.logout,name ="logout"),
    path('courses',views.courses_all,name="courses"),
    path('profile',views.profile,name = 'profile'),
    path('purchased',views.purchased,name = 'purchased'),
    path('lms',views.lms,name = 'lms'),
    path('test',views.test,name='test'),
    path('calc',views.calc,name='calc'),
    path('allCourses',views.render_all_courses_page,name = "render_all_courses_page"),
    path('reset_password',auth_views.PasswordResetView.as_view(template_name = "reset_password_dir/password_reset.html"),name ="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name = "reset_password_dir/password_reset_sent.html"),name = "password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = "reset_password_dir/password_reset_form.html"),name = "password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name = "reset_password_dir/password_reset_done.html"),name = "password_reset_complete"),
    path('allBlogs',views.allBlogs,name = "allBlogs"),
    path('about',views.about,name = "about"),
    path('editProfile',views.editProfile,name = "editProfile"),
    path('editQuestions',views.edit_tab_profile,name = "edit_tab_profile"),
    path('psychotest',views.psychotest,name="psychotest"),
    path('calcpsych',views.calcpsych,name="calcpsych"),
    path('contactQuery',views.contactQuery,name = "contactQuery"),
    path('blog',views.blog,name="blog")

]