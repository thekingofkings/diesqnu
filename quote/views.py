from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


# Create your views here.
def index( request ):
    template = loader.get_template("quote/index.html")
    context = RequestContext( request )
    return HttpResponse( template.render( context ) )
    
    
    
def about_us( request ):
    return render( request, "quote/about-us.html", {  
            'nvg3': 'active',
            'name': 'visitor',
        })
        
def sign_up( request ):
    return render( request, "quote/sign-up.html" )