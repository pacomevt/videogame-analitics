from django.shortcuts import render

def index(request):
    return render(request, 'app/index.html', context={'name': 'John Doe'})

