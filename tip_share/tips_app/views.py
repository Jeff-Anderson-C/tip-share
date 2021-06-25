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
    if request.method == "GET":
        return redirect('/')
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

def logout(request):
    request.session.clear()
    return redirect('/')


# ## Dashboard 
def dashboard(request):
    # user must be logged in
    if "userid" not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    context = {
        "user": user,
    }
    return render(request, 'dashboard.html', context)
#     return HttpResponse ("This is the User Dashboard page displaying pathways to Start Pool, Open Group Chat, View Profile, and View $ History")



# ## POOL
def pool_new(request):
    # user must be logged in
    if "userid" not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    context = {
        "user": user
    }
    # return render(request, "pool_new.html")
    return HttpResponse ("User is looking to start a pool")

# def pool_create(request, pool_id):
    # user must be logged in
    # if "userid" not in request.session:
    #     return redirect('/')
#     if request.method == "GET":
#         return redirect('/')
#     if not (request.session['userid']):
#         return redirect('/')
#     user = User.objects.get(id=request.session['userid'])
#     days_tips = Tips.days_tips
#     share = 0
#     num_users = 0
#     for (user in pool): { 
#         share += User.hours_worked
#         num_users ++
#     }
#     share = share / num_users
#     for (user in pool){
#         User.share_of_tips = hours_worked * share
#     }
#     return redirect(f'/pool/{pool.id}/summary')

# def pool(request, pool_id):
    # user must be logged in
    # if "userid" not in request.session:
        # return redirect('/')
#     return HttpResponse ("Reviewing the Summary of the pool information")

# #Optional paths not on wireframe:
# #def pool_edit(request, pool_id):
# #def pool_update(request, pool_id):
# #def pool_delete(request, pool_id):


# ## GROUP CHAT    
# def groupchat(request,pool_id):
    # user must be logged in
    # if "userid" not in request.session:
    #     return redirect('/')
#     return HttpResponse ("This is the Pool Group Chat Page")
    
# def groupchat_create(request,pool_id):
    # user must be logged in
    # if "userid" not in request.session:
    #     return redirect('/')
#     return redirect(f'/pool/{pool.id}/groupchat')

# def groupchat_user(request,pool_id):
    # user must be logged in
    # if "userid" not in request.session:
    #     return redirect('/')
#     return HttpResponse ("This is another User's Profile page who is in the group chat")


    
# ## USER PROFILE
def user(request):
    # user must be logged in
    if "userid" not in request.session:
        return redirect('/')
    return HttpResponse ("User Profile Page") 

# def user_edit(request):
    # user must be logged in
    # if "userid" not in request.session:
    #     return redirect('/')
#     return HttpResponse ("This is my EDIT User Profile Page")
    
# def user_update(request):
    # user must be logged in
    # if "userid" not in request.session:
    #     return redirect('/')
#     return redirect('/user/summary')

# ## USER $$ HISTORY
def transactions(request):
    # user must be logged in
    if "userid" not in request.session:
        return redirect('/')
    return HttpResponse ("This is the Transaction History Page")

# DEVELOPMENT TOOLS
# restart database, erase all objects (for development only)
def restart(request):
    eraseUser = User.objects.all()
    eraseUser.delete()
    return redirect("/")