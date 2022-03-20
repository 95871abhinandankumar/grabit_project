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
    
class UserChat(models.Model):
    message = models.CharField(max_length=100)
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    message_date_time = models.DateTimeField()
    
        