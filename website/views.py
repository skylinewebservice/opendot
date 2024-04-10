from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def why(request):
    return render(request, 'why.html')

def contact(request):
    return render(request, 'contact.html')