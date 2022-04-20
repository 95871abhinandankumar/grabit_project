from dataclasses import fields
import email
from django import forms

from .models import User
from django.core.validators import RegexValidator

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields = ['first_name', 'last_name', 'roll_number', 'room_number', 'phone_number', 'email_id', 'password_field', 'image']
        widgets={
            'password_field' : forms.PasswordInput(),
        }
        error_messages = {
            'email_id': {
                    'Required':"Institute Email-id required"                
            },
        }