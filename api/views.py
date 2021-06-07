import io
import logging

from backend.controller.ddRadtoolController import handleDDRadSeqRequest, requestRestrictionEnzymes
from .forms import BasicInputDDRadDataForm

from django.shortcuts import render, redirect
from django.contrib import messages

logger = logging.getLogger(__name__)

# Create your views here.

def webinterfaceViews(request):

    context = {"graph": ""}
    restrictionEnzymes = requestRestrictionEnzymes()

    if request.method == "POST":
        inputForm = BasicInputDDRadDataForm(request.POST, request.FILES, restrictionEnzymes=restrictionEnzymes)

        if inputForm.is_valid():

            try:
                readInputFasta = io.StringIO(request.FILES['fastaFile'].read().decode('utf-8'))
                context["graph"] = handleDDRadSeqRequest(readInputFasta, restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme1'])], restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme2'])])

            except Exception as e:
                logger.error(e)
                messages.error(request, 'A valid fasta file has not been uploaded.')

        else:
            logger.error(inputForm.errors)

    context["form"] = BasicInputDDRadDataForm(restrictionEnzymes=restrictionEnzymes)
    return render(request, "webinterface.html", context)