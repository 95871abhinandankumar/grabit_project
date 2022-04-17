from django.test import SimpleTestCase
from django.urls import reverse, resolve
from grabit.views import home, addProduct, my_ad, send_message, productPage, changePassword, forgot_password, userChat,chat_with_someone, logout_function, register, logIn,edit_profile, activate


class TestUrls(SimpleTestCase):
    
    
    def test_home_url_is_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)
        
    def test_addProduct_url_is_resolves(self):
        url = reverse('addProduct')
        self.assertEquals(resolve(url).func, addProduct)
        
    def test_my_ads_url_is_resolves(self):
        url = reverse('my_ads')
        self.assertEquals(resolve(url).func, my_ad)
        
    def test_send_message_is_resolves(self):
        url = reverse('send_message', args=[1])
        self.assertEquals(resolve(url).func, send_message)
    
    def test_product_page_is_resolves(self):
        url = reverse('productpage', args=[1])
        self.assertEquals(resolve(url).func, productPage)
    
    
    def test_setting_url_is_resolves(self):
        url = reverse('setting')
        self.assertEquals(resolve(url).func, changePassword)
    
    def test_forgot_password_url_is_resolves(self):
        url = reverse('forgot_password')
        self.assertEquals(resolve(url).func, forgot_password)
        
    def test_userChat_url_is_resolves(self):
        url = reverse('chat')
        self.assertEquals(resolve(url).func, userChat)
    
    def test_chatWith_url_is_resolves(self):
        url = reverse('chat_with')
        self.assertEquals(resolve(url).func, chat_with_someone)
    
    def test_logout_url_is_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_function)
        
    def test_register_url_is_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)
        
    def test_logIn_url_is_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, logIn)
        
    def test_editProfile_is_resolves(self):
        url = reverse('edit_profile')
        self.assertEquals(resolve(url).func, edit_profile)
        