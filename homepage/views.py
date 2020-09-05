'''
        Spanav 0.1v
        Copyright (C) 2020 SpanavEdTech.private.limited
        
        Created By : NayanRaj Adhikary  (github : https://github.com/nayanraj210401)
                     Sameer Kasivajhula (github : https://github.com/sameerkousik)

'''
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import Courses,ProfileEdit,Enrollement,Weeks,CourseTest,Questions,profileEditQuestions,ExperimentDevelopment,PsychoQues,PsychoTest,Blogs,ContactPersons,OurTeam,Carousel
from django.contrib.auth.decorators import login_required
import random,datetime
import itertools
import json
from ratelimit.decorators import ratelimit
from django.core.mail import EmailMessage
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template import RequestContext


# this is to handle the 404 http error as this is a custom 404 page 
def error_404(request,exception):
    return render(request,'404.html')


# this is a index that is referr to /
''' This is uses Models : Courses --> to show the our courses
    Blogs --> used to render the images in homepage with on click goes to the link
    all_val --> used in the Carousel indicator to count the iterations
'''
def index(request):
    what_user_say = "whatusersay"
    courses = Courses.objects.filter(popular = True)
    blogs = Blogs.objects.all().reverse()
    current_user = request.user
    carousels = Carousel.objects.all()
    all_val = len(carousels)
    ver = ExperimentDevelopment.objects.filter(section = what_user_say).exists()
    context = {
            'blogs' : blogs,
            'courses' : courses,
            'current_user' : current_user,
            'carousels' : carousels,
            'allVal' : all_val,
            'Experiment' : ver
        }
    return render(request,'index.html',context)
    
    
# This is handle the register of the user in the database
'''
Models : 
    User -- > this is the Default auth_user table by django
    this function is implemented with also the validation those includes 
        - password and confirm password are equal 
        - same email aren't allowed 
        - password 8 digit is not implemented x
'''
def register(request):
    if(request.method == 'POST'):
       first_name = request.POST['first_name']
       last_name = request.POST['last_name']
       username = request.POST['username']
       password1 = request.POST['password1']
       password2 = request.POST['password2']
       email = request.POST['email'] 
       if(password1 == password2):
           if(User.objects.filter(username = username).exists()):
               messages.info(request,"Username Exists")
               return render(request,'login-signup.html')
           elif(User.objects.filter(email = email).exists()):
               messages.info(request,"email Taken taken")
               return render(request,'login-signup.html')
           else:
               user = User.objects.create_user(username = username , password = password1,email = email,first_name = first_name,last_name = last_name)
               user.save()
               user = auth.authenticate(username = username,password = password1)
               auth.login(request,user)
               return redirect("/")
       else:
           messages.info(request,"Password aren't matching !!")
           return redirect("register")
    else:
        return render(request,'login-signup.html')
    
    
# This is handle with the login details this is allow the user to access the Courses 
'''
    required : POST (for validations) GET (fetches login-signup.html)
    models:
        This Uses the User --> ie the auth_user table by django
        This function is used to login the users 
        The validations included are 
            - user login into the application 
'''
def login(request):
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       user = auth.authenticate(username = username,password = password)
       if(user is not None):
           auth.login(request,user)
           return redirect('/')
       else:
           messages.info(request,"Invaid Credentials")
           
    elif request.method == 'GET' and 'course_id' in request.GET:
        course_id = request.GET['course_id']
        if(course_id is not None and course_id != ' '):
            request.META.get('HTTP_REFERER')
    else:
        return render(request,'login-signup.html')
    return render(request,'login-signup.html')


# This is a Simple function the name itself explain it all
def logout(request):
    auth.logout(request)
    return redirect('/')



# This is Basically the Course-details 
'''
 required : POST (for validations) 
 models used :
    -- Enrollement , Courses 

The Basic function is 
    if not logined in -
            redirect to login
    
    if logged in 
        show the price of the courses and lnked with the purchas gateway
        
    if logged in and purchased course
        linked with the lms system
        
'''
def courses_all(request):
    if(request.method == 'POST'):
        course_id = request.POST['course_id']
        title = request.POST['course_title']
        user = request.user
        checkout_enrolled_course = Enrollement.objects.filter(id = user.id ,course_id = course_id).exists();
        # print(checkout_enrolled_course)
        try:
            courses = Courses.objects.get(course_id = course_id,title = title)
        except ObjectDoesNotExist:
                return HttpResponse(status = 404)
        
        if checkout_enrolled_course :
            enrolle  = Enrollement.objects.get(id = user.id ,course_id = course_id)
            # print(enrolle.registration_id)
            return render(request,'course-details.html',{'courses' : courses,'checkout_enrolled_course' : checkout_enrolled_course , 'registration_id' : enrolle.registration_id })
        return render(request,'course-details.html',{'courses' : courses , 'checkout_enrolled_course' : checkout_enrolled_course})
    else:
        return HttpResponse(status = 404)



# This are the blogs which are displayed 
'''
    required : POST (need the blogs_id for the Identifing the Blogs)
Models :
    Blogs
'''
def blog(request):
    if request.method == 'POST':
        blog_id = request.POST['blog_id']
        blog = Blogs.objects.get(id=blog_id)
        context={
            'blog':blog
        }
        return render(request,'blog.html',context)
    else:
        return HttpResponse(status = 404)


