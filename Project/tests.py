from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from veges.models import Receipe  
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By



# testCase script for registration page
'''
class RegistrationTests(TestCase):

    def setUp(self):
        self.url = reverse('register') 

    def test_register_user_success(self):
        response = self.client.post(self.url, {
            'first_name': 'madhuri',
            'last_name': 'shendge',
            'username': 'madhuri',
            'password': '123'
        })
        
       
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='madhuri')
        self.assertEqual(user.first_name, 'madhuri')
        self.assertEqual(user.last_name, 'shendge')
        self.assertTrue(user.check_password('123'))

       
        self.assertRedirects(response, '/login/') 

       
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Account created successfully.")
        print("test_register_user_success")

    def test_register_user_username_exists(self):
        User.objects.create_user(username='madhuri', password='123')

        response = self.client.post(self.url, {
            'first_name': 'mansi',
            'last_name': 'shendge',
            'username': 'madhuri',
            'password': '456'
        })

      
        self.assertEqual(User.objects.count(), 1)

        
        self.assertRedirects(response, '/register/')  

       
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Username already exists.")
        print("test_register_user_username_exists")


# Test case script for Login Page

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
        print("test_login_success") 

    def test_login_invalid_username(self):
        
        response = self.client.post(self.url, {
            "username": "wronguser",
            "password": "password123"
        })

        self.assertRedirects(response, "/login/")
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Invalid Username")
        print("test_login_invalid_username")

    def test_login_invalid_password(self):
        
        response = self.client.post(self.url, {
            "username": "testuser",
            "password": "wrongpassword"
        })

     
        self.assertRedirects(response, "/login/")
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Invalid password")
        print("test_login_invalid_password")


# Test case script to  check Receipe creates successfully.

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
        print("test_create_receipe_success")

   
        

    def test_retrieve_all_receipes(self):
        Receipe.objects.create(receipe_name="Pasta", receipe_description="A classic Italian dish")
        Receipe.objects.create(receipe_name="Salad", receipe_description="A healthy vegetable salad")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")
        self.assertContains(response, "Salad")
        print("test_retrieve_all_receipes")



# Test case script for updating the receipe

class UpdateReceipeTests(TestCase):

    def setUp(self):
        
        self.receipe = Receipe.objects.create(
            receipe_name="Pasta",
            receipe_description="A classic Italian dish",
            receipe_image=None
        )
        self.url = reverse("update_receipe", args=[self.receipe.id])

    def test_update_receipe_success(self):
        
        new_image = SimpleUploadedFile(name="new_test.jpg", content=b"", content_type="image/jpeg")

        response = self.client.post(self.url, {
            "Receipe_Name": "Updated Pasta",
            "Receipe_Description": "An improved recipe",
            "Receipe_Image": new_image
        })

        # Refresh from DB
        self.receipe.refresh_from_db()

        self.assertEqual(self.receipe.receipe_name, "Updated Pasta")
        self.assertEqual(self.receipe.receipe_description, "An improved recipe")
        self.assertRedirects(response, "/receipes/") 
        print("test_update_receipe_success")

    def test_update_receipe_without_image(self):
        """Test updating a recipe without changing the image."""
        response = self.client.post(self.url, {
            "Receipe_Name": "Veggie Pasta",
            "Receipe_Description": "A healthier version",
            "Receipe_Image": ""  
        })

        self.receipe.refresh_from_db()

        self.assertEqual(self.receipe.receipe_name, "Veggie Pasta")
        self.assertEqual(self.receipe.receipe_description, "A healthier version")
        self.assertRedirects(response, "/receipes/")
        print("test_update_receipe_without_image")

    def test_update_receipe_invalid_id(self):
        """Test updating a recipe with an invalid ID."""
        invalid_url = reverse("update_receipe", args=[99999])
        response = self.client.post(invalid_url, {
            "Receipe_Name": "Failsauce",
            "Receipe_Description": "Should not update"
        })

        self.assertEqual(response.status_code, 404)  
        print("test_update_receipe_invalid_id")



# test case script for deleting the receipe
class DeleteReceipeTests(TestCase):

    def setUp(self):
        self.receipe = Receipe.objects.create(
            receipe_name="Chocolate Cake",
            receipe_description="A delicious chocolate cake recipe"
        )
        self.url = reverse("delete_receipe", args=[self.receipe.id])

    def test_delete_receipe_success(self):
        
        response = self.client.post(self.url) 

        # Ensure the recipe is deleted
        self.assertFalse(Receipe.objects.filter(id=self.receipe.id).exists())

       
        self.assertRedirects(response, "/receipes/") 
        print("test_delete_receipe_success")
        
        
    def test_delete_receipe_invalid_id(self):
        
        invalid_url = reverse("delete_receipe", args=[99999]) 
        response = self.client.post(invalid_url)

        self.assertEqual(response.status_code, 404) 
        print("test_delete_receipe_invalid_id") 
        
        
# Test case for searching the receipe
     
class SearchReceipesTests(TestCase):

    def setUp(self):
      
        Receipe.objects.create(receipe_name="Chocolate Cake", receipe_description="A delicious dessert")
        Receipe.objects.create(receipe_name="Pasta", receipe_description="An Italian dish")
        Receipe.objects.create(receipe_name="Salad", receipe_description="A healthy option")
        self.url = reverse("receipes")  

    def test_search_query_found(self):
       
        response = self.client.get(self.url, {"search": "Pasta"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")
        self.assertNotContains(response, "Chocolate Cake")
        self.assertNotContains(response, "Salad")
        print("test_search_query_found")
         
    def test_search_query_not_found(self):
      
        response = self.client.get(self.url, {"search": "Burger"})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Chocolate Cake")
        self.assertNotContains(response, "Pasta")
        self.assertNotContains(response, "Salad")
        print("test_search_query_not_found")
        

    def test_empty_search_query(self):
        
        response = self.client.get(self.url, {"search": ""})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chocolate Cake")
        self.assertContains(response, "Pasta")
        self.assertContains(response, "Salad")
        print("test_empty_search_query")
        


# Test case for logout the user or not
class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

    def test_logout_redirect(self):
        response = self.client.get(reverse('logout_page'))  
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)
        print("LogoutViewTest")
'''
# tests/test_registration.py

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegistrationTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = True  # Run in headless mode
        cls.selenium = webdriver.Chrome(options=options)
        options.add_argument("--no-sandbox")
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_register_new_user(self):
        self.selenium.get(self.live_server_url + reverse('register'))  # Adjust the URL as needed


        # Fill out the registration form
        self.selenium.find_element(By.NAME, 'first_name').send_keys('John')
        self.selenium.find_element(By.NAME, 'last_name').send_keys('Doe')
        self.selenium.find_element(By.NAME, 'username').send_keys('johndoe')
        self.selenium.find_element(By.NAME, 'password').send_keys('password123')

        # Submit the form
        wait = WebDriverWait(self.selenium, 10)
        
        try:
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]')))
        except:
            try:
                submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
            except Exception as e:
                # Print page source to help debugging
                print("Submit button not found. Page source:")
                print(self.selenium.page_source)
                raise e
        submit_button.click()
       
        # Check for success message
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))  # Adjust class name as needed
        )
        success_message = self.selenium.find_element(By.CLASS_NAME, 'alert-success').text
        self.assertIn("Account created successfully.", success_message)

        # Verify the user is created in the database
        user_exists = get_user_model().objects.filter(username='johndoe').exists()
        self.assertTrue(user_exists)
        print("test_register_new_user : Testcase passed" )

    def test_register_existing_user(self):
        # Create a user to test the existing username scenario
        get_user_model().objects.create_user(first_name='Jane', last_name='Doe', username='janedoe', password='password123')

        self.selenium.get(self.live_server_url + reverse('register'))  # Adjust the URL as needed

        # Fill out the registration form with an existing username
        self.selenium.find_element(By.NAME, 'first_name').send_keys('John')
        self.selenium.find_element(By.NAME, 'last_name').send_keys('Doe')
        self.selenium.find_element(By.NAME, 'username').send_keys('janedoe')  # Existing username
        self.selenium.find_element(By.NAME, 'password').send_keys('password123')

        # Submit the form
        wait = WebDriverWait(self.selenium, 10)
        try:
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]')))
        except Exception:
            try:
                submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
            except Exception as e:
                # Print page source to help debugging
                print("Submit button not found. Page source:")
                print(self.selenium.page_source)
                raise e
        submit_button.click()

        # Check for error message
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-info'))  # Adjust class name as needed
        )
        error_message = self.selenium.find_element(By.CLASS_NAME, 'alert-info').text
        self.assertIn("Username already exists.", error_message)
        print("test_register_existing_user : Testcase passed" )





        