import io

from django.shortcuts import render

from backend.controller.ddRadtoolController import handleDDRadSeqRequest
from .forms import BasicInputDDRadDataForm

# Create your views here.

def webinterfaceViews(request):
    inputForm = BasicInputDDRadDataForm()
    context = {"graph": ""}
    if request.method == "POST":
        inputForm = BasicInputDDRadDataForm(request.POST, request.FILES)
        if inputForm.is_valid() and context["graph"] == "":
            readInputFasta = io.StringIO(request.FILES['fastaFile'].read().decode('utf-8'))
            outputGraph = handleDDRadSeqRequest(readInputFasta)
            context["graph"] = outputGraph
            print("Everybody makes mistake")
        else:
            print(inputForm.errors)
    else:
        inputForm = BasicInputDDRadDataForm()
    context["form"] = inputForm
    return render(request, "webinterface.html", context)
