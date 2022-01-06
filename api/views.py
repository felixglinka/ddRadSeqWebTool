import logging
import os

from chunked_upload.views import ChunkedUploadCompleteView, ChunkedUploadView
from django.contrib import messages
from django.shortcuts import render, redirect

from backend.controller.ddRadtoolController import handleDDRadSeqRequest, requestRestrictionEnzymes, \
    handlePopulationStructureRequest, requestPopoverTexts, requestInformationTexts, handleGenomeScanRequest
from backend.settings import PAIRED_END_ENDING, SEQUENCING_YIELD_MULTIPLIER, MAX_NUMBER_SELECTFIELDS, \
    ADAPTORCONTAMINATIONSLOPE, OVERLAPSLOPE, POLYMORPHISM_MODIFIER, DENSITY_MODIFIER
from .forms import BasicInputDDRadDataForm
from .models import fastaFileUpload

logger = logging.getLogger(__name__)

# Create your views here.

def webinterfaceViews(request):

    context = {"graph": "", 'mode': 'none', 'popoverContents': requestPopoverTexts(),
               'adaptorContaminationSlope': ADAPTORCONTAMINATIONSLOPE, "overlapSlope": OVERLAPSLOPE}
    restrictionEnzymes = requestRestrictionEnzymes()

    if request.method == "POST":

        try:
            inputForm = BasicInputDDRadDataForm(request.POST, restrictionEnzymes=restrictionEnzymes)
            checkIfThereIsAnInputFastaFile(inputForm)

            if inputForm.is_valid():

                try:
                    checkCorrectSequenceCalculationFields(inputForm)

                    uploadedFastaFile = inputForm.cleaned_data['formFile']
                    context["mode"] = inputForm.cleaned_data['formMode']
                    context["fileName"] = os.path.splitext(inputForm.cleaned_data['formFileName'])[0]

                    if(inputForm.cleaned_data['formMode'] == 'tryOut'):
                        context = tryOutRequest(inputForm, restrictionEnzymes, uploadedFastaFile, context)
                    if(inputForm.cleaned_data['formMode'] == 'beginner-populationStructure'):
                        context = beginnerPopulationStructureRequest(inputForm, uploadedFastaFile, context)
                    if(inputForm.cleaned_data['formMode'] == 'beginner-genomeScan'):
                        context = beginnerGenomeScanRequest(inputForm, uploadedFastaFile, context)

                except Exception as e:
                    logger.error(e)
                    messages.error(request, e)

            else:
                logger.error(inputForm.errors)

        except Exception as e:
            logger.error(e)
            messages.error(request, e)

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

def beginnerPopulationStructureRequest(inputForm, stringStreamFasta, context):

    checkAllBeginnerFieldEntries(inputForm)

    if (inputForm.cleaned_data["popStructNumberOfSnps"] == "" or inputForm.cleaned_data[
        "popStructExpectPolyMorph"] == "" ):
        raise Exception("Please insert all fields for the population structure analysis.")

    populationStructureResult = handlePopulationStructureRequest(stringStreamFasta,
                                           int(inputForm.cleaned_data["popStructNumberOfSnps"]),
                                           int(inputForm.cleaned_data["popStructExpectPolyMorph"])/POLYMORPHISM_MODIFIER,
                                           int(inputForm.cleaned_data['basepairLengthToBeSequenced']) if inputForm.cleaned_data["basepairLengthToBeSequenced"] != "" else None,
                                           inputForm.cleaned_data['pairedEndChoice'] if inputForm.cleaned_data["pairedEndChoice"] != "" else None)

    if "graph" in populationStructureResult:
        context["graph"] = populationStructureResult['graph']
    else:
        context["noRecommendation"] = 'n'
    if "dataFrames" in populationStructureResult: context["dataFrames"] = populationStructureResult['dataFrames']
    context["basepairLengthToBeSequenced"] = inputForm.cleaned_data['basepairLengthToBeSequenced']
    context["pairedEndChoice"] = inputForm.cleaned_data['pairedEndChoice']
    context["sequencingYield"] = int(inputForm.cleaned_data["sequencingYield"]) * SEQUENCING_YIELD_MULTIPLIER
    context["coverage"] = inputForm.cleaned_data['coverage']
    context["expectedNumberOfSnps"] = inputForm.cleaned_data['popStructNumberOfSnps']
    context["expectPolyMorph"] = int(inputForm.cleaned_data['popStructExpectPolyMorph'])/POLYMORPHISM_MODIFIER

    return context

def beginnerGenomeScanRequest(inputForm, stringStreamFasta, context):

    checkAllBeginnerFieldEntries(inputForm)

    if (inputForm.cleaned_data["genomeScanRadSnpDensity"] == "" or inputForm.cleaned_data[
        "genomeScanExpectPolyMorph"] == "" ):
        raise Exception("Please insert all fields for the genome scan.")

    genomeScanResult = handleGenomeScanRequest(stringStreamFasta,
                                           int(inputForm.cleaned_data["genomeScanRadSnpDensity"])/DENSITY_MODIFIER,
                                           int(inputForm.cleaned_data["genomeScanExpectPolyMorph"])/POLYMORPHISM_MODIFIER,
                                           int(inputForm.cleaned_data['basepairLengthToBeSequenced']) if inputForm.cleaned_data["basepairLengthToBeSequenced"] != "" else None,
                                           inputForm.cleaned_data['pairedEndChoice'] if inputForm.cleaned_data["pairedEndChoice"] != "" else None)

    if "graph" in genomeScanResult:
        context["graph"] = genomeScanResult['graph']
    else:
        context["noRecommendation"] = 'n'
    if "dataFrames" in genomeScanResult: context["dataFrames"] = genomeScanResult['dataFrames']
    if "expectedNumberOfSnps" in genomeScanResult: context["expectedNumberOfSnps"] = genomeScanResult['expectedNumberOfSnps']
    context["basepairLengthToBeSequenced"] = inputForm.cleaned_data['basepairLengthToBeSequenced']
    context["pairedEndChoice"] = inputForm.cleaned_data['pairedEndChoice']
    context["sequencingYield"] = int(inputForm.cleaned_data["sequencingYield"]) * SEQUENCING_YIELD_MULTIPLIER
    context["coverage"] = inputForm.cleaned_data['coverage']
    context["expectPolyMorph"] = int(inputForm.cleaned_data['genomeScanExpectPolyMorph']) / POLYMORPHISM_MODIFIER

    return context

def checkAllBeginnerFieldEntries(inputForm):
    if (inputForm.cleaned_data["basepairLengthToBeSequenced"] == "" or inputForm.cleaned_data[
        "sequencingYield"] == "" or inputForm.cleaned_data["coverage"] == ""):
        raise Exception("All sequence calculation parameters has to be chosen for the prediction")

def checkIfThereIsAnInputFastaFile(inputForm):

    if (inputForm.data['formMode'] == 'uploadError'):
        raise Exception("Something went wrong while uploading. Please try again.")

    if ('formFile' not in inputForm.data or inputForm.data["formFile"] == None):
        raise Exception("Input Fasta File is needed")

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

            raise Exception("Please ensure that every Restriction Enzyme has a partner.")

        if(inputFormClearedData['restrictionEnzyme' + str(firstRestrictionEnzyme)] != "" and
           inputFormClearedData['restrictionEnzyme' + str(secondRestrictionEnzyme)] != ""):
            chosenRestrictionEnzymePairs.append((restrictionEnzymes[int(inputFormClearedData['restrictionEnzyme' + str(firstRestrictionEnzyme)])],
                                                 restrictionEnzymes[int(inputFormClearedData['restrictionEnzyme' + str(secondRestrictionEnzyme)])]))

    if not chosenRestrictionEnzymePairs:
        raise Exception("Please select at least one pair, if you would like to use this option")

    return chosenRestrictionEnzymePairs

def explanationsViews(request):

    context = {'mode': 'none', 'explantionTexts': requestInformationTexts()}

    return render(request, "explanations.html", context)

class FastaFileUploadView(ChunkedUploadView):

    model = fastaFileUpload
    field_name = 'fastaFile'

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

class FastaFileUploadCompleteView(ChunkedUploadCompleteView):

    model = fastaFileUpload

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        # Do something with the uploaded file. E.g.:
        # * Store the uploaded file on another model:
        # SomeModel.objects.create(user=request.user, file=uploaded_file)
        # * Pass it as an argument to a function:
        # function_that_process_file(uploaded_file)
        pass


    def get_response_data(self, chunked_upload, request):
        return {'file': chunked_upload.file.name, 'filename': chunked_upload.filename}