from django.shortcuts import render, redirect
from .models import *
import bcrypt

# Views the landing page. If logged in - takeds user to dash.
def index(request):
    if 'errors' not in request.session:
        request.session['errors']={}
    if 'current_user' not in request.session or not User.objects.filter(email=request.session['current_user']).exists():
        return render(request,"index.html")
    else:
        return redirect('/dashboard')

#The dash. To be filled with whatever content necessary
def dashboard(request):
    if 'current_user' not in request.session:
        return redirect('/')
    quotes = []
    for quote in Quote.objects.all():
        liked = User.objects.get(email=request.session['current_user']) in quote.liked_by.all()
        temp = {
            'quote':quote.quote,
            'author':quote.author,
            'creator':quote.creator.first_name + ' ' + quote.creator.last_name,
            'id':quote.id,
            'user_id':quote.creator.id,
            'like_count':str(quote.liked_by.all().count()),
            'liked_by_this':liked
        }
        quotes.append(temp)
    user = User.objects.get(email=request.session['current_user'])
    context = {
        'user':{
            'name':user.first_name,
            'id':user.id
        },
        'quotes':quotes
    }
    return render(request,'dashboard.html',context)

#New user handling. First user created becomes admin
def sign_up(request):
    request.session.clear()
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors):
            request.session['errors']=errors
            return redirect('/')
        else:
            #encoding password
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
            #checking if creating the first user
            if len(User.objects.all()) == 0:
                access_level = 9
            else:
                access_level = 1
            #Userbuilder and login wrapped together
            User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hashed_pw, access_level=access_level)
            request.session['current_user']=request.POST['email']
    return redirect('/dashboard')

#Login view hands password confirmation to the models
def log_in(request):
    request.session.clear()
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            request.session['errors']=errors
            return redirect('/')
        else:
            request.session['current_user']=request.POST['email']
    return redirect('/dashboard')

#render the page of individual user's quotes ONLY.
#no account info, aside from the name
def user_quotes(request,id):
    user = User.objects.get(id=id)
    quotes = user.quotes.all()
    output = []
    for quote in quotes:
        temp = {
            'author':quote.author,
            'quote':quote.quote
        }
        output.append(temp)
    context = {
        'user':{
            'name':user.first_name+' '+user.last_name
        },
        'quotes':output
    }
    return render(request,'userquotes.html',context)

#since an id is being passed on, there's probably
#a scaleable feature of admin access implied
#not doing that, but ok, run by id it is
#and users have an access_level field now,
#just in case

def account_update(request):
    request.session['errors']={}
    if request.method=="POST":
        errors = User.objects.update_validator(request.POST)
        if len(errors):
            request.session['errors']=errors
            route = '/myaccount/' + str(request.POST['id'])
            return redirect(route)
        else:
            user = User.objects.get(id=request.POST['id'])
            user.first_name=request.POST['first_name']
            user.last_name=request.POST['last_name']
            if user.email == request.session['current_user']:
                request.session['current_user']=request.POST['email']
            user.email=request.POST['email']
            user.save()

    return redirect('/dashboard')

def myaccount(request,id):
    user=User.objects.get(id=id)
    context = {
        'user':{
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            'id':id
        }
    }
    return render(request,'account_edit.html',context)

def quote_submit(request):
    if request.method=='POST':
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors):
            request.session['errors']=errors
        else:
            Quote.objects.create(author=request.POST['author'], quote=request.POST['quote'],creator=User.objects.get(email=request.session['current_user']))
    return redirect('/dashboard')

def quote_delete(request,id):
    Quote.objects.get(id=id).delete()
    return redirect('/dashboard')

#pretty self-explanatory
def log_off(request):
    request.session.clear()
    return redirect('/')

def like(request,id):
    user=User.objects.get(email=request.session['current_user'])
    quote=Quote.objects.get(id=id)
    if user in quote.liked_by.all():
        quote.liked_by.remove(user)
    else:
        quote.liked_by.add(user)
    return redirect('/dashboard')