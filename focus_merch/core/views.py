from django.shortcuts import render 


def page(request):
    return render(request, 'index.html')
# Create your views here.