import io
import logging

from django.contrib import messages
from django.shortcuts import render

from backend.controller.ddRadtoolController import handleDDRadSeqRequest, requestRestrictionEnzymes
from backend.settings import PAIRED_END_ENDING, SEQUENCING_YIELD_MULTIPLIER, MAX_NUMBER_SELECTFIELDS
from .forms import BasicInputDDRadDataForm

logger = logging.getLogger(__name__)

# Create your views here.

def webinterfaceViews(request):

    context = {"graph": "", 'mode': 'none'}
    restrictionEnzymes = requestRestrictionEnzymes()

    if request.method == "POST":

        inputForm = BasicInputDDRadDataForm(request.POST, request.FILES, restrictionEnzymes=restrictionEnzymes)

        if inputForm.is_valid():

            try:
                checkCorrectSequenceCalculationFields(inputForm)
                try:
                    readInputFasta = request.FILES['fastaFile'].read().decode('utf-8')
                    stringStreamFasta = io.StringIO(readInputFasta)
                except UnicodeDecodeError:
                    raise Exception('No proper fasta file has been uploaded')

                context["mode"] = inputForm.cleaned_data['formMode']

                if(inputForm.cleaned_data['formMode'] == 'tryOut'):
                    context = tryOutRequest(inputForm, restrictionEnzymes, stringStreamFasta, context)

            except Exception as e:
                logger.error(e)
                messages.error(request, e)

        else:
            logger.error(inputForm.errors)

    else:
        inputForm = BasicInputDDRadDataForm(initial={'pairedEndChoice': PAIRED_END_ENDING}, restrictionEnzymes=restrictionEnzymes)

    context["form"] = inputForm

    return render(request, "webinterface.html", context)

def tryOutRequest(inputForm, restrictionEnzymes, stringStreamFasta, context):

    if inputForm.cleaned_data["coverage"] != "" and int(inputForm.cleaned_data["coverage"]) == 0:
        raise Exception("Coverage cannot be 0")

    ddRadSeqresult = handleDDRadSeqRequest(stringStreamFasta, getPairsOfChosenRestrictionEnzyme(inputForm.cleaned_data, restrictionEnzymes),
                                           int(inputForm.cleaned_data["sequencingYield"]) * SEQUENCING_YIELD_MULTIPLIER if inputForm.cleaned_data["sequencingYield"] != "" else None,
                                           int(inputForm.cleaned_data["coverage"]) if inputForm.cleaned_data["coverage"] != "" else None,
                                           int(inputForm.cleaned_data['basepairLengthToBeSequenced']) if inputForm.cleaned_data["basepairLengthToBeSequenced"] != "" else None,
                                           inputForm.cleaned_data['pairedEndChoice'] if inputForm.cleaned_data["pairedEndChoice"] != "" else None)

    context["graph"] = ddRadSeqresult['graph']
    if "dataFrames" in ddRadSeqresult: context["dataFrames"] = ddRadSeqresult['dataFrames']
    context["basepairLengthToBeSequenced"] = inputForm.cleaned_data['basepairLengthToBeSequenced']
    context["pairedEndChoice"] = inputForm.cleaned_data['pairedEndChoice'] if inputForm.cleaned_data["pairedEndChoice"] != "" else None
    context["sequencingYield"] = int(inputForm.cleaned_data["sequencingYield"]) * SEQUENCING_YIELD_MULTIPLIER if inputForm.cleaned_data["sequencingYield"] != "" else None
    context["coverage"] = inputForm.cleaned_data['coverage'] if inputForm.cleaned_data["coverage"] != "" else None

    return context

def checkCorrectSequenceCalculationFields(inputForm):
    if (inputForm.cleaned_data["basepairLengthToBeSequenced"] != "" and inputForm.cleaned_data[
        "sequencingYield"] == "" and inputForm.cleaned_data["coverage"] == "" or
            inputForm.cleaned_data["basepairLengthToBeSequenced"] != "" and inputForm.cleaned_data[
                "sequencingYield"] != "" and inputForm.cleaned_data["coverage"] == "" or
            inputForm.cleaned_data["basepairLengthToBeSequenced"] != "" and inputForm.cleaned_data[
                "sequencingYield"] == "" and inputForm.cleaned_data["coverage"] != "" or
            inputForm.cleaned_data["sequencingYield"] != "" and inputForm.cleaned_data[
                "basepairLengthToBeSequenced"] == "" and inputForm.cleaned_data["coverage"] == "" or
            inputForm.cleaned_data["sequencingYield"] != "" and inputForm.cleaned_data[
                "basepairLengthToBeSequenced"] != "" and inputForm.cleaned_data["coverage"] == "" or
            inputForm.cleaned_data["sequencingYield"] != "" and inputForm.cleaned_data[
                "basepairLengthToBeSequenced"] == "" and inputForm.cleaned_data["coverage"] != "" or
            inputForm.cleaned_data["coverage"] != "" and inputForm.cleaned_data["basepairLengthToBeSequenced"] == "" and
            inputForm.cleaned_data["sequencingYield"] == "" or
            inputForm.cleaned_data["coverage"] != "" and inputForm.cleaned_data["basepairLengthToBeSequenced"] != "" and
            inputForm.cleaned_data["sequencingYield"] == "" or
            inputForm.cleaned_data["coverage"] != "" and inputForm.cleaned_data["basepairLengthToBeSequenced"] == "" and
            inputForm.cleaned_data["sequencingYield"] != ""):
        raise Exception("All sequence calculation parameters has to be chosen for calculation of sequence cost")

def getPairsOfChosenRestrictionEnzyme(inputFormClearedData, restrictionEnzymes):

    chosenRestrictionEnzymePairs = []

    for firstRestrictionEnzyme, secondRestrictionEnzyme in zip(range(1, MAX_NUMBER_SELECTFIELDS, 2), range(2, MAX_NUMBER_SELECTFIELDS, 2)):

        if inputFormClearedData['restrictionEnzyme' + str(firstRestrictionEnzyme)] == '' and inputFormClearedData['restrictionEnzyme' + str(secondRestrictionEnzyme)] != '' \
            or inputFormClearedData['restrictionEnzyme' + str(secondRestrictionEnzyme)] == '' and inputFormClearedData['restrictionEnzyme' + str(firstRestrictionEnzyme)] != "":

            raise Exception("Please ensure the every Restriction Enzyme has a partner.")

        if(inputFormClearedData['restrictionEnzyme' + str(firstRestrictionEnzyme)] != "" and
           inputFormClearedData['restrictionEnzyme' + str(secondRestrictionEnzyme)] != ""):
            chosenRestrictionEnzymePairs.append((restrictionEnzymes[int(inputFormClearedData['restrictionEnzyme' + str(firstRestrictionEnzyme)])],
                                                 restrictionEnzymes[int(inputFormClearedData['restrictionEnzyme' + str(secondRestrictionEnzyme)])]))

    if not chosenRestrictionEnzymePairs:
        raise Exception("Please select at least one pair, if you use this option")

    return chosenRestrictionEnzymePairs
