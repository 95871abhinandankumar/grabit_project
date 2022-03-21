from asyncio.windows_events import NULL
from distutils.log import error
from email import message
from pyexpat.errors import messages
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from django.core import serializers
import json
import datetime
import secrets
import string


from django.contrib.auth import login, authenticate , logout 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token 
from .models import User , UserChat 
from django.core.mail import EmailMessage  

import re

# Create your views here.


def logout_function(request):
    try:
        print("before deleting session")
        del request.session['user_id']
        print("after deleting session")
    except KeyError:
        pass
    return redirect('home')
    

def home(request):
    obj = None
    print(request.user.is_authenticated)
    if 'user_id' in request.session.keys():
        print("In user ........................")
        obj = User.objects.get(pk=request.session['user_id'])
    
    
    
    return render(request, "grabit/index.html", {'user': obj})


def forgot_password(request):
    obj = None
    if request.method == 'POST':
        username = request.POST['username']
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        
        try:
            # print(User.objects.get(email_id=username))
            obj = User.objects.get(email_id=username) 
            mail_subject = 'Password Reset'  
            message = render_to_string('grabit/password_reset.html', {  
                'user': obj,   
                'password':password,  
            }) 
            # print(message) 
            to_email = username  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()
            obj.password_field = password
            obj.save()
            
            return render(request, "grabit/After_password_reset.html")
        except User.DoesNotExist:
            return render(request, "grabit/forgot_password.html" , {'error_message':'Please enter a correct email-id','user': obj})
    
    return render(request, "grabit/forgot_password.html" ,{'user': obj})

def logIn(request):
    obj=None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        
        try:
            # print(User.objects.get(email_id=username))
            obj = User.objects.get(email_id=username)
            print(obj.is_active)
            # return render(request, "grabit/login.html" , {'error_message':'Account is not active'})
            if not obj.is_active:
                print("user is inactive")
                current_site = get_current_site(request)  
                mail_subject = 'Activation link has been sent to your email id'  
                message = render_to_string('grabit/acc_active_email.html', {  
                    'user': obj,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(obj.pk)),  
                    'token':account_activation_token.make_token(obj),  
                }) 
                # print(message) 
                to_email = username  
                email = EmailMessage(  
                            mail_subject, message, to=[to_email]  
                )  
                email.send()
                return render(request, "grabit/login.html" , {'error_message':'Account is not active, Please check your email!'})
            else:
                if obj.password_field != password:
                    return render(request, "grabit/login.html" , {'error_message':'Invalid password'})
                
                
                request.session['user_id'] = obj.id
                return render(request, "grabit/index.html" , {'user':obj})
                
            
        except User.DoesNotExist:
            return render(request, "grabit/login.html" , {'error_message':'User name is incorrect!'})
        
        
    return render(request, "grabit/login.html", {'user':obj})

def edit_profile(request):
    
    obj = None
    if 'user_id' in request.session.keys():
        obj = User.objects.get(pk=request.session['user_id'])
    
    if obj is None:
        return HttpResponse("page does't exits")
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        roll_number = request.POST['roll_number']
        room_number = request.POST['room_number']
        phone_number = request.POST['phone_number']
        
        if first_name != "":
            obj.first_name = first_name
        if last_name != "":
            obj.last_name = last_name 
        if roll_number != "":
            obj.roll_number = roll_number 
        if room_number != "":
            obj.room_number = room_number 
        if phone_number != "":
            obj.phone_number = phone_number  
        
        obj.save()
        
        
        
    return render(request, "grabit/edit_profile.html", { 'user' : obj})


def register(request):
    obj = None 
    if request.method == 'POST':  
        form = UserForm(request.POST, request.FILES) 
        # print("Hello") 
        if form.is_valid():  
            # save form in the memory not in database 
            # print("Before sending the email") 
            email = form.cleaned_data['email_id']
            email_regex = re.compile(r'^.*@iiitg.ac.in$')
            if bool(email_regex.match(email)) == False:
                return render(request, "grabit/register.html" , {'form': form, 'error_message':'Use iiitg email address'})
            
            try:
                User.objects.get(email_id=email)
                return render(request, "grabit/register.html" , {'form': form, 'error_message':'Email already in use'})
            except User.DoesNotExist:
            # Unable to find a user, this is fine
                user = form.save(commit=False)  
                user.is_active = False  
                user.save()  
                # to get the domain of the current site  
                current_site = get_current_site(request)  
                mail_subject = 'Activation link has been sent to your email id'  
                message = render_to_string('grabit/acc_active_email.html', {  
                    'user': user,     
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':account_activation_token.make_token(user),  
                }) 
                # print(message) 
                to_email = form.cleaned_data.get('email_id')  
                email = EmailMessage(  
                            mail_subject, message, to=[to_email]  
                )  
                email.send()  
                print("after sending the email")
                return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = UserForm()
    return render(request, "grabit/register.html" , {'form': form, 'user':obj})   



