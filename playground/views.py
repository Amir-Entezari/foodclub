from django.core.mail import EmailMessage,BadHeaderError
from templated_mail.mail import BaseEmailMessage
from django.shortcuts import render,HttpResponse
from restaurant.models import Food
from .tasks import notify_customers
from restaurant.models import Customer
from core.tasks import notify_offer
# Create your views here.


def say_hello(request):
    notify_offer.delay('Notifing offers')
    return render(request,'playground/index.html')