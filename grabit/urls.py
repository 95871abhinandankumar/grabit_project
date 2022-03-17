from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('login', views.logIn, name='login'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('activate/<uidb64>/<token>/',  
        views.activate, name='activate'),  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)