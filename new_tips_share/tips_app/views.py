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
            restaurant = request.POST ['restaurant'],
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
    return render(request, "pool.html", context)
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
    users = [None, None, None, None]
    if request.POST['username1']:
        users[0] = request.POST['username1']
    if request.POST['username2']:
        users[1] = request.POST['username2']
    if request.POST['username3']:
        users[2] = request.POST['username3']
    if request.POST['username4']:
        users[3] = request.POST['username4']
    # create instances from form data
    creator = User.objects.get(id= request.session ['userid'])
    
    u1 = User.objects.get(username=request.POST['username1'])
    u2 = User.objects.get(username=request.POST['username2']) 
    u3 = User.objects.get(username=request.POST['username3'])  
    u4 = User.objects.get(username=request.POST['username4']) 
    
    new_pool = Pool.objects.create (
        total_tips = request.POST['total_tips'], 
        total_hours = request.POST['total_hours'], 
        pool_creator = creator, 
    )
    a=request.POST['total_tips']
    b=request.POST['total_hours']
    tip_hour = (int(a) / int(b))
    y=0
    x=[None, None, None, None]
    for i in users:
        x[y]=User.objects.filter(username=user)
        y+=1

    u1 = User.objects.get(username=request.POST['username1'])
    u2 = User.objects.get(username=request.POST['username2']) 
    u3 = User.objects.get(username=request.POST['username3'])  
    u4 = User.objects.get(username=request.POST['username4'])  

    u1.pool_groups.add(new_pool)
    u2.pool_groups.add(new_pool)
    u3.pool_groups.add(new_pool)
    u4.pool_groups.add(new_pool)

    q=request.POST['1']
    u1t = Transaction.objects.create (
        sender = creator,
        hours_worked = request.POST['1'],
        tips_shared = (int(q) * int(tip_hour))
    )
    u1.transactions_recieved.add(u1t)

    q=request.POST['2']   
    u2t = Transaction.objects.create (
        sender = creator,
        hours_worked = request.POST['2'],
        tips_shared = (int(q) * int(tip_hour))
    )
    u2.transactions_recieved.add(u2t)

    q=request.POST['3']
    u3t = Transaction.objects.create (
        sender = creator,
        hours_worked = request.POST['3'],
        tips_shared = (int(q) * int(tip_hour))
    )
    u3.transactions_recieved.add(u3t)

    q=request.POST['4']
    u4t = Transaction.objects.create (
        sender = creator,
        hours_worked = request.POST['4'],
        tips_shared = (int(q) * int(tip_hour))
    )

    u4.transactions_recieved.add(u4t)
    return render(request, 'summary.html', {'new_pool':new_pool, 'u1':u1, 'u2':u2, 'u3':u3, 'u4':u4, 'u1t':u1t, 'u2t':u2t, 'u3t':u3t, 'u4t':u4t})



def search_users(request):
    return render(request, 'search_users.html')


def search_profile(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        users = User.objects.filter(username__contains=searched)
        return render(request,'profile_find.html', 
        {'searched':searched, 'users':users})
    else:
        return render(request,'profile_find.html', 
        {})

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
    user = User.objects.get(id=request.session['userid']) 
    user_trans = user.transactions_recieved.all()   
    return render(request, "profile.html", {'user':user, 'user_trans':user_trans})
    # return HttpResponse ("User Profile Page") 

def other_profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'other_profile.html', {'user':user})

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
    user = User.objects.get(id=request.session['userid'])
    user_trans = user.transactions_recieved.all() 
    # name = user
    # user_trans = Transaction.objects.filter(recipients__contains=searched)
    if "userid" not in request.session:
        return redirect('/')
    return render (request, "history.html", {'user':user, 'user_trans':user_trans})

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
