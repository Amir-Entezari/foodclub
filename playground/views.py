from django.shortcuts import render,HttpResponse
from restaurant.models import Food
# Create your views here.
def say_hello(request):
    queryset = Food.objects.all()
    return render(request,'index.html',{'foods':list(queryset)})