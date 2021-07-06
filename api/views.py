import io, logging, shutil

from backend.controller.ddRadtoolController import handleDDRadSeqRequest, requestRestrictionEnzymes, \
    handleDDRadSeqComparisonRequest
from backend.settings import PAIRED_END_ENDING, ILLUMINA_150
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

                if (inputForm.cleaned_data["basepairLengthToBeSequenced"] != "" and inputForm.cleaned_data["sequencingYield"] == "" and inputForm.cleaned_data["coverage"] == "" or
                    inputForm.cleaned_data["basepairLengthToBeSequenced"] != "" and inputForm.cleaned_data["sequencingYield"] != "" and inputForm.cleaned_data["coverage"] == "" or
                    inputForm.cleaned_data["basepairLengthToBeSequenced"] != "" and inputForm.cleaned_data["sequencingYield"] == "" and inputForm.cleaned_data["coverage"] != "" or
                    inputForm.cleaned_data["sequencingYield"] != "" and inputForm.cleaned_data["basepairLengthToBeSequenced"] == "" and inputForm.cleaned_data["coverage"] == "" or
                    inputForm.cleaned_data["sequencingYield"] != "" and inputForm.cleaned_data["basepairLengthToBeSequenced"] != "" and inputForm.cleaned_data["coverage"] == "" or
                    inputForm.cleaned_data["sequencingYield"] != "" and inputForm.cleaned_data["basepairLengthToBeSequenced"] == "" and inputForm.cleaned_data["coverage"] != "" or
                    inputForm.cleaned_data["coverage"] != "" and inputForm.cleaned_data["basepairLengthToBeSequenced"] == "" and inputForm.cleaned_data["sequencingYield"] == "" or
                    inputForm.cleaned_data["coverage"] != "" and inputForm.cleaned_data["basepairLengthToBeSequenced"] != "" and inputForm.cleaned_data["sequencingYield"] == "" or
                    inputForm.cleaned_data["coverage"] != "" and inputForm.cleaned_data["basepairLengthToBeSequenced"] == "" and inputForm.cleaned_data["sequencingYield"] != ""):
                    raise Exception("All sequence calculation parameters has to be chosen for calculation of sequence cost")

                if inputForm.cleaned_data["coverage"] != "" and int(inputForm.cleaned_data["coverage"]) == 0:
                    raise Exception("Coverage cannot be 0")

                context["graphHeight"] = "500"


                if inputForm.cleaned_data['restrictionEnzyme3'] == "" and inputForm.cleaned_data['restrictionEnzyme4'] == "":

                    if (inputForm.cleaned_data['sequencingYield'] != "" and inputForm.cleaned_data['coverage'] != ""):
                        ddRadSeqresult = handleDDRadSeqRequest(stringStreamFasta, restrictionEnzymes[
                            int(inputForm.cleaned_data['restrictionEnzyme1'])], restrictionEnzymes[
                                                                   int(inputForm.cleaned_data['restrictionEnzyme2'])],
                                                               int(inputForm.cleaned_data["sequencingYield"]),
                                                               int(inputForm.cleaned_data["coverage"]),
                                                               int(inputForm.cleaned_data['basepairLengthToBeSequenced']),
                                                               inputForm.cleaned_data['pairedEndChoice'])
                        context["dataFrame"] = ddRadSeqresult['dataFrame']
                        context["firstChosenRestrictionEnzymes"] = restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme1'])].name + '+' + restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme2'])].name
                        context["basepairLengthToBeSequenced"] = inputForm.cleaned_data['basepairLengthToBeSequenced']
                        context["pairedEndChoice"] = inputForm.cleaned_data['pairedEndChoice']
                        context["sequencingYield"] = inputForm.cleaned_data['sequencingYield']
                        context["coverage"] = inputForm.cleaned_data['coverage']

                    else:
                        ddRadSeqresult = handleDDRadSeqRequest(stringStreamFasta, restrictionEnzymes[
                            int(inputForm.cleaned_data['restrictionEnzyme1'])], restrictionEnzymes[
                                                                   int(inputForm.cleaned_data['restrictionEnzyme2'])])

                    context["graph"] = ddRadSeqresult['graph']

                elif inputForm.cleaned_data['restrictionEnzyme3'] == "" or inputForm.cleaned_data['restrictionEnzyme4'] == "":
                    raise Exception("Two restriction enzymes for comparison has to be chosen")

                else:

                    if (inputForm.cleaned_data['sequencingYield'] != "" and inputForm.cleaned_data['coverage'] != ""):
                        ddRadSeqComparisonResult = handleDDRadSeqComparisonRequest(stringStreamFasta, restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme1'])],
                                                    restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme2'])],
                                                    restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme3'])],
                                                    restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme4'])],                                                    int(inputForm.cleaned_data["sequencingYield"]), int(inputForm.cleaned_data["coverage"]),
                                                    int(inputForm.cleaned_data['basepairLengthToBeSequenced']), inputForm.cleaned_data['pairedEndChoice'])

                        context["dataFrame1"] = ddRadSeqComparisonResult['dataFrame1']
                        context["dataFrame2"] = ddRadSeqComparisonResult['dataFrame2']
                        context["firstChosenRestrictionEnzymes"] = restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme1'])].name + '+' + restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme2'])].name
                        context["secondChosenRestrictionEnzymes"] = restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme3'])].name + '+' + restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme4'])].name
                        context["basepairLengthToBeSequenced"] = inputForm.cleaned_data['basepairLengthToBeSequenced']
                        context["pairedEndChoice"] = inputForm.cleaned_data['pairedEndChoice']
                        context["sequencingYield"] = inputForm.cleaned_data['sequencingYield']
                        context["coverage"] = inputForm.cleaned_data['coverage']

                    else:
                        ddRadSeqComparisonResult = handleDDRadSeqComparisonRequest(stringStreamFasta,
                                                   restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme1'])],
                                                   restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme2'])],
                                                   restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme3'])],
                                                   restrictionEnzymes[int(inputForm.cleaned_data['restrictionEnzyme4'])])

                    context["graph"] = ddRadSeqComparisonResult['graph']

            except Exception as e:
                logger.error(e)
                messages.error(request, e)

        else:
            logger.error(inputForm.errors)

    context["form"] = BasicInputDDRadDataForm(initial={'pairedEndChoice': PAIRED_END_ENDING}, restrictionEnzymes=restrictionEnzymes)
    return render(request, "webinterface.html", context)