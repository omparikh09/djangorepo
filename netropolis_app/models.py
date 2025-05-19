from datetime import timezone
import math
from django.db import models

# Create your models here.

"""
python manage.py makemigrations
python manage.py migrate
"""


class User(models.Model):
    email = models.EmailField(max_length=30,unique=True)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=10)
    otp = models.IntegerField(default=456)
    
    def __str__(self):
        return self.email
    
class Chairman(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)
    address = models.TextField()
    vehicle_detail = models.CharField(max_length=20)
    about_us = models.TextField()
    pic = models.FileField(upload_to="media/images", default="media/my.png")
    
    def __str__(self):
        return self.first_name
    
class Members(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)
    no_of_family_members = models.CharField(max_length=10)
    building_number = models.CharField(max_length=7) # A, B, C, D
    house_number = models.IntegerField() 
    blood_group = models.CharField(max_length=5)
    vehicle_detail = models.CharField(max_length=20)
    job_discription = models.CharField(max_length=30)
    members_type = models.CharField(max_length=10)
    about_us = models.TextField()
    pic = models.FileField(upload_to="media/images", default="media/my.png")
    aadhar_card = models.FileField(upload_to="media/doc")
    work_address = models.TextField()
    
    def __str__(self):
        return self.first_name
    
class Notice(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    Description = models.TextField()
    
    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"
    
    def __str__(self):
        return self.title
    
class Events(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    Description = models.TextField()
    pic = models.FileField(upload_to="media/images")
    
    def __str__(self):
        return self.title
    
class Complaints(models.Model):
    user_id = models.ForeignKey(Members,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField()
    status = models.CharField(max_length=30,default="OPEN")
    
    def __str__(self):
        return self.title
    
class Watchmans(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)
    watchman_experience = models.CharField(max_length=30)
    home_address = models.CharField(max_length=50)
    about_us = models.TextField()
    aadhar_card = models.FileField(upload_to="media/doc")
    pic = models.FileField(upload_to="media/images", default="media/my.png")
    
    def __str__(self):
        return self.first_name