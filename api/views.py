from django.shortcuts import render
# Create your views here.

def webinterface(request):
    return render(request, "webinterface.html")
