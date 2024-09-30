import africastalking
from django.conf import settings

# Initialize the Africa's Talking SDK
africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)

sms = africastalking.SMS

#Send customer a message after adding an order
def send_order_sms_alert(customer_name, customer_phone, order_item, order_amount):
    message = f"Hi {customer_name}, your order for {order_item} amounting to {order_amount} has been received!"
    recipients = [customer_phone]  
    
    try:
        response = sms.send(message, recipients)
        print(f"API Response: {response}")  
    except Exception as e:
        print(f"Error sending SMS: {e}")  

