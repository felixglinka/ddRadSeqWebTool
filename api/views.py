import io, logging, shutil

from backend.controller.ddRadtoolController import handleDDRadSeqRequest, requestRestrictionEnzymes, \
    handleDDRadSeqComparisonRequest
from .forms import BasicInputDDRadDataForm

from django.shortcuts import render
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
                try:
                    readInputFasta = request.FILES['fastaFile'].read().decode('utf-8')
                    stringStreamFasta = io.StringIO(readInputFasta)
                except UnicodeDecodeError:
                    raise Exception('No proper fasta file has been uploaded')

                selectedMinSize = int(inputForm.cleaned_data["sizeSelectMin"])
                selectedMaxSize = int(inputForm.cleaned_data["sizeSelectMax"])

                if selectedMaxSize != None and selectedMinSize != None and selectedMaxSize < selectedMinSize:
                    raise Exception("Minimum value cannot exceed maximum value")

                if selectedMaxSize != None and selectedMinSize == None or selectedMinSize != None and selectedMaxSize == None :
                    raise Exception("A minimum and a maximum value needs to be chosen for the size selection")

                if inputForm.cleaned_data['restrictionEnzyme3'] == "" and inputForm.cleaned_data['restrictionEnzyme4'] == "":
                    context["graph"] = handleDDRadSeqRequest(stringStreamFasta, restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme1'])], restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme2'])], selectedMinSize, selectedMaxSize)
                elif inputForm.cleaned_data['restrictionEnzyme3'] == "" or inputForm.cleaned_data['restrictionEnzyme4'] == "":
                    raise Exception("Two restriction enzymes for comparison has to be chosen")
                else:
                    context["graph"] = handleDDRadSeqComparisonRequest(stringStreamFasta, restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme1'])], restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme2'])],
                                                                       restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme3'])], restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme4'])], selectedMinSize, selectedMaxSize)

            except Exception as e:
                logger.error(e)
                messages.error(request, e)

        else:
            logger.error(inputForm.errors)

    context["form"] = BasicInputDDRadDataForm(restrictionEnzymes=restrictionEnzymes)
    return render(request, "webinterface.html", context)