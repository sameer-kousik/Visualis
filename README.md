
# Visualis
This is an Django applications with PostgreSQL
=======
#  Visualis

Visualis is a Oragnisation provide brief document about the upcoming tecnologies

# Structure of the Project
 V.1:
  - Homepage 
  - JobStream
  - Courses
  - LMS
  - Blogs

## HomePage
In this page it need's to show just the lastest courses,Blog,what our users say 
  - It has some overview about the Organisation

## JobStreams
In this page it talks about the upcoming trends in the market and this page will be done as Static page and weekly updated

## Courses
In this page we need to show the Courses our Organizations is providing 

## LMS[Learning Management System]
In this basically we need to have a page to purhase the course and show the data of the Course 
 - The basic reqirement is to have a system with dynamic weeks (usually we will have 5)
 - each week will have a test with minimum criteria to pass 
 - based on all the week result we need to issue certification
> we need to make the LMS easy to use to our user 
>And So on.

## Blog 
This page need to have daily blog and this will be shown in another page


### Tech Stack 

Intially for the basic structure of project we use:

* [html] - HTML !
* [Django] - for routing 
* [Bootstrap] - great UI boilerplate
* [jQuery] - for animations
* [css] - for styling
* [js] - for some small operations
* [PostgreSQL] - for the database

### Want to Contribute

Open your favorite terminal Please Dont use CMD (no offense!!!)
install [git](https://git-scm.com/)

>Check the Green Download button and copy the https / ssl

```sh
git clone https://github.com/sameer-kousik/Visualis.git
```
 make a new Branch 
```sh
 $ git checkout -b [newbranchname]
```
to change branch 
```sh
$ git checkout [alreadycreatedbranch]
```

### Installation

Visualis requires [Django](https://www.djangoproject.com/) to run.

Install the dependencies and devDependencies and start the server.

First we need in an virtualEnv
```sh
$ source Visualis/Scripts/activate    
```
next we need to go 
```sh
$ cd Visualis
$ pip install -r requirement.txt
```
after installing all the dependences 

```sh
$ python manage.py collectstatic
```

Now We need to setup DataBase
 - this is in setting.py
>DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Visualis',
        'USER' : 'postgres',
        'PASSWORD' :'1234',
        'HOST' : 'localhost'
    }
}

Go to postgre admin and add 
| |  |
| ------ | ------ |
| database | Visualis |
| username | change as per given by use usually default : postgres |
| password | change as per given  |
| host | depends where your db is |

Now check for postgreSQL connector
- so install [pip install](https://pypi.org/project/psycopg2/)
- postgresSQL [install](https://www.postgresql.org/)
- for see all tables and other details download [pgAdmin4](https://www.pgadmin.org/download/)

After setting the database
```sh
$ python manage.py makemigrations
$ python manage.py migrate  
```



> Your Good to go

```sh
$ python manage.py runserver
```

> To run in different port
python manage.py runserver [postnumber]


