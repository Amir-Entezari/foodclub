from django.core.mail import EmailMessage,BadHeaderError
from templated_mail.mail import BaseEmailMessage
from django.shortcuts import render,HttpResponse
from restaurant.models import Food
# Create your views here.


def say_hello(request):
    try:
        message=BaseEmailMessage(
            template_name='emails/hello.html',
            context={'name':'Amir'}
        )
        message.send(['user@gmail.com'])
    except BadHeaderError:
        raise 'Bad Header Error'
    return render(request,'index.html')