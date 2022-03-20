from django.contrib import admin
from .models import User, UserChat

# Register your models here.
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name', 'roll_number', 'room_number', 'phone_number', 'email_id', 'password_field' )
    
@admin.register(UserChat)
class Chat(admin.ModelAdmin):
    list_display = ('id','message','sender_id', 'receiver_id', 'message_date_time' )
