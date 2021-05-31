from django.shortcuts import render

from .forms import BasicInputDDRadDataForm
from backend.service.HandleFastafile import readInFastaAndReturnOnlySequence
# Create your views here.

def webinterfaceViews(request):
    inputForm = BasicInputDDRadDataForm()
    if request.method == "POST":
        inputForm = BasicInputDDRadDataForm(request.POST, request.FILES)
        if inputForm.is_valid():
            print(request.FILES['fastaFile'])
            print(readInFastaAndReturnOnlySequence(request.FILES['fastaFile']))
            print("Everybody makes mistake")
        else:
            print(inputForm.errors)
    context = {
        "form": inputForm
    }
    return render(request, "webinterface.html", context)
