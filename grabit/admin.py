from django.contrib import admin
from .models import Advertisement, Product, User, UserChat

# Register your models here.
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'image','first_name','last_name', 'roll_number', 'room_number', 'phone_number', 'email_id', 'password_field' )
    
@admin.register(UserChat)
class Chat(admin.ModelAdmin):
    list_display = ('id','message','sender_id', 'receiver_id', 'message_date_time' )
    

@admin.register(Product)
class product(admin.ModelAdmin):
    list_display = ('id','item_name','price', 'owner', 'buyer', 'item_availablity', 'category', 'item_description', 'image1', 'image2', 'image3','image4')
    

@admin.register(Advertisement)
class Advertisement(admin.ModelAdmin):
    list_display = ('id','ad_date_time','product_id', 'choice_mark', 'ad_likes', 'ad_dislikes')
