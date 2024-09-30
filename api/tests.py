from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer, Order
from rest_framework.exceptions import ValidationError
from .serializers import CustomerSerializer
from unittest.mock import patch
from api.services import send_order_sms_alert

# Test cases for Customer and Order API views
class CustomerOrderTests(APITestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  

        # Create a customer for testing
        self.customer = Customer.objects.create(
            user=self.user, name='Mark Wambugu', code='123456', phone_number='+254712345678'
        )
 
    # Test the GET request for listing customers
    def test_list_customers(self):
        url = reverse('customer-list')  # URL for customer list
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    # Test the GET request for listing orders
    def test_list_orders(self):
        Order.objects.create(user=self.user, customer=self.customer, item='Laptop', amount=1000)
        url = reverse('order-list')  # URL for order list
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1) 


# Test cases for CustomerSerializer
class SerializerTests(APITestCase):

    # Test for invalid customer serialization
    def test_customer_serializer_invalid(self):
        data = {'name': 'Mary Olang', 'code': '123', 'phone_number': 'invalidphone'}
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


# Test case for sending order SMS
class ServiceTests(APITestCase):

    @patch('api.services.sms.send')  
    def test_send_order_sms_alert(self, mock_send):
        mock_send.return_value = "SMS Sent"
        
        result = send_order_sms_alert('Mark Wambugu', '+254712345678', 'Laptop', 1000)
        
        self.assertEqual(result, None)  
        
        mock_send.assert_called_once_with(
            "Hi Mark Wambugu, your order for Laptop amounting to 1000 has been received!", 
            ['+254712345678']
        )

# Test cases for authentication (Auth0 integration)
class AuthTests(APITestCase):

    # Test if the user is redirected to the Auth0 login page
    def test_auth_login(self):
        response = self.client.get(reverse('social:begin', args=['auth0']))
        self.assertEqual(response.status_code, 302)  

    # Test if the user is redirected after logout
    def test_auth_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  


# Test cases for API root and URLs
class URLTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

    # Test for the dashboard URL
    def test_dashboard_url(self):
        url = reverse('dashboard')
        self.assertEqual(url, '/dashboard/')

    # Test for the customer URL
    def test_customer_url(self):
        url = reverse('customer-list')
        self.assertEqual(url, '/api/customers/')


