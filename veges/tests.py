from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from veges.views import  login_page

from django.core.files.uploadedfile import SimpleUploadedFile
from veges.models import Receipe  




class RegistrationTests(TestCase):

    def setUp(self):
        self.url = reverse('register') 

    def test_register_user_success(self):
        response = self.client.post(self.url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'password123'
        })
        
        # Check that the user was created
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='johndoe')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('password123'))

        # Check that the response redirects to the login page
        self.assertRedirects(response, '/login/')  # Adjust this if your login URL is different

        # Check for success message
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Account created successfully.")


    def test_register_user_username_exists(self):
        User.objects.create_user(username='johndoe', password='password123')

        response = self.client.post(self.url, {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'password456'
        })

        # Check that the user count is still 1
        self.assertEqual(User.objects.count(), 1)

        # Check that the response redirects back to the registration page
        self.assertRedirects(response, '/register/')  # Adjust this if your register URL is different

        # Check for error message)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Username already exists.")



class LoginTests(TestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.url = reverse("login")  

    def test_login_success(self):
       
        response = self.client.post(self.url, {
            "username": "testuser",
            "password": "password123"
        })

        self.assertRedirects(response, "/receipes/")  

    def test_login_invalid_username(self):
        
        response = self.client.post(self.url, {
            "username": "wronguser",
            "password": "password123"
        })

        self.assertRedirects(response, "/login/")
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Invalid Username")

    def test_login_invalid_password(self):
        
        response = self.client.post(self.url, {
            "username": "testuser",
            "password": "wrongpassword"
        })

        self.assertRedirects(response, "/login/")
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Invalid password")
        




class ReceipesTests(TestCase):

    def setUp(self):
        
        self.url = reverse("receipes")  
        self.receipe_image = SimpleUploadedFile(name='test.jpg', content=b'', content_type='image/jpeg')

    def test_create_receipe_success(self):
        
        response = self.client.post(self.url, {
            "Receipe_Name": "Chocolate Cake",
            "Receipe_Description": "A delicious chocolate cake recipe",
            "Receipe_Image": self.receipe_image,
        })

        self.assertEqual(Receipe.objects.count(), 1)
        receipe = Receipe.objects.first()
        self.assertEqual(receipe.receipe_name, "Chocolate Cake")
        self.assertEqual(receipe.receipe_description, "A delicious chocolate cake recipe")
        self.assertRedirects(response, "/receipes/")  

    def test_retrieve_all_receipes(self):
        Receipe.objects.create(receipe_name="Pasta", receipe_description="A classic Italian dish")
        Receipe.objects.create(receipe_name="Salad", receipe_description="A healthy vegetable salad")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")
        self.assertContains(response, "Salad")


