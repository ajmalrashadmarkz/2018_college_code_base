from django.shortcuts import render,redirect
# Create your views here.

# def home_page(request):
#     return render(request,'home.html')

def home_page(request):
    context = {'page_title': 'Home Page'}
    return render(request, 'home.html', context)

