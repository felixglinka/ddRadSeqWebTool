import io

from django.shortcuts import render

from backend.controller.ddRadtoolController import handleDDRadSeqRequest
from .forms import BasicInputDDRadDataForm

from django.contrib import messages

# Create your views here.

def webinterfaceViews(request):
    context = {"graph": ""}

    if request.method == "POST":
        inputForm = BasicInputDDRadDataForm(request.POST, request.FILES)
        if inputForm.is_valid():
            try:
                readInputFasta = io.StringIO(request.FILES['fastaFile'].read().decode('utf-8'))
                outputGraph = handleDDRadSeqRequest(readInputFasta)
            except:
                messages.error(request, "You better get the best of both worlds")
                context["form"] = BasicInputDDRadDataForm()
                return render(request, "webinterface.html", context)

            context["graph"] = outputGraph
        else:
            print(inputForm.errors)
    else:
        inputForm = BasicInputDDRadDataForm()

    context["form"] = inputForm
    return render(request, "webinterface.html", context)
