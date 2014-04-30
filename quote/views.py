from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User


# Create your views here.
def index( request ):
    template = loader.get_template("quote/index.html")
    context = RequestContext( request, {'nvg1': 'active'} )
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
    