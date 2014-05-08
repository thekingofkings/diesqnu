from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from models import Record, Query
from django.http import Http404
from notify import ChangeNotify


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
        query = request.POST['querystring']
        qresult = Record.objects.filter(name__icontains=query)
        qcnt = len( qresult )
        
        # log the user's query if  user is logged in
        u = request.user
        if u.is_authenticated():
            q = Query(user=u, queryStr=query, cntRes=qcnt)
            q.save()
            # for res in qresult:
                # q.queryRes.add(res)
                
        return render( request, "quote/index.html", {
            'nvg1': 'active',
            'status': 'result',
            'query': query,
            'results': qresult,
        })
        
        
        
def query_log( request ):
    if request.user.is_authenticated():
        print request.user.username
        querylist = Query.objects.filter(user__username=request.user.username)
        return render( request, "quote/querylog.html", {
            'querylogs' : querylist,
            })
    
    
def registerQuery( request ):
    if 'queryID' in request.POST:
        try:
            qid = request.POST['queryID']
            q = Query.objects.get(id=int(qid))
        except Query.DoesNotExist:
            print "Query not exist"
            raise Http404
        else:
            q.isRegistered = True
            q.save()
            qresults = Record.objects.filter(name__icontains=q.queryStr)
            for res in qresults:
                q.queryRes.add(res)
            return redirect("querylog")
    else:
        raise Http404
        

def unregisterQuery( request, queryID ):
    try:
        q = Query.objects.get(id=queryID)
    except Query.DoesNotExist:
        print "Query", queryID, "does not exist"
        raise Http404
    else:
        q.isRegistered = False
        q.save()
        return redirect("querylog")
        
        
def notify( request ):
    u = request.user
    querySet = Query.objects.filter(user__id=u.id, isRegistered=True)
    email = u.email
    for query in querySet:
        newRes = Record.objects.filter(name__icontains=query)
        oldRes = query.queryRes.all()
        if len(newRes) != len(oldRes):
            notifier = ChangeNotify()
            notifier.sendToOneAddress(email, "Your query has new results")
    return redirect("querylog")