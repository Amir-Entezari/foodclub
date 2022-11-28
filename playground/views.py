from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from core.tasks import notify_offer
import logging
# Create your views here.

logger = logging.getLogger(__name__)


def say_hello(request):
    notify_offer.delay('Notifing offers')
    return render(request, 'playground/index.html')


class HelloView(APIView):
    def get(self, request):
        try:
            logger.info('Calling Something')
            # SOME CODE HERE
            # .
            # .
            # .
            logger.info('Recived the respone')
            return render(request, 'playground/index.html')
        except request.ConnectionError:
            logger.critical('Something went wrong')