# this is the Myprofile page
'''
requirement : POST(user_id) -- > to Indentify the user
    Models 
        -User 
        -ProfileEditQuestions
        -ProfileEdit
        -Enrollement
The Basic Function of this function is to show all the info of the user
'''
@login_required
def profile(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
    # print(user_id)
        user = User.objects.get(id = user_id)
        current_user = request.user
        ver = profileEditQuestions.objects.filter(user = current_user).exists()
        profile = None
        ver_profile_edit = ProfileEdit.objects.filter(user = current_user).exists()
        if(ver_profile_edit):
            profile = ProfileEdit.objects.get(user = current_user)
        else:
            profile = "-"
        if(not ver):
            prof = {'answer1' : "click on the Button to Edit",
                'answer2' : "click on the Button to Edit",
                'answer3' : "click on the Button to Edit",
                }
            id_user = User.objects.get(id = user_id)
            if Enrollement.objects.filter(id = id_user).exists():
                enrolle = Enrollement.objects.filter(id = id_user)
        # for i in enrolle:
        #     print(i.course_id)
        # for i in enrolle:
        #     print(i.registration_id)
                return render(request,'profile.html',{'profile' : profile, 'enrolle' : enrolle,'prof' : prof})
            else:
                return render(request,'profile.html',{'profile' : profile,'prof' : prof})
    
        else:
            prof = profileEditQuestions.objects.get(user = current_user)
            id_user = User.objects.get(id = user_id)
            if Enrollement.objects.filter(id = id_user).exists():
                enrolle = Enrollement.objects.filter(id = id_user)
        # for i in enrolle:
        #     print(i.course_id)
        # for i in enrolle:
        #     print(i.registration_id)
                return render(request,'profile.html',{'profile' : profile, 'enrolle' : enrolle,'prof' : prof})
            else:
                return render(request,'profile.html',{'profile' : profile,'prof' : prof})
        return render(request,'profile.html',{'profile' : profile,'prof' : prof})
    else:
        return HttpResponse(status = 404)



# This is function profile used to make changes of his/her informantion in our database
'''
    requirement : POST (user_id,college_name,brach_name,contact)
    models
        -User 
        -ProfileEdit
        -ProfileEditQuestions
    
'''
@login_required
def editProfile(request):
    if(request.method == 'POST'):
        user_id = request.POST['user_id']
        college_name = request.POST['college_name']
        branch_name = request.POST['branch_name']
        contact = request.POST['contact']
        # print(contact)
        current_user = request.user
        ver = ProfileEdit.objects.filter(user = current_user).exists()
        if(ver):
            profile_val = ProfileEdit.objects.filter(user = current_user).update(user_contact_number = contact,user_college_name = college_name,user_branch_name =branch_name)
            profile = ProfileEdit.objects.get(user = current_user)
            ver_prof = profileEditQuestions.objects.filter(user = current_user).exists()
            prof = None
            if(ver_prof):
                prof = profileEditQuestions.objects.get(user = current_user)
            else:
                prof = {'answer1' : "Click to edit button to edit", 'answer2': "Click to edit button to edit" ,'answer3' : "Click to edit button to edit"}
            return render(request,'profile.html',{'user' : current_user, 'profile' : profile,'prof' : prof})
        else:
            profile = ProfileEdit(user = current_user,user_img = 'deafult.jpg' ,user_college_name = college_name,user_branch_name = branch_name,user_contact_number = contact,onces = True)
            profile.save()
            return render(request,'profile.html',{'user' : current_user, 'profile' : profile })
    elif (request.method == 'GET'):
        user_id = request.GET['user']
        current_user = request.user
        ver_profile = ProfileEdit.objects.filter(user = current_user).exists()
        profile = None
        if ver_profile:
            profile = ProfileEdit.objects.get(user = current_user)
        else:
            profile = "-"
        return render(request,'editProfile.html',{'user':current_user,'profile' : profile})




# This is functions used for payment gateway purchased
'''
requirement : POST (id,course_id)
models 
    -User
    -Enrollement

This functions basically generate an random 16bit alpanumeric string which refered as registrations id here after in LMS
'''
@login_required
def purchased(request):
    if request.method == 'POST':
        user_id = request.POST['id']
        course_id = request.POST['course_id']   
        id_user = User.objects.get(id = user_id)
        id_course = Courses.objects.get(course_id = course_id)
    # if not Enrollement.objects.filter(id=id_user,course_id = id_course).exists():
    #     enrolle = Enrollement(registration_id = registration_id,id = id_user,course_id = id_course,token_id = token_id,date_of_completion = None)
    #     return render(request,'purchase.html',{'enrolle' : enrolle})
    # else:
        if  Enrollement.objects.filter(id = id_user,course_id = id_course).exists():
            enrolle = Enrollement.objects.get(id = id_user,course_id = course_id)
            return render(request,'purchase.html',{'enrolle' : enrolle})
        else: 
            registration_id = '%32x' % random.getrandbits(16*8)
            token_id = '%8x' % random.getrandbits(16*8)
            d_o_c = datetime.date(1972,10,11)
            enrolle = Enrollement(registration_id = registration_id,id = id_user,course_id = id_course,token_id = token_id,date_of_completion = d_o_c)
            enrolle.save()
            return render(request,'purchase.html',{'enrolle' : enrolle})
    else:
        return HttpResponse(status = 404)
 
 
    
# This is the LMS functions is used to show all information 
'''
requirement : POST(registrations_id)
models:
    -Enrollement
    -Courses
    -Weeks
'''
@login_required
def lms(request):
    # course_tit = request.POST['course_title']
    if request.method == 'POST':
        registration_id = request.POST['registration_id']
        enrolle = Enrollement.objects.get(registration_id = registration_id)
    # print(enrolle.course_id.course_id)
        course = Courses.objects.get(course_id = enrolle.course_id.course_id)
        weeks = Weeks.objects.filter(course_id = enrolle.course_id.course_id)
        return render(request,'lms.html',{'weeks' : weeks,'course':course, 'registration_id':registration_id})
    else:
        return HttpResponse(status = 404)



# This is the allCourses page shows all the courses availble in our website
'''
requirement : GET 
    models 
        - Courses
'''
def render_all_courses_page(request):
    courses = Courses.objects.all()
    return render(request,'allCourses.html',{'courses' : courses})



# This is the allBlogs page as the name suggest
'''
requriments : GET
    models 
        -ExperimentDevelopment
        -Blogs
'''
def allBlogs(request):
    val = 'Blogs'
    dev = ExperimentDevelopment.objects.filter(section = val).exists()
    # print(dev)
    res = False
    if dev:
        val =  ExperimentDevelopment.objects.get(section = val)
        res = val.development
    # print(res)
    blogs = Blogs.objects.all().reverse()
    context={
        'blogs':blogs,
        'development':res
    }
    return render(request,'blogs.html',context)



# This is the test module/functions this is used for test in LMS page
'''
requirement : POST(requriment_id,week_id)
models
    -Enrollement
    -CourseTest
    -Questions
'''
@login_required
def test(request):
    if request.method == 'POST':
        registration_id = request.POST['registration_id']
        week_id = request.POST['week_id']
        st = ""
        num=0
        enrol = Enrollement.objects.get(registration_id=registration_id)
        test = CourseTest.objects.filter(registration_id=enrol.registration_id,week_id=week_id)
        if(test.exists()):
            st = "You've Already Taken This Test"
            test_info = CourseTest.objects.get(registration_id=enrol.registration_id,week_id=week_id)
            return render(request,'test.html',{'st':st ,'test_info' : test_info})
        else:
            num=1
            questions = Questions.objects.filter(week_id=week_id)
            context={
                'questions':questions,
                'registration_id':enrol.registration_id,
                'week_id':week_id,
                'num':num
            }
            return render(request,'test.html',context)
    else:
        return HttpResponse(status = 404)
    
    
    
# This is the psychometric Test module/Function
'''
requirement : GET (works when only your logged in) otherwise httpresponse 404
models 
    -PsychoTest
    -PsychoQues
'''
@login_required 
def psychotest(request):
    user = request.user
    user_id = user.id
    test = PsychoTest.objects.filter(user_id=user_id)
    num=0
    st=""
    ver_user = user.is_authenticated
    if ver_user:
        if(test.exists()):
            test = PsychoTest.objects.get(user_id=user_id)
            questions = PsychoQues.objects.all()
            correct = PsychoQues.objects.all().values_list('correct_answer',flat=True)
            corr = list(correct)
            coN = test.result
            jsonDec = json.decoder.JSONDecoder()
            choices=  jsonDec.decode(test.choices)
            anslist = zip(questions, corr, choices)
            coN = test.result
            context= {
            'anslist':anslist,
            'answers':corr,
            'choices':choices,
            'coN':coN
            }
            return render(request,'calc.html',context)
        else:
            questions = PsychoQues.objects.all()
            num=1
            context={
            'num':num,
            'questions':questions,
            'user_id':user_id
            }
            return render(request,'psycho.html',context)
    else:
        return redirect('/login')
    
    
# This is Test Calcution function / module Used for the result of the user
'''
requriment : POST (answers,week_id)
models:
    -Enrollement
    -Questions
    -CourseTest
'''
@login_required
def calc(request):
    answers = request.POST['answers']
    week_id = request.POST['week_id']
    registration_id = request.POST['registration_id']
    enrol = Enrollement.objects.get(registration_id=registration_id)
    test = CourseTest.objects.filter(registration_id=enrol.registration_id,week_id=week_id)
    if(test.exists()):
        st = "You've Already Taken This Test"
        test_info = CourseTest.objects.get(registration_id=enrol.registration_id,week_id=week_id)   
        return render(request,'test.html',{'st':st ,'test_info' : test_info})
    enrol = Enrollement.objects.get(registration_id = registration_id)
    ques = Questions.objects.filter(week_id=week_id)
    correct = Questions.objects.filter(week_id=week_id).values_list('correct_answer',flat=True)
    corr = list(correct)
    choices = [x for x in answers.split(',')]
    if(len(choices)!=len(corr)):
        return render(request,'wrong.html')
    coN=0
    for i in range(len(corr)):
        if(corr[i]==choices[i]):
            coN+=1
    test_attempt = CourseTest(registration_id=registration_id,week_id=week_id,attempt=True,result=coN)
    test_attempt.save()
    anslist = zip(ques, corr, choices)
    context= {
        'anslist':anslist,
        'answers':corr,
        'choices':choices,
        'coN':coN
    }
    return render(request,'calc.html',context)
  
  
# This is Calculation function for PsychoTest function
'''
requirement : POST(answers)
models:
    -PsychoQues
    -PsychoTest
'''
@login_required   
def calcpsych(request):
    user = request.user
    user_id = user.id
    test = PsychoTest.objects.filter(user_id=user_id)
    num=0
    st=""
    if(test.exists()):
        test = PsychoTest.objects.get(user_id=user_id)
        questions = PsychoQues.objects.all()
        correct = PsychoQues.objects.all().values_list('correct_answer',flat=True)
        corr = list(correct)
        coN = test.result
        jsonDec = json.decoder.JSONDecoder()
        choices=  jsonDec.decode(test.choices)
        anslist = zip(questions, corr, choices)
        coN = test.result
        context= {
            'anslist':anslist,
            'answers':corr,
            'choices':choices,
            'coN':coN
        }
        return render(request,'calc.html',context)
    answers = request.POST['answers']
    questions = PsychoQues.objects.all()
    user = request.user
    user_id = user.id
    correct = PsychoQues.objects.all().values_list('correct_answer',flat=True)
    corr = list(correct)
    choices = [x for x in answers.split(',')]
    coN=0
    if(len(choices)!=len(corr)):
        return render(request,'wrong.html')
    for i in range(len(corr)):
        if(corr[i]==choices[i]):
            coN+=1
    test_attempt = PsychoTest(user_id=user,result=coN,choices=json.dumps(choices))
    test_attempt.save()
    anslist = zip(questions, corr, choices)
    context= {
        'anslist':anslist,
        'answers':corr,
        'choices':choices,
        'coN':coN
    }
    return render(request,'calc.html',context)
  
# This is the AboutUs page 
'''
requirement : GET (NONE)
 models:
    -OurTeam
'''
def about(request):
    ourTeams = OurTeam.objects.all()
    return render(request,'about-us.html',{'ourTeams' : ourTeams})



# This is the EditProfile for tabular Questions
''''
requriment : POST (question_number,Answer) Or GET(question)
models:
    -profileEditQuestions
    -Enrollement
    -ProfileEdit
'''
@login_required
def edit_tab_profile(request):
    if(request.method == 'GET'):
        question_number = request.GET['question']
        current_user = request.user
        question_number = int(question_number)
        if(question_number == 1):
            question_val = "What Programming Skill?"
            ver = profileEditQuestions.objects.filter(user = current_user).exists()
            if(ver):
                answer = profileEditQuestions.objects.get(user = current_user)
                return  render(request,'edit-tab-profile.html',{'question_val' : question_val,'question_number' : question_number ,'answer' : answer})
            answer = {  'answer1' : "",
                        'answer2' : "",
                        'answer3' : ""
                       }
            return render(request,'edit-tab-profile.html',{'question_val' : question_val,'question_number' : question_number ,'answer' : answer})
        elif(question_number == 2):
            question_val = "What are your aim?"
            ver = profileEditQuestions.objects.filter(user = current_user).exists()
            if(ver):
                answer = profileEditQuestions.objects.get(user = current_user)
                return  render(request,'edit-tab-profile.html',{'question_val' : question_val,'question_number' : question_number ,'answer' : answer})
            answer = {  'answer1' : "",
                        'answer2' : "",
                        'answer3' : ""
                       }
            return render(request,'edit-tab-profile.html',{'question_val' : question_val,'question_number' : question_number  ,'answer' : answer})
        elif(question_number == 3):
            question_val = "What are cerifications Have you Done?"
            ver = profileEditQuestions.objects.filter(user = current_user).exists()
            if(ver):
                answer = profileEditQuestions.objects.get(user = current_user)
                return  render(request,'edit-tab-profile.html',{'question_val' : question_val,'question_number' : question_number ,'answer' : answer})
            answer = {  'answer1' : "",
                        'answer2' : "",
                        'answer3' : ""
                       }
            return render(request,'edit-tab-profile.html',{'question_val' : question_val,'question_number' : question_number  ,'answer' : answer})
    elif (request.method == 'POST'):  
        question_number = request.POST['question_number']
        answer_real = request.POST['Answer']
        current_user = request.user
        question_number = int(question_number)
        ver = profileEditQuestions.objects.filter(user = current_user).exists()
        # print(ver)
        if(ver):
            if(question_number == 1):
                to_update = profileEditQuestions.objects.filter(user = current_user).update(answer1 = answer_real)
            elif(question_number == 2):
                to_update = profileEditQuestions.objects.filter(user = current_user).update(answer2 = answer_real)
            elif(question_number == 3):
                to_update = profileEditQuestions.objects.filter(user = current_user).update(answer3 = answer_real)
        else:
            # print(question_number)
            if(question_number == 1):
                print(answer_real)
                pro = profileEditQuestions(user = current_user,answer1 = answer_real,answer2 = " ",answer3 = " ")
                pro.save()
            elif(question_number == 2):
                pro = profileEditQuestions(user = current_user,answer1 = " ",answer2 = answer_real,answer3 = " ")
                pro.save()
            elif(question_number == 3):
                pro = profileEditQuestions(user = current_user,answer1 = " ",answer2 = " ",answer3 = answer_real)
                pro.save()
        ver_profile_edit_val = ProfileEdit.objects.filter(user = current_user).exists()
        profile = None
        if(ver_profile_edit_val):
            profile = ProfileEdit.objects.get(user = current_user)
        else:
            profile = "-"
        # print(profile)
        id_user = User.objects.get(id = current_user.id)
        prof = profileEditQuestions.objects.get(user = current_user)
        if Enrollement.objects.filter(id = id_user).exists():
            enrolle = Enrollement.objects.filter(id = id_user)
        # for i in enrolle:
        #     print(i.course_id)
        # for i in enrolle:
        #     print(i.registration_id)
            # print(prof.answer1)
            return render(request,'profile.html',{'profile' : profile, 'enrolle' : enrolle,'prof' : prof})
    else:
        return render(request,'profile.html',{'profile' : profile,'prof' : prof})
    
    return render(request,'profile.html',{'profile' : profile,'prof' : prof})



# This is a 3rd Party API which is used that the email is real or not
'''
requirement : Email(xyz@domainname)
'''
def validateEmail(email):
    import requests as req
    try:
        response = req.get("https://isitarealemail.com/api/email/validate",
        params = {'email': email})
    except Exception:
        return False
    res = response.json()['status']
    res = str(res)
    ver = res in ['valid',"Valid","valid"]
    if ver:
        return True
    return False


# This is Contact us at the Bottom of the Page The ratelimit with 10 Request per IP address
'''
requriment : GET (name,email,message) also gives csrf_token
models:
    -ContactPersons
'''
@ratelimit(key='ip', rate='10/m')
def contactQuery(request):
    name = request.GET['name']
    email = request.GET['email']
    msg = request.GET['message']
    verfied = validateEmail(email)
    # print(verfied)
    if verfied:
        current_user = request.user
        contact_id = '%8x' % random.getrandbits(16*8)
        contact = ContactPersons(contact_id = contact_id,name = name,email = email,message_given = msg,resolved = False)
        ver_contact = ContactPersons.objects.filter(email = email).exists()
        if ver_contact:
            contact = ContactPersons.objects.filter(email = email)
            return render(request,'Query.html',{'contact' : contact, 'contact_ver' : True})
        else:
            contact.save()
            send_email = EmailMessage(
            subject='Acknowledged:'+name,
            body= 'Your message has been received, \nThis is your contact_id is:'+contact_id+
            '\nFor futher Queries email us at support@spanavedtech.com',
                to=[email])
            send_email.send()
            return render(request,'Query.html',{'contact' : contact , 'contact_ver' : False})  
    else:   
        return HttpResponse(status = 404)
