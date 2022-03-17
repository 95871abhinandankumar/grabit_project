from dataclasses import fields
import email
from django import forms
from django.forms import ModelForm, PasswordInput
from .models import User
from django.core.validators import RegexValidator

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'roll_number', 'room_number', 'phone_number', 'email_id', 'password_field', 'image']
        error_messages = {
            'email_id': {
                    'Required':"Institute Email-id required"                
            },
        }