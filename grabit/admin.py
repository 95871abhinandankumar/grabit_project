from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name', 'roll_number', 'room_number', 'phone_number', 'email_id', 'password_field' )
