from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('', views.home, name='home'),
    path('add_product', views.addProduct, name='addProduct'),
    path('my_ads', views.my_ad, name='my_ads'),
    path('<int:id>/send_message', views.send_message, name='send_message'),
    path('<int:id>/product_page', views.productPage, name='productpage'),
    path('setting', views.changePassword, name='setting'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('chat', views.userChat, name='chat'),
    path('chat_', views.chat_with_someone, name='chat_with'),
    path('logout', views.logout_function, name='logout'),
    path('register', views.register, name='register'),
    path('login', views.logIn, name='login'),
    path('activate/<uidb64>/<token>/',  
        views.activate, name='activate'),  
    path('<str:catogery>', views.home1, name='home1'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)