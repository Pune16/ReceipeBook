from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from veges.models import Receipe  
from django.contrib.auth import get_user_model
from django.test.client import Client


# testCase script for registration page

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
        
       
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='johndoe')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('password123'))

       
        self.assertRedirects(response, '/login/') 

       
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

      
        self.assertEqual(User.objects.count(), 1)

        
        self.assertRedirects(response, '/register/')  

       
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Username already exists.")


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
        


# Test case script to  check Receipe creates successfylly.

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

    def test_update_receipe_without_image(self):
        """Test updating a recipe without changing the image."""
        response = self.client.post(self.url, {
            "Receipe_Name": "Veggie Pasta",
            "Receipe_Description": "A healthier version",
            "Receipe_Image": ""  
        })

        # Refresh from DB
        self.receipe.refresh_from_db()

        self.assertEqual(self.receipe.receipe_name, "Veggie Pasta")
        self.assertEqual(self.receipe.receipe_description, "A healthier version")
        self.assertRedirects(response, "/receipes/")

    def test_update_receipe_invalid_id(self):
        """Test updating a recipe with an invalid ID."""
        invalid_url = reverse("update_receipe", args=[99999])
        response = self.client.post(invalid_url, {
            "Receipe_Name": "Failsauce",
            "Receipe_Description": "Should not update"
        })

        self.assertEqual(response.status_code, 404)  



# test case script for deleting the receipe
class DeleteReceipeTests(TestCase):

    def setUp(self):
        self.receipe = Receipe.objects.create(
            receipe_name="Chocolate Cake",
            receipe_description="A delicious chocolate cake recipe"
        )
        self.url = reverse("delete_receipe", args=[self.receipe.id])

    def test_delete_receipe_success(self):
        """Test deleting a recipe successfully."""
        response = self.client.post(self.url) 

        # Ensure the recipe is deleted
        self.assertFalse(Receipe.objects.filter(id=self.receipe.id).exists())

       
        self.assertRedirects(response, "/receipes/") 
    def test_delete_receipe_invalid_id(self):
        """Test attempting to delete a non-existent recipe."""
        invalid_url = reverse("delete_receipe", args=[99999]) 
        response = self.client.post(invalid_url)

        self.assertEqual(response.status_code, 404)  
        
        
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

    def test_search_query_not_found(self):
      
        response = self.client.get(self.url, {"search": "Burger"})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Chocolate Cake")
        self.assertNotContains(response, "Pasta")
        self.assertNotContains(response, "Salad")

    def test_empty_search_query(self):
        
        response = self.client.get(self.url, {"search": ""})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chocolate Cake")
        self.assertContains(response, "Pasta")
        self.assertContains(response, "Salad")



# Test case for logout the user or not
class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

    def test_logout_redirect(self):
        response = self.client.get(reverse('logout_page'))  
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)
