from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

## REGISTER / LOG IN ##
def index(request):
    #return render(request, 'login.html')
    return HttpResponse ("This is the loging/register page")

def register(request):
    return redirect('/dashboard')

def login(request):
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')


## Dashboard 
def dashboard(request):
    return HttpResponse ("This is the User Dashboard page displaying pathways to Start Pool, Open Group Chat, View Profile, and View $ History")



## POOL
def pool_new(request):
    return HttpResponse ("User is looking to start a pool")

def pool_create(request, pool_id):
    return redirect(f'/pool/{pool.id}/summary')

def pool(request, pool_id):
    return HttpResponse ("Reviewing the Summary of the pool information")

#Optional paths not on wireframe:
#def pool_edit(request, pool_id):
#def pool_update(request, pool_id):
#def pool_delete(request, pool_id):


## GROUP CHAT    
def groupchat(request,pool_id):
    return HttpResponse ("This is the Pool Group Chat Page")
    
def groupchat_create(request,pool_id):
    return redirect(f'/pool/{pool.id}/groupchat')

def groupchat_user(request,pool_id):
    return HttpResponse ("This is another User's Profile page who is in the group chat")


    
## USER PROFILE
def user(request):
    return HttpResponse ("User Profile Page") 

def user_edit(request):
    return HttpResponse ("This is my EDIT User Profile Page")
    
def user_update(request):
    return redirect('/user/summary')

## USER $$ HISTORY
def transaction(request):
    return HttpResponse ("This is the Transaction History Page")
    

