from django.db import models
from django.contrib.auth.models import User 



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=13, default='+254000000000')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item
