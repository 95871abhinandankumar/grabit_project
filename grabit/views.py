from asyncio.windows_events import NULL
from distutils.log import error
from email import message
from itertools import product
from logging import exception
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
from django.core.paginator import Paginator


from django.contrib.auth import login, authenticate , logout 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token 
from .models import Advertisement, Product, User , UserChat 
from django.core.mail import EmailMessage  

import re

# Create your views here.


def help(request):
    obj = None
    print(request.user.is_authenticated)
    if 'user_id' in request.session.keys():
        print("In user ........................")
        obj = User.objects.get(pk=request.session['user_id'])
    
    else:
        return redirect('login')
    
    
    if request.method == 'GET':
        fname = request.GET.get('first-name', None)
        lname = request.GET.get('last-name', None)
        email = request.GET.get('email', None)
        message = request.GET.get('message', None)
        phone = request.GET.get('phone', None)
        try:
             
            mail_subject = fname + " " + lname  
            message = "Sender first-name is {fname} and last-name is {lname}. His phone number and Email-id is {phone} and {email}. Message : {message}".format(fname=fname, lname=lname, phone=phone, email=email, message=message) 
            to_email = 'grabitgrabit33@gmail.com' 
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()
        except:
            pass
        

    return render(request, "grabit/help.html", {'user': obj})



def send_message(request, id):
    obj = None
    print(request.user.is_authenticated)
    if 'user_id' in request.session.keys():
        print("In user ........................")
        obj = User.objects.get(pk=request.session['user_id'])
    
    else:
        return redirect('home')
    
    
    print(Product.objects.get(pk=id))
    
    
    return render(request, "grabit/send_message.html", {'user': obj})



def delete_ad(request, id):
    
    obj = None
    print(request.user.is_authenticated)
    if 'user_id' in request.session.keys():
        print("In user ........................")
        obj = User.objects.get(pk=request.session['user_id'])
    
    else:
        return redirect('login')
 
    try :
        Product.objects.get(pk=id).delete()
        Advertisement.objects.get(product_id=id).delete()
    except:
        pass
    
    return redirect('home')

# edit_ad view function

def edit_ad(request, id):
    
    obj = None
    print(request.user.is_authenticated)
    if 'user_id' in request.session.keys():
        print("In user ........................")
        obj = User.objects.get(pk=request.session['user_id'])
    
    else:
        return redirect('login')
 
    ads = Product.objects.get(pk=id)
    
    if request.method == 'POST':
        ads.price = request.POST['item_price']
        if request.POST.get('availability', False) == "on":
            ads.item_availablity = False
        
        ads.item_description = request.POST['item_description']
        ads.save()
    
    return render(request, "grabit/edit_ad.html", {'user': obj, 'ads':ads}) 

# end of edit_ad view function   


def my_ad(request):
    
    obj = None
    print(request.user.is_authenticated)
    if 'user_id' in request.session.keys():
        print("In user ........................")
        obj = User.objects.get(pk=request.session['user_id'])
    
    else:
        return redirect('login')
    
    
    user_ads = list(Product.objects.raw('select * from grabit_Product where buyer = %s or owner = %s', [obj.id, obj.id]))
    # print("in user ads : ", user_ads)
    
    
    return render(request, "grabit/my_ad.html", {'user': obj, 'user_ads':user_ads})
# end of my_ads views



def productPage(request, id):
    obj = None
    print(request.user.is_authenticated)
    if 'user_id' in request.session.keys():
        print("In user ........................")
        obj = User.objects.get(pk=request.session['user_id'])
    
    else:
        return redirect('login')
    
    itemObj = Product.objects.get(pk=id)

    return render(request, "grabit/productpage.html", {'user': obj, 'item':itemObj})

def addProduct(request):
    obj = None
    print(request.user.is_authenticated)
    if 'user_id' in request.session.keys():
        print("In user ........................")
        obj = User.objects.get(pk=request.session['user_id'])
    
    else:
        return redirect('login')
    
    if request.method == 'POST':
        item_name = request.POST['adTitle']
        price = request.POST['price']
        category = request.POST['category']
        item_description = request.POST['description']
        
        number = re.compile(r'^\d*\.?\d*$')
        if bool(number.match(price)) == False:
            return render(request, "grabit/addProduct.html" , {'user':obj, 'error_message_for_price':'Enter digits only(0-9)'})
        
        try:
            image1 = request.FILES['file1']
            image2 = request.FILES['file2']
            image3 = request.FILES['file3']
            image4 = request.FILES['file4']
        except Exception:
            print("image not found!")
            message="All four images are required"
            return render(request, "grabit/addProduct.html", {'user': obj, 'error_message':message})

        item = Product()
        
        item.item_name = item_name
        item.price = price
        item.category = category
        item.item_description = item_description
        item.image1 = image1
        item.image2 = image2
        item.image3 = image3
        item.image4 = image4
        
        
        
        
        radioValue = request.POST['radio']
        # print("For Sell")
        print(radioValue)
        if radioValue == 'sell':
            item.owner = obj.id
        else:
            item.buyer = obj.id
            
        item.save()
        
        ad = Advertisement()
        ad.ad_date_time = datetime.datetime.now()
        ad.product_id = item.id
        ad.ad_likes = 0
        ad.ad_dislikes = 0
        
        ad.save()
            
        
        # print("In add produt view ..................")
        # print("item title : ", item_name)
        # print("item description : ", item_description)
        # print("item category : ", category)
        # print("item price ", price)
        

    return render(request, "grabit/addProduct.html", {'user': obj})

def logout_function(request):
    try:
        print("before deleting session")
        del request.session['user_id']
        print("after deleting session")
    except KeyError:
        pass
    return redirect('home')



def home1(request, catogery):
    obj = None
    print(request.user.is_authenticated)
    if 'user_id' in request.session.keys():
        print("In user ........................")
        obj = User.objects.get(pk=request.session['user_id'])
        
        
    
    
    query = request.GET.get('search')
    
    if catogery=='buyer_ads':
        if query:
            try:
                products = Product.objects.filter(item_description__icontains=query, owner=None)
            except Product.DoesNotExist:
                return render(request, "grabit/index.html", {'user': obj, 'page_obj':None})
        else:
            products = Product.objects.filter(owner=None)
    else : 
        if query:
            try:
                products = Product.objects.filter(item_description__icontains=query, category=catogery, buyer=None)
            except Product.DoesNotExist:
                return render(request, "grabit/index.html", {'user': obj, 'page_obj':None})
        else:
            products = Product.objects.filter(category=catogery, buyer=None)
    
    
        
    sort_according = request.GET.get('sort')
    if sort_according:
        if sort_according == 'High to low price':
            products = products.order_by("-price")
        elif sort_according == 'Low to high price':
            products = products.order_by("price")
        elif sort_according == "Older first":
            products = products.order_by("-pk")
            print(products[0].id)
        elif sort_according == "Newer first":
            products = products.order_by("pk")
    
        products = list(products)
    
    product_objs = []
    for item in products:
        # print("today date", datetime.date.today())
        # print("product date", Advertisement.objects.get(product_id=item.id).ad_date_time.date())
        string1 = str(datetime.date.today() - Advertisement.objects.get(product_id=item.id).ad_date_time.date())
        s1 = string1.split(" ")[0].split(":")[0]
        if int(s1) <= 30:
            product_objs.append({'item':item, 'item_ad':Advertisement.objects.get(product_id=item.id)})
    
    
    
    p = Paginator(product_objs, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    
    
    return render(request, "grabit/index.html", {'user': obj, 'page_obj':page_obj.object_list})


    

def home(request):
    obj = None
    print(request.user.is_authenticated)
    if 'user_id' in request.session.keys():
        print("In user ........................")
        obj = User.objects.get(pk=request.session['user_id'])
        
        
    
    
    query = request.GET.get('search')
    if query:
        try:
            products = Product.objects.filter(item_description__icontains=query, buyer=None)
        except Product.DoesNotExist:
            return render(request, "grabit/index.html", {'user': obj, 'page_obj':None})
    else:
        products = Product.objects.filter(buyer=None)
        
    sort_according = request.GET.get('sort')
    if sort_according:
        if sort_according == 'High to low price':
            products = products.order_by("-price")
        elif sort_according == 'Low to high price':
            products = products.order_by("price")
        elif sort_according == "Older first":
            products = products.order_by("-pk")
            print(products[0].id)
        elif sort_according == "Newer first":
            products = products.order_by("pk")

    
    products = list(products)
    
    product_objs = []
    for item in products:
        # to show last 30 days product only
        string1 = str(datetime.date.today() - Advertisement.objects.get(product_id=item.id).ad_date_time.date())
        s1 = string1.split(" ")[0].split(":")[0]
        if int(s1) <= 30:
            product_objs.append({'item':item, 'item_ad':Advertisement.objects.get(product_id=item.id)})
    
    
    
    p = Paginator(product_objs, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    
    for ob in page_obj.object_list:
        print("page obj", ob)
    
    
    return render(request, "grabit/index.html", {'user': obj, 'page_obj':page_obj.object_list})


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
                # return render(request, "grabit/index.html" , {'user':obj})
                return redirect('home')
                
            
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
        
        print(request.FILES)
        if 'profile_pic' in request.FILES:
            obj.image = request.FILES['profile_pic'] 
            
        
        obj.save()
    
    print(obj.image)
        
        
        
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
        
    # print("User chat received : ", usersChat_recieved)
    # print("user chat sent ", usersChat_sent)
        
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


def changePassword(request):
    obj = None
    if 'user_id' in request.session.keys():
            obj = User.objects.get(pk=request.session['user_id'])
            
    
    print("in change Password method")
    if obj == None:
        print("obj is none in change password")
        return redirect('login')
        
    if request.method == 'POST': 
        # print("After submission of form")
        # print("old password : ", request.POST['oldPassword'])
        # print("new Password : " , request.POST['newPassword'])
        # print("reenter new password : ", request.POST['reenter_newPassword'])
        oldPass = request.POST['oldPassword']
        newPass = request.POST['newPassword']
        reenter_newPass = request.POST['reenter_newPassword']
        if oldPass != obj.password_field:
            return render(request, "grabit/changePassword.html", {'user':obj, 'error_message':"Current password is incorrect."})
        
        if newPass != reenter_newPass:
            return render(request, "grabit/changePassword.html", {'user':obj, 'error_message':"New password is not matching with Re-entered password."})
        
        obj.password_field = newPass
        obj.save()
        return render(request, "grabit/changePassword.html", {'user':obj, 'success_message':"Password successfully updated."})
            
    
    return render(request, "grabit/changePassword.html", {'user':obj})
    