def activate(request, uidb64, token):  
    user = User()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))
        # print("printing uid",uid)  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None 
    
    # print(user)
    # print(token) 
    # print(account_activation_token.check_token(user, token))
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return render(request, "grabit/after_account_activation.html" )  
    else:  
        return HttpResponse('Activation link is invalid!')  
    


def userChat(request):
    
    
    obj = None
    if 'user_id' in request.session.keys():
        obj = User.objects.get(pk=request.session['user_id'])
    
    if obj is None:
        return redirect('login')
    
    if request.method == 'POST':
        
        print("printing active user of chat",request.POST['active_user_id'])

    usersChat_recieved = dict()
    usersChat_sent = dict()
    
    
    try:
        allChat_received = UserChat.objects.order_by('message_date_time').filter(receiver_id=obj.id)
    except UserChat.DoesNotExist:
        allChat_received = None
    
    try:
        allChat_sent = UserChat.objects.order_by('message_date_time').filter(sender_id=obj.id)
    except UserChat.DoesNotExist:
        allChat_sent = None
    
    
    for ob in allChat_received:
        # print("printing sender id in for loop : ", ob.sender_id)
        # print("Message ", ob.message, "reciever ", ob.receiver_id, "sender ", ob.sender_id)
        # print("type : ", type(ob.sender_id))
        try:
            userObj=User.objects.get(pk=ob.sender_id)
        except User.DoesNotExist:
            userObj = None
        
        if  ob.sender_id not in usersChat_recieved.keys():
            usersChat_recieved[ob.sender_id] = {'username':userObj.first_name, 'sender_id':userObj.id, 'messages':[ob]}
            
        else:
            usersChat_recieved[ob.sender_id]['messages'].append(ob)
    
    
    for ob in allChat_sent:
        print("in all chat sent")
        try:
            userObj=User.objects.get(pk=ob.receiver_id)
        except User.DoesNotExist:
            userObj = None
        
        if ob.receiver_id not in usersChat_sent.keys():
            usersChat_sent[ob.receiver_id] = {'username':userObj.first_name, 'receiver_id':userObj.id, 'messages':[ob]}
        
        else:
            usersChat_sent[ob.receiver_id]['messages'].append(ob)
        
    print("User chat received : ", usersChat_recieved)
    print("user chat sent ", usersChat_sent)
        
    return render(request, 'grabit/chat.html', {'chats_received':usersChat_recieved, 'chats_sent':usersChat_sent ,'user': obj})

def chat_with_someone(request):
    
    
    
    obj = None
    if 'user_id' in request.session.keys():
        obj = User.objects.get(pk=request.session['user_id'])
    
    if obj is None:
        return redirect('login')
    
    if request.method == 'GET':
        text = request.GET['text']
        temp = request.GET['receiver_id']
        sender = obj.id
        curr_date_time = datetime.datetime.now()
        print("before error")
        print(UserChat.objects.create(message=text, sender_id=sender, receiver_id=temp,message_date_time=curr_date_time))
        print("after error")
        
        chat_person = User.objects.get(pk=temp)
        x = list (UserChat.objects.raw('select * from grabit_userchat where (sender_id=%s and receiver_id=%s) or (sender_id=%s and receiver_id=%s) order by  message_date_time', [int(temp), obj.id, obj.id,int(temp)]))
        
        return render(request, "grabit/chat_with_someone.html", {'chat_history':x,'user': obj, 'chat_person':chat_person})
    
    
    if request.method == 'POST':
        
        print("printing active user of chat in chat with someone",request.POST['active_user_id'])
        temp = request.POST['active_user_id']
        chat_person = User.objects.get(pk=request.POST['active_user_id'])
        x = list (UserChat.objects.raw('select * from grabit_userchat where (sender_id=%s and receiver_id=%s) or (sender_id=%s and receiver_id=%s) order by  message_date_time', [int(temp), obj.id, obj.id,int(temp)]))
        
        return render(request, "grabit/chat_with_someone.html", {'chat_history':x,'user': obj, 'chat_person':chat_person})
        
    
    return render(request, "grabit/chat_with_someone.html", {'user': obj})
