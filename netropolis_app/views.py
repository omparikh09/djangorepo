from django.shortcuts import render
from .utils import *
from .models import *
import random
from django.core.mail import send_mail
# Create your views here.
def login(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Chairman':  
            cid = Chairman.objects.get(user_id = uid)
            
            mcount = Members.objects.all().count()
            ncount = Notice.objects.all().count()
            ecount = Events.objects.all().count()
            context = {
                'uid' : uid,
                'cid' : cid,
                'mcount' : mcount,
                'ncount' : ncount,
                'ecount' : ecount,
            }    
            return render(request,"netropolis_app/index.html",context)
    else:
        if request.POST:
            try:
                email = request.POST['email']
                password = request.POST['password']
                
                print("---->>>> EMAIL",email)
                print("---> Submit Button Press")
                
                uid = User.objects.get(email = email)
                if uid:
                    print("::::: Email Match :::::")
                    if uid.password == password:
                        if uid.role == "Chairman":
                            request.session["email"] = email #store Email in Session
                            print("::::: Valid Login :::::")
                            cid = Chairman.objects.get(user_id = uid)
                            context = {
                                'uid' : uid,
                                'cid' : cid,
                            }
                            return render(request,"netropolis_app/index.html",context)
                        elif uid.role == "Members":
                            request.session["email"] = email
                            
                            mid = Members.objects.get(user_id = uid)
                            context = {
                                'uid' : uid,
                                'mid' : mid,
                            }
                            return render(request,"netropolis_app/member-index.html",context)
                        print("::::: Valid Login :::::")
                        return render(request,"netropolis_app/index.html")
                    else:
                        e_msg = "invalid password"
                        return render(request,"netropolis_app/login.html",{'e_msg' : e_msg})
            except Exception as e:
                print(":::::::::: Exception ::::::::::",e)
                e_msg = "Invalid Email"
                return render(request,"netropolis_app/login.html",{'e_msg' : e_msg})
        else:
            print("---> Only Page Referesh")
        return render(request,"netropolis_app/login.html")

def home(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Chairman':
            cid = Chairman.objects.get(user_id = uid)
            
            mcount = Members.objects.all().count()
            ncount = Notice.objects.all().count()
            ecount = Events.objects.all().count()
            context = {
                'uid' : uid,
                'cid' : cid,
                'mcount' : mcount,
                'ncount' : ncount,
                'ecount' : ecount,
            }    
            return render(request,"netropolis_app/index.html",context)
    else:
        return render(request,"netropolis_app/login.html")
    
def logout(request):
    if "email" in request.session:
        del request.session["email"]
        return render(request,"netropolis_app/login.html")
    else:
        return render(request,"netropolis_app/login.html")
    
def profile(request):
    if "email" in request.session:
        if request.POST:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Chairman':
                cid = Chairman.objects.get(user_id = uid)
                
                cid.first_name = request.POST['first_name']
                cid.last_name = request.POST['last_name']
                cid.contact_number = request.POST['contact_number']
                cid.vehicle_detail = request.POST['vehicle_detail']
                
                if "pic" in request.FILES:
                    cid.pic = request.FILES['pic']
                    
                cid.about_us = request.POST['about_us']
                    
                cid.address = request.POST['address']
                
                cid.save()
                
                context = {
                    'uid' : uid,
                    'cid' : cid,
                }    
                return render(request,"netropolis_app/profile.html",context)
        else:        
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Chairman':
                cid = Chairman.objects.get(user_id = uid)
                context = {
                    'uid' : uid,
                    'cid' : cid,
                }    
                return render(request,"netropolis_app/profile.html",context)
    else:
        return render(request,"netropolis_app/profile.html")

def chairman_password(request):
    if "email" in request.session:
        if request.POST:
            uid = User.objects.get(email = request.session['email'])
            currentpassword = request.POST['currentpassword']
            newpassword = request.POST['newpassword']
            if uid.password == currentpassword:
                uid.password = newpassword
                uid.save()
                s_msg = "Successfully Password Reset"
                del request.session["email"]
                return render(request,"netropolis_app/login.html",{'s_msg':s_msg})
            else:
                e_msg = "Invalid Current Password"
                del request.session["email"]
                return render(request,"netropolis_app/login.html",{'e_msg':e_msg})
        else:
            return render(request,"netropolis_app/login.html")

def add_society_member(request):
    if 'email' in request.session:
        if request.POST:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Chairman':
                cid = Chairman.objects.get(user_id = uid) 
                
                email = request.POST['email']
                contact_number = request.POST['contact_number']
                
                # first_name = request.POST['first_name']
                # last_name = request.POST['last_name']
                # no_of_family_members = request.POST['no_of_family_members']
                # building_number = request.POST['building_number'] # A, B, C, D
                # house_number = request.POST['house_number'] 
                # blood_group = request.POST['blood_group']
                # vehicle_detail = request.POST['vehicle_detail']
                # job_discription = request.POST['job_discription']
                # members_type = request.POST['members_type']
                # pic = request.FILES['pic']
                # aadhar_card = request.FILES['aadhar_card']
                # work_address = request.POST['work_address']
                       
                l1 = ['D543DW9W4', 'BN92N8A85B', 'L0VEY0U02', '0OPSNQ542N', 'PD893DA', 'SW462VKL', 'GHL052FB']
                
                generatedPassword = random.choice(l1)+email[2:4]+contact_number[3:7]       
                
                user = User.objects.create(email = email, password = generatedPassword, role = "Member")
                if user:
                    mid = Members.objects.create(user_id = user,
                                                first_name = request.POST['first_name'],
                                                last_name = request.POST['last_name'],
                                                no_of_family_members = request.POST['no_of_family_members'],
                                                building_number = request.POST['building_number'] ,# A, B, C, D
                                                house_number = request.POST['house_number'] ,
                                                blood_group = request.POST['blood_group'],
                                                vehicle_detail = request.POST['vehicle_detail'],
                                                job_discription = request.POST['job_discription'],
                                                members_type = request.POST['members_type'],
                                                pic = request.FILES['pic'],
                                                aadhar_card = request.FILES['aadhar_card'],
                                                work_address = request.POST['work_address'],
                                                )
                    
                    if mid:
                        s_msg = "Society Member Added Successfully !!! "
                        context = {
                            'uid' : uid,
                            'cid' : cid,
                            's_msg' : s_msg,
                        }
                        return render(request,"netropolis_app/add_society_member.html",context)    
        else:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Chairman':
                cid = Chairman.objects.get(user_id = uid)
                context = {
                    'uid' : uid,
                    'cid' : cid,
                }
                return render(request,"netropolis_app/add_society_member.html",context)
    else:
        return render(request,"netropolis_app/login.html")

def all_members(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Chairman':
            cid = Chairman.objects.get(user_id = uid)
            
            mall = Members.objects.all()
            
            for i in mall:
                print("--->>>",i)
            
            context = {
                'uid' : uid,
                'cid' : cid,
                'mall' : mall,
            }    
            return render(request,"netropolis_app/members.html",context)

def view_members(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Chairman':
            cid = Chairman.objects.get(user_id = uid)
            mid = Members.objects.get(id=pk)
            context = {
                'uid' : uid,
                'cid' : cid,
                'mid' : mid,
            }    
            return render(request,"netropolis_app/member_spacific_profile.html",context)
        
def delete_member(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Chairman':
            cid = Chairman.objects.get(user_id = uid)
            mid = Members.objects.get(id=pk)
            
            member_user_id = User.objects.get(id = mid.user_id.id)
            mid.delete()
            member_user_id.delete()
            
            mall =Members.objects.all()
            
            context = {
                'uid' : uid,
                'cid' : cid,
                'mall' : mall,
            }    
            return render(request,"netropolis_app/members.html",context)
        
def add_notice(request):
    if "email" in request.session:
        if request.POST:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Chairman':
                cid = Chairman.objects.get(user_id = uid)
                
                title = request.POST['title']
                Description = request.POST['Description']
                
                nid = Notice.objects.create(user_id = uid, title = title, Description = Description)
                
                if nid:
                    s_msg = "Succssfully Notice Added !"
                    context = {
                        'uid' : uid,
                        'cid' : cid,
                        's_msg' : s_msg,
                    }    
                    return render(request,"netropolis_app/add-notice.html",context)
        else:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Chairman':
                cid = Chairman.objects.get(user_id = uid)
                context = {
                    'uid' : uid,
                    'cid' : cid,

                }    
                return render(request,"netropolis_app/add-notice.html",context)
            
def all_notice(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Chairman':
            cid = Chairman.objects.get(user_id = uid)
            
            nall = Notice.objects.all()
            
            context = {
                'uid' : uid,
                'cid' : cid,
                'nall' : nall,
            }    
            return render(request,"netropolis_app/notice-list.html",context)
        
def delete_notice(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Chairman':
            cid = Chairman.objects.get(user_id = uid)
            
            nid = Notice.objects.get(id=pk)
            nid.delete()
            
            nall = Notice.objects.all()
            
            context = {
                'uid' : uid,
                'cid' : cid,
                'nall' : nall,
            }    
            return render(request,"netropolis_app/notice-list.html",context)

def add_events(request):
    if "email" in request.session:
        if request.POST:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Chairman':
                cid = Chairman.objects.get(user_id = uid)
                
                title = request.POST['title']
                Description = request.POST['Description']
                pic = request.FILES['pic']
                
                eid = Events.objects.create(user_id = uid, title = title, Description = Description,pic = pic)
                
                if eid:
                    s_msg = "Succssfully Notice Added !"
                    context = {
                        'uid' : uid,
                        'cid' : cid,
                        's_msg' : s_msg,
                    }    
                    return render(request,"netropolis_app/add-events.html",context)
        else:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Chairman':
                cid = Chairman.objects.get(user_id = uid)
                context = {
                    'uid' : uid,
                    'cid' : cid,

                }    
                return render(request,"netropolis_app/add-events.html",context)

def events_list(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Chairman':
            cid = Chairman.objects.get(user_id = uid)
            
            eall = Events.objects.all()
            
            context = {
                'uid' : uid,
                'cid' : cid,
                'eall' : eall,
            }    
            return render(request,"netropolis_app/events-list.html",context)            
            
def complaints_list(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Chairman':
            cid = Chairman.objects.get(user_id = uid)
            
            call = Complaints.objects.all()
            
            context = {
                'uid' : uid,
                'cid' : cid,
                'call' : call,
            }    
            return render(request,"netropolis_app/complaints-list.html",context)

def forgot_password(request):
    if request.POST:
        try:
            print("--->>> On send otp button Clicked")
            otp = random.randint(1000,9999)
            email = request.POST['email']
            uid = User.objects.get(email = email)
            
            uid.otp = otp 
            uid.save()
            
            if uid:
                sendMyCustomMail("Forgot Password","mail-templates",email,{'otp': otp})
                context = {
                    'email' : email
                }
                return render(request,"netropolis_app/reset-password.html",context)
        except Exception as e:
            print("--------------------",e)
            context = {
                'e_msg' : "Email address incorrect !!"
            }
            return render(request,"netropolis_app/forgot-password.html",context)
    else:
        return render(request,"netropolis_app/forgot-password.html")    

def reset_password(request):
    if request.POST:
        email = request.POST['email']
        otp = request.POST['otp']
        newpassword = request.POST['newpassword']
        repassword = request.POST['repassword']
        
        uid = User.objects.get(email = email)
        if str(uid.otp) == otp:
            if newpassword == repassword:
                uid.password = newpassword
                uid.save()
                context = {
                    's_msg' : "Password Reset Successfully !!"
                }
                return render(request,"netropolis_app/login.html",context)
            else:
                context = {
                    'email' : email,
                    'e_msg' : "Password does not match !"
                }
                return render(request,"netropolis_app/reset-password.html",context)
        else:
            context = {
                'email' : email,
                'e_msg' : "Invalid OTP !!"
            }
            return render(request,"netropolis_app/reset-password.html",context)

def register(request):
    return render(request,"netropolis_app/register.html")

# For Society Members 

def member_login(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Members':  
            mid = Members.objects.get(user_id = uid)
            context = {
                'uid' : uid,
                'mid' : mid,
            }    
            return render(request,"netropolis_app/member-index.html",context)
    else:
        if request.POST:
            try:
                email = request.POST['email']
                password = request.POST['password']
                
                print("---->>>> EMAIL",email)
                print("---> Submit Button Press")
                
                uid = User.objects.get(email = email)
                if uid:
                    print("::::: Email Match :::::")
                    if uid.password == password:
                        if uid.role == "Members":
                            request.session["email"] = email
                            
                            mid = Members.objects.get(user_id = uid)
                            context = {
                                'uid' : uid,
                                'mid' : mid,
                            }
                            return render(request,"netropolis_app/member-index.html",context)
                        print("::::: Valid Login :::::")
                        return render(request,"netropolis_app/member-index.html")
                    else:
                        e_msg = "invalid password"
                        return render(request,"netropolis_app/member-login.html",{'e_msg' : e_msg})
            except Exception as e:
                print(":::::::::: Exception ::::::::::",e)
                e_msg = "Invalid Email"
                return render(request,"netropolis_app/member-login.html",{'e_msg' : e_msg})
        else:
            print("---> Only Page Referesh")
        return render(request,"netropolis_app/member-login.html")

def member_profile(request):
    if "email" in request.session:
        if request.POST:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Members':
                mid = Members.objects.get(user_id = uid)
                
                mid.first_name = request.POST['first_name']
                mid.last_name = request.POST['last_name']
                mid.contact_number = request.POST['contact_number']
                mid.vehicle_detail = request.POST['vehicle_detail']
                mid.no_of_family_members = request.POST['no_of_family_members']
                mid.building_number = request.POST['building_number']
                mid.house_number = request.POST['house_number']
                mid.blood_group = request.POST['blood_group']
                mid.job_discription = request.POST['job_discription']
                mid.members_type = request.POST['members_type']
                
                if "pic" in request.FILES:
                    mid.pic = request.FILES['pic']
                if "aadhar_card" in request.FILES:
                    mid.aadhar_card = request.FILES['aadhar_card']
                
                mid.about_us = request.POST['about_us']
                
                mid.work_address = request.POST['work_address']
                
                mid.save()
                
                context = {
                    'uid' : uid,
                    'mid' : mid,
                }    
                return render(request,"netropolis_app/member-profile.html",context)
        else:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Members':
                mid = Members.objects.get(user_id = uid)
                context = {
                    'uid' : uid,
                    'mid' : mid,
                }    
                return render(request,"netropolis_app/member-profile.html",context)
    else:
        return render(request,"netropolis_app/member-profile.html")     

def member_home(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Members':
            mid = Members.objects.get(user_id = uid)
            context = {
                'uid' : uid,
                'mid' : mid,
            }    
            return render(request,"netropolis_app/member-index.html",context)
    else:
        return render(request,"netropolis_app/member-login.html")
    
def member_password(request):
    if "email" in request.session:
        if request.POST:
            uid = User.objects.get(email = request.session['email'])
            currentpassword = request.POST['currentpassword']
            newpassword = request.POST['newpassword']
            if uid.password == currentpassword:
                uid.password = newpassword
                uid.save()
                s_msg = "Successfully Password Reset"
                del request.session["email"]
                return render(request,"netropolis_app/member-login.html",{'s_msg':s_msg})
            else:
                e_msg = "Invalid Current Password"
                del request.session["email"]
                return render(request,"netropolis_app/member-login.html",{'e_msg':e_msg})
        else:
            return render(request,"netropolis_app/member-login.html")
        
def member_views_all_member(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Members':
            mid = Members.objects.get(user_id = uid)
            
            mall = Members.objects.all()
            
            for i in mall:
                print("--->>>",i)
            
            context = {
                'uid' : uid,
                'mid' : mid,
                'mall' : mall,
            }    
            return render(request,"netropolis_app/all_members.html",context)
    
def view_all_member(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Members':
            mid = Members.objects.get(id=pk)
            context = {
                'uid' : uid,
                'mid' : mid,
            }    
            return render(request,"netropolis_app/all_member_spacific_profile.html",context)
        
def member_view_all_notice(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Members':
            mid = Members.objects.get(user_id = uid)
            
            nall = Notice.objects.all()
            
            context = {
                'uid' : uid,
                'mid' : mid,
                'nall' : nall,
            }    
            return render(request,"netropolis_app/member-view-notice-list.html",context)

def events_list_member(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Members':
            cid = Members.objects.get(user_id = uid)
            
            eall = Events.objects.all()
            
            context = {
                'uid' : uid,
                'cid' : cid,
                'eall' : eall,
            }    
            return render(request,"netropolis_app/events-list-member.html",context) 
        
def add_personal_event(request):  
    if "email" in request.session:
        if request.POST:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Members':
                mid = Members.objects.get(user_id = uid)
                
                title = request.POST['title']
                Description = request.POST['Description']
                pic = request.FILES['pic']
                
                eid = Events.objects.create(user_id = uid, title = title, Description = Description,pic = pic)
                
                if eid:
                    s_msg = "Succssfully Notice Added !"
                    context = {
                        'uid' : uid,
                        'mid' : mid,
                        's_msg' : s_msg,
                    }    
                    return render(request,"netropolis_app/add-personal-event.html",context)
        else:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Members':
                mid = Members.objects.get(user_id = uid)
                context = {
                    'uid' : uid,
                    'mid' : mid,

                }    
                return render(request,"netropolis_app/add-personal-event.html",context)
            
def add_complaints(request):
    if "email" in request.session:
        if request.POST:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Members':
                mid = Members.objects.get(user_id = uid)
                
                title = request.POST['title']
                description = request.POST['Description']
                
                cid = Complaints.objects.create(user_id = mid, title = title, description = description)
                
                if cid:
                    s_msg = "Succssfully Complaints Added !"
                    context = {
                        'uid' : uid,
                        'mid' : mid,
                        's_msg' : s_msg,
                    }    
                    return render(request,"netropolis_app/add-complaints.html",context)
        else:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Members':
                mid = Members.objects.get(user_id = uid)
                context = {
                    'uid' : uid,
                    'mid' : mid,    
                }    
                return render(request,"netropolis_app/add-complaints.html",context)
            
def member_complaints_list(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Members':
            cid = Members.objects.get(user_id = uid)
            
            call = Complaints.objects.all()
            
            context = {
                'uid' : uid,
                'cid' : cid,
                'call' : call,
            }    
            return render(request,"netropolis_app/member-view-complaints-list.html",context) 

# For Society Watchman

def watchman_login(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Watchmans':  
            wid = Watchmans.objects.get(user_id = uid)
            context = {
                'uid' : uid,
                'wid' : wid,
            }    
            return render(request,"netropolis_app/watchman-index.html",context)
    else:
        if request.POST:
            try:
                email = request.POST['email']
                password = request.POST['password']
                
                print("---->>>> EMAIL",email)
                print("---> Submit Button Press")
                
                uid = User.objects.get(email = email)
                if uid:
                    print("::::: Email Match :::::")
                    if uid.password == password:
                        if uid.role == "Watchmans":
                            request.session["email"] = email
                            
                            wid = Watchmans.objects.get(user_id = uid)
                            context = {
                                'uid' : uid,
                                'wid' : wid,
                            }
                            return render(request,"netropolis_app/watchman-index.html",context)
                        print("::::: Valid Login :::::")
                        return render(request,"netropolis_app/watchman-index.html")
                    else:
                        e_msg = "invalid password"
                        return render(request,"netropolis_app/watchman-login.html",{'e_msg' : e_msg})
            except Exception as e:
                print(":::::::::: Exception ::::::::::",e)
                e_msg = "Invalid Email"
                return render(request,"netropolis_app/watchman-login.html",{'e_msg' : e_msg})
        else:
            print("---> Only Page Referesh")
        return render(request,"netropolis_app/watchman-login.html")
    
def watchman_home(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Watchmans':
            wid = Watchmans.objects.get(user_id = uid)
            context = {
                'uid' : uid,
                'wid' : wid,
            }    
            return render(request,"netropolis_app/watchman-index.html",context)
    else:
        return render(request,"netropolis_app/watchman-login.html")
    
def watchman_profile(request):
    
    if "email" in request.session:
        if request.POST:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Watchmans':
                wid = Watchmans.objects.get(user_id = uid)
                
                wid.first_name = request.POST['first_name']
                wid.last_name = request.POST['last_name']
                wid.contact_number = request.POST['contact_number']
                wid.watchman_experience = request.POST['watchman_experience']
                
                if "pic" in request.FILES:
                    wid.pic = request.FILES['pic']
                if "aadhar_card" in request.FILES:
                    wid.aadhar_card = request.FILES['aadhar_card']
                
                wid.about_us = request.POST['about_us']
                
                wid.home_address = request.POST['home_address']
                
                wid.save()
                
                context = {
                    'uid' : uid,
                    'wid' : wid,
                }    
                return render(request,"netropolis_app/watchman-profile.html",context)
        else:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'Watchmans':
                wid = Watchmans.objects.get(user_id = uid)
                context = {
                    'uid' : uid,
                    'wid' : wid,
                }    
                return render(request,"netropolis_app/watchman-profile.html",context)
    else:
        return render(request,"netropolis_app/watchman-profile.html")  
    
def watchman_views_all_member(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'Watchmans':
            mid = Watchmans.objects.get(user_id = uid)
            
            mall = Members.objects.all()
            
            for i in mall:
                print("--->>>",i)
            
            context = {
                'uid' : uid,
                'mid' : mid,
                'mall' : mall,
            }    
            return render(request,"netropolis_app/watchman_views_all_members.html",context)
