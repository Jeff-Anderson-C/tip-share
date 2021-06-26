from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), #localhost:8000
    path('register', views.register), #call to action = (C2A)
    path('login', views.login), #C2A
    
    # #dashboard - 4 paths (Pool, Group Chat, User Profile, User $ history)
    path('dashboard', views.dashboard), #localhost:8000/dashboard
    path('logout', views.logout),#C2A
    
    # ## POOL
    path('pool/start', views.pool_new), #localhost:8000/pool/start
    path('pool/create', views.pool_create), #C2A
    # path('pool/<int:pool_id>/summary', views.pool), #localhost:8000/pool/3/summary

    # #Optional paths not on wireframe:
    # #path('pool/<int:pool_id>/edit',views.pool_edit), #localhost:8000/pool/3/edit
    # #path('pool/<int:pool_id>/delete',views.pool_delete), #C2A
    # #path('pool/<int:pool_id>/update', views.pool_update), #C2A

    # ## GROUP CHAT
    # path('pool/<int:pool_id>/groupchat', views.groupchat), #localhost:8000/pool/3/groupchat
    # path('pool/<int:pool_id>/groupchat/create', views.groupchat_create), #C2A
    # path('pool/<int:pool_id>/groupchat/user_<int:otherprofile_id>', views.groupchat_user), #localhost:8000/pool/3/groupchat/user_5

    
    # ## USER PROFILE
    path('user/summary', views.user), #localhost:8000/user/summary
    # path('user/edit',views.user_edit), #localhost:8000/user/edit
    # path('user/update', views.user_update), #C2A
    
    # ## USER $$ HISTORY 
    path('transactions/history', views.transactions), #localhost:8000/transaction/history

    #develop tool "restart", erase all database objects (for development only)
    path("restart", views.restart),
    #develop tool "quickstart", create group members' database objects (for development only)
    path("quickstart", views.quickstart),
    
]