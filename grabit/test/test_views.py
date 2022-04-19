from django.test import TestCase, Client
from django.urls import reverse
from grabit.views import home, addProduct, my_ad, send_message, productPage, changePassword, forgot_password, userChat,chat_with_someone, logout_function, register, logIn,edit_profile, activate
from grabit.models import User, UserChat, Product, Advertisement
import json


# class TestViews(TestCase):
#     def test_call_view_deny_anonymous(self):
#         response = self.client.get('/url/to/view', follow=True)
#         self.assertRedirects(response, '/login/')
#         response = self.client.post('/url/to/view', follow=True)
#         self.assertRedirects(response, '/login/')

    
    