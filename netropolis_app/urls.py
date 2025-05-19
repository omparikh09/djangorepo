"""
URL configuration for netropolis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # For Chairman Part
    
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('chairman-password/',views.chairman_password, name='chairman-password'),
    path('add-society-member/',views.add_society_member, name='add-society-member'),
    path('all-members',views.all_members, name='all-members'),
    path('view-members/<int:pk>',views.view_members, name='view-members'),
    path('delete-member/<int:pk>',views.delete_member, name='delete-member'),
    path('add-notice/',views.add_notice, name='add-notice'),
    path('notice-list/', views.all_notice, name='notice-list'),
    path('delete-notice/<int:pk>', views.delete_notice, name='delete-notice'),
    path('add-events/', views.add_events, name='add-events'),
    path('events-list/', views.events_list, name='events-list'),
    path('complaints-list/', views.complaints_list, name='complaints-list'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/', views.reset_password, name='reset-password'),
    
    # For Members Part
    path('member-login/', views.member_login, name='member-login'),
    path('member-home/', views.member_home, name='member-home'),
    path('member-profile/', views.member_profile, name='member-profile'),
    path('member-password/', views.member_password, name='member-password'),
    path('member-views-all-member/', views.member_views_all_member, name='member-views-all-member'),
    path('view-all-member/<int:pk>', views.view_all_member, name='view-all-member'),
    path('member-view-notice-list/', views.member_view_all_notice, name='member-view-notice-list'),
    path('events-list-member/', views.events_list_member, name='events-list-member'),
    path('add-personal-event/', views.add_personal_event, name='add-personal-event'),
    path('add-complaints/', views.add_complaints, name='add-complaints'),
    path('member-complaints-list/', views.member_complaints_list ,name='member-complaints-list'),
    
    # For Society Watchman Part
    path('watchman-login/', views.watchman_login, name='watchman-login'),
    path('watchman-home/', views.watchman_home, name='watchman-home'),
    path('watchman-profile/', views.watchman_profile, name='watchman-profile'),
    path('watchman-views-all-member/', views.watchman_views_all_member, name='watchman-views-all-member'),
]