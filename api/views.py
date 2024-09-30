from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from rest_framework import viewsets
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .services import send_order_sms_alert
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from django.conf import settings
from django.db import IntegrityError
from django.contrib import messages
import urllib.parse
import bleach


# ViewSets to handle customers and orders API endpoints
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    #Send Africa'sTalking SMS after an order instance has been saved
    def perform_create(self, serializer):

        order = serializer.save()
        customer = order.customer
        customer_name = customer.name
        customer_phone = customer.phone_number  

        send_order_sms_alert(customer_name, customer_phone, order.item, order.amount)
  
  
  
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

    
@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('social:begin', backend='auth0') 
    customers = Customer.objects.filter(user=request.user) 
    orders = Order.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {
        'auth0_domain': settings.SOCIAL_AUTH_AUTH0_DOMAIN,
        'auth0_client_id': settings.SOCIAL_AUTH_AUTH0_KEY, 
        'customers': customers,
        'orders': orders
    })

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'customers': reverse('customer-list', request=request, format=format),
        'orders': reverse('order-list', request=request, format=format),
        'dashboard': request.build_absolute_uri(reverse('dashboard')),
        'logout': request.build_absolute_uri(reverse('logout'))
    })

# View to add a new customer. Only logged-in users can access this view.
@login_required
def add_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        phone_number = request.POST.get('phone_number')

        # Sanitize inputs from the customer form to prevent attacks
        sanitized_name = bleach.clean(name)
        sanitized_code = bleach.clean(code)
        
        # Check if a customer with the same code already exists
        if Customer.objects.filter(code=sanitized_code).exists():
            messages.error(request, 'Customer code already exists! Please use a different code.')
            return redirect('dashboard')

        try:
            # Create a new customer and associate te customer with the logged-in user
            Customer.objects.create(
                user=request.user, 
                name=sanitized_name, code=sanitized_code, 
                phone_number=f'+254{phone_number}')
        
            messages.success(request, 'Customer added successfully!')
            return redirect('dashboard')
        except IntegrityError:
            messages.error(request, 'An error occurred while adding the customer.')
            return redirect('dashboard')

    return render(request, 'dashboard.html')

# View to add a new order. Only logged-in users can access this view.
@login_required
def add_order(request):
    if request.method == 'POST':
        # Get order details from the POST request
        customer_id = request.POST.get('customer') 
        item = request.POST.get('item')
        amount = request.POST.get('amount')

        # Get the customer object associated with the logged-in user
        customer = Customer.objects.get(id=customer_id, user=request.user)

        # Create a new order for the customer
        order = Order.objects.create(user=request.user, customer=customer, item=item, amount=amount)

        # Send an Africa's Talking SMS alert to the customer about the order
        send_order_sms_alert(customer.name, customer.phone_number, order.item, order.amount)

        return redirect('dashboard')

# View to handle logout using Auth0. Redirects the user to the Auth0 logout URL.
def auth0_logout(request):
    
    django_logout(request)

    auth0_domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY

    if request.get_host() == 'localhost:8000':
        return_url = 'http://localhost:8000/' 
    else:
        return_url = 'https://savannah-informatics-app-e00749f637ce.herokuapp.com/'  

    logout_url = f'https://{auth0_domain}/v2/logout?client_id={client_id}&returnTo={urllib.parse.quote(return_url)}'

    return redirect(logout_url)

# Custom 404 error handler to redirect users based on their login status.
def page_not_found(request, exception=None):
    """
    Custom 404 error handler. Redirects to home if not logged in, 
    or to the dashboard if logged in.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('home')
