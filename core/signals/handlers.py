from django.dispatch import receiver
from restaurant.signals import order_created
from templated_mail.mail import BaseEmailMessage
from django.core.mail import EmailMessage, BadHeaderError


@receiver(order_created)
def on_order_created(sender, **kwargs):
    try:
        message = BaseEmailMessage(
            template_name='core/emails/hello.html',
            context={'name': kwargs['name'],
                     'order': kwargs['order']
                     }
        )
        message.send([kwargs['email']])
    except BadHeaderError:
        raise 'Bad Header Error'
    print(kwargs['order'])
