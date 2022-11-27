from celery import shared_task
from django.dispatch import receiver
from restaurant.signals import order_created
from django.core.mail import send_mass_mail, send_mail
from django.core.mail import EmailMessage, BadHeaderError
from restaurant.models import Customer

@shared_task
def notify_offer(message):
    print('Sending 10k emails...')
    print(message)

    queryset = Customer.objects.select_related('user').values('user__email')
    #names_list = [user['user__first_name'] for user in queryset]
    emails_list = [user['user__email'] for user in queryset]
    try:
        send_mail('FRIDAY OFFER!','message','info@foodclub.com',emails_list)
    except BadHeaderError:
        raise 'Bad Header Error'
    
    print('Emails were successfully sent!')