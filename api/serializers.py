from rest_framework import serializers
from .models import Customer, Order
import re

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'code', 'phone_number', 'user']

    # Validate the customer name, customer code and phone number
    
    def validate_name(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError("Name can only contain letters and spaces.")
        return value

    def validate_code(self, value):
        if not re.match(r'^[A-Za-z0-9]{6}$', value):
            raise serializers.ValidationError("Customer code must be exactly 6 alphanumeric characters.")
        return value

    def validate_phone_number(self, value):
        if not re.match(r'^\+254\d{9}$', value):
            raise serializers.ValidationError("Phone number must start with +254 and contain exactly 9 digits.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    # Validate the order item and order amount
    def validate_item(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError("Order item can only contain letters and spaces.")
        return value

    def validate_amount(self, value):
        try:
            if float(value) <= 0:
                raise serializers.ValidationError("Order amount must be a positive number.")
        except ValueError:
            raise serializers.ValidationError("Order amount must be a valid number.")
        return value