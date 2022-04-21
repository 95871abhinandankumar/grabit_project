from secrets import choice
from django import forms
from django.db import models
from django.dispatch import receiver
from django.forms import EmailField, IntegerField, PasswordInput
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(models.Model):
    is_active = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image = models.ImageField(
        upload_to='usersImages', blank=True)
    roll_number = models.IntegerField()
    room_number = models.IntegerField()
    phone_number = PhoneNumberField(null=True)
    email_id = models.EmailField()
    password_field = models.CharField(max_length=10, blank=False)
    rating = models.FloatField(default=0)
    
class UserChat(models.Model):
    message = models.CharField(max_length=100)
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    message_date_time = models.DateTimeField()
    


class Product(models.Model):
    item_name = models.CharField(max_length=50)
    price = models.FloatField()
    owner = models.IntegerField(null=True)
    buyer = models.IntegerField(null=True)
    # item available means true
    item_availablity = models.BooleanField(default=True)
    category = models.CharField(max_length=20)
    item_description = models.CharField(max_length=500)
    
    image1 = models.ImageField(
        upload_to='productImages', blank=False)
    
    image2 = models.ImageField(
        upload_to='productImages', blank=True)
    
    image3 = models.ImageField(
        upload_to='productImages', blank=True)
    
    image4 = models.ImageField(
        upload_to='productImages', blank=True)
    

class Advertisement(models.Model):
    ad_date_time = models.DateTimeField()
    product_id = models.IntegerField(null=False)
    choice_mark = models.BooleanField(default=False)
    ad_likes = models.IntegerField()
    ad_dislikes = models.IntegerField()

# class Likes(models.Model):
#     user_id = models.IntegerField(null=False)
#     item_id = models.IntegerField(null=False)
    
    
    
    
    