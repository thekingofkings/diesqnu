from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index( request ):
    template = loader.get_template("quote/index.html")
    context = RequestContext( request, {'nvg1': 'active', 'status': 'query'} )
    return HttpResponse( template.render( context ) )
    
    
def about_us( request ):
    return render( request, "quote/about-us.html", {  
            'nvg3': 'active',
            'name': 'visitor',
        })
        
        
        
def sign_up( request ):
    return render( request, "quote/sign-up.html" , {
            'nvg2': 'active',
            'status': 'showform',
        })
 
 
 
def createUser( request ):
    usrname = request.POST['usrname']
    email = request.POST['email']
    fname = request.POST['fname']
    lname = request.POST['lname']
    pwd = request.POST['pwd']
    pwdv = request.POST['pwdv']
    try:
        u = User.objects.get( username__exact = usrname )
    except User.DoesNotExist:
        if usrname == '':
            return render( request, "quote/sign-up.html", {
                'nvg2': 'active',
                'status': 'nousrname',
            })
        elif email == '':
            return render( request, "quote/sign-up.html", {
                'nvg2': 'active',
                'status': 'noemail',
            })
        elif pwd =='' or pwdv == '':
            return render( request, "quote/sign-up.html", {
                'nvg2': 'active',
                'status': 'nopwd',
            })
        elif pwd != pwdv:
            return render( request, "quote/sign-up.html", {
                'nvg2': 'active',
                'status': 'wrongpwd',
            })
        else:
            User.objects.create_user( usrname, email, pwd, first_name=fname, last_name=lname)
            return render( request, "quote/sign-up.html", {
                'nvg2': 'active',
                'status': 'success',
            })
    else:
        return render( request, "quote/sign-up.html", {
            'nvg2': 'active',
            'status': 'usrexists',
        })
    
 

 
 
def login_view( request ):
    if request.method == 'GET':
        return render( request, "quote/login.html", {
            'nvg4': 'active',
        })
    elif request.method == 'POST':
        usrname = request.POST['usrname']
        pwd = request.POST['pwd']
        u = authenticate(username=usrname, password=pwd)
        if u is not None:
            if u.is_active:
                login( request, u )
                return redirect("index")
        else:
            return render( request, "quote/login.html", {
                'nvg4': 'active',
                'status': 'failed',
            })
            
            

def logout_view( request ):
    if request.user.is_authenticated:
        logout( request )
        return redirect("index")
        
        
  
def search( request ):
    if request.method == 'POST':
        return render( request, "quote/index.html", {
            'nvg1': 'active',
            'status': 'result'
        })
    