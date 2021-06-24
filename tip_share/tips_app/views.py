from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

## REGISTER / LOG IN ##
def index(request):
    #return render(request, 'login.html')
    return render(request, 'login.html')
    # return HttpResponse ("This is the loging/register page")

# def register(request):
#     return redirect('/dashboard')
def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST ['first_name'],
            last_name = request.POST ['last_name'],
            email = request.POST ['email'],
            username = request.POST ['username'],
            password = pw_hash,
        )
        request.session['userid'] = new_user.id 
        return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:    
        user = User.objects.filter(username = request.POST['username'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id 
                return redirect('/dashboard')
            else:
                messages.error(request, 'Invalid password')
            return redirect('/')
        return redirect('/')
#     return redirect('/dashboard')

# def logout(request):
#     request.session.clear()
#     return redirect('/')


# ## Dashboard 
def dashboard(request):
    return render(request, 'dashboard.html')
#     return HttpResponse ("This is the User Dashboard page displaying pathways to Start Pool, Open Group Chat, View Profile, and View $ History")



# ## POOL
# def pool_new(request):
#     return HttpResponse ("User is looking to start a pool")

# def pool_create(request, pool_id):
#     return redirect(f'/pool/{pool.id}/summary')

# def pool(request, pool_id):
#     return HttpResponse ("Reviewing the Summary of the pool information")

# #Optional paths not on wireframe:
# #def pool_edit(request, pool_id):
# #def pool_update(request, pool_id):
# #def pool_delete(request, pool_id):


# ## GROUP CHAT    
# def groupchat(request,pool_id):
#     return HttpResponse ("This is the Pool Group Chat Page")
    
# def groupchat_create(request,pool_id):
#     return redirect(f'/pool/{pool.id}/groupchat')

# def groupchat_user(request,pool_id):
#     return HttpResponse ("This is another User's Profile page who is in the group chat")


    
# ## USER PROFILE
# def user(request):
#     return HttpResponse ("User Profile Page") 

# def user_edit(request):
#     return HttpResponse ("This is my EDIT User Profile Page")
    
# def user_update(request):
#     return redirect('/user/summary')

# ## USER $$ HISTORY
# def transaction(request):
#     return HttpResponse ("This is the Transaction History Page")
    