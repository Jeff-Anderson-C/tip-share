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
        "user": user,
    }
    return render(request, "pool_new.html", context)
    # return HttpResponse ("User is looking to start a pool")

# brute force pool_create, will need to refactor
def pool_create(request):
    # user must be logged in
    if "userid" not in request.session:
        return redirect('/')
    # request must be GET
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    # create instances from form data
    user1 = User.objects.get(username=request.POST['username1'])
    Hours.objects.create(
        hours_worked = 12,
        user = user1,
    )
    user2 = User.objects.get(username=request.POST['username2'])
    Hours.objects.create(
        hours_worked = request.POST['hours_worked2'],
        user = user2,
    )
    user3 = User.objects.get(username=request.POST['username3'])
    Hours.objects.create(
        hours_worked = request.POST['hours_worked3'],
        user = user3,
    )
    user4 = User.objects.get(username=request.POST['username4'])
    user4_hours = Hours.objects.create(
        hours_worked = request.POST['hours_worked4'],
        user = user4,
    )
    print("(checkpoint1) user4 workthrough:", user4_hours.hours_worked)
    pooled_tips = Tips.objects.create(
        days_tips = request.POST['total_tips'],
    )
    print("(checkpoint2) total_tips:", pooled_tips.days_tips)
    request.session["these_tips"] = pooled_tips.id
    # create pool
    new_pool = Pool.objects.create(
        pool_creator = user,
    )
    request.session['this_pool'] = new_pool.id
    this_pool = Pool.objects.get(id=request.session['this_pool'])
    print("(checkpoint3) pool ID",request.session['this_pool'])
    # add users to pool
    this_pool.pool_users.add(user1)
    this_pool.pool_users.add(user2)
    this_pool.pool_users.add(user3)
    this_pool.pool_users.add(user4)
    print("(checkpoint4) pool_users:",this_pool.pool_users.all())
    # done creating the pool with its relationships
    # begin tip share logic
    # total_hours_worked = user1.hours_worked + user2.hours_worked + user3.hours_worked + user4.hours_worked
    # share_value = 0
    # num_users = 0
    # for user in this_pool.pool_users.all():  
    #     print(user.username)
    #     print(user.hours_worked)
        # num_users +=1
        
    # share = share / num_users
    # for (user in pool){
    #     User.share_of_tips = hours_worked * share
    # }
    return redirect('/dashboard')
    # return redirect(f'/pool/{pool.id}/summary')

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
    return render(request, "profile.html")
    # return HttpResponse ("User Profile Page") 

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
    eraseUsers = User.objects.all()
    eraseUsers.delete()
    eraseHours = Hours.objects.all()
    eraseHours.delete()
    erasePools = Pool.objects.all()
    erasePools.delete()
    eraseTips = Tips.objects.all()
    eraseTips.delete()
    eraseTransactions = Transaction.objects.all()
    eraseTransactions.delete()
    return redirect("/")

# quickstart database User objects, one for each of our group
def quickstart(request):
    password = "goodpw123"
    pw_hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user1 = User.objects.create(
            first_name = "Jeff",
            last_name = "Anderson",
            email = "JA@cd.go",
            username = "Jeff",
            password = pw_hash1,
        )
    pw_hash2 = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user2 = User.objects.create(
            first_name = "Chris",
            last_name = "Joyner",
            email = "CJ@cd.go",
            username = "Chris",
            password = pw_hash2,
        )
    pw_hash3 = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user3 = User.objects.create(
            first_name = "Yuttabipool",
            last_name = "Somprasong",
            email = "Top@cd.go",
            username = "Top",
            password = pw_hash3,
        )
    pw_hash4 = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user4 = User.objects.create(
            first_name = "Cliff",
            last_name = "Hunt",
            email = "CH@cd.go",
            username = "Cliff",
            password = pw_hash4,
        )
    return redirect("/")
