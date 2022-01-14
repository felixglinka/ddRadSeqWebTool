import logging
import numpy as np

from backend.service.DoubleDigestedDnaComparison import DoubleDigestedDnaComparison
from backend.service.ExtractRestrictionEnzymes import extractRestrictionEnzymesFromNewEnglandList, \
    getRestrictionEnzymeObjectByName
from backend.service.HandleFastafile import countFragmentLengthOfInputFasta, tryOutRareCutterAndFilterSmallest
from backend.service.ReadInJsonFiles import readInPopoverTexts, readInInformationTexts
from backend.settings import MAX_BINNING_LIMIT, BINNING_STEPS, COMMONLYUSEDECORIFREQUENTCUTTERS, \
    COMMONLYUSEDPSTIFREQUENTCUTTERS, COMMONLYUSEDSBFIFREQUENTCUTTERS, COMMONLYUSEDSPHIFREQUENTCUTTERS, \
    FIRST_BINNING_LIMIT

logger = logging.getLogger(__name__)


def handleDDRadSeqRequest(inputFasta, restrictionEnzymePairList, sequencingYield=None, coverage=None, sequenceLength=None, pairedEnd=None):

    try:

        binningSizes = np.append(np.arange(FIRST_BINNING_LIMIT, MAX_BINNING_LIMIT+BINNING_STEPS, BINNING_STEPS), MAX_BINNING_LIMIT+BINNING_STEPS)
        restrictionEnzymePairs = collectRestrictionEnzymePairs(restrictionEnzymePairList)

        doubleDigestedDnaComparison = DoubleDigestedDnaComparison(sequencingYield, coverage, sequenceLength, pairedEnd)
        doubleDigestedDnaComparison.createEmptyDataFrame(restrictionEnzymePairs, binningSizes)

        countFragmentLengthOfInputFasta(inputFasta, restrictionEnzymePairList, doubleDigestedDnaComparison)
        if doubleDigestedDnaComparison.sequencingCalculation:
            for restrictionEnzymePair in restrictionEnzymePairs:
                doubleDigestedDnaComparison.calculateBaseSequencingCosts(restrictionEnzymePair)

        if not doubleDigestedDnaComparison.sequencingCalculation:
            return {
                'graph': doubleDigestedDnaComparison.createLineChart(restrictionEnzymePairs)
            }
        else:
            return {
                'graph': doubleDigestedDnaComparison.createLineChart(restrictionEnzymePairs),
                'dataFrames': doubleDigestedDnaComparison.prepareDataframeData()
            }

    except Exception as e:
        logger.error(e)

def handlePopulationStructureRequest():
    return 0

def handleGenomeScanRequest():
    return 0

def handlePopulationStructureRequest(inputFasta, numberOfSnps, expectPolyMorph, sequenceLength, pairedEnd):

    try:

        binningSizes = np.append(np.arange(0, MAX_BINNING_LIMIT+BINNING_STEPS, BINNING_STEPS), MAX_BINNING_LIMIT+BINNING_STEPS)

        rareCutterCutsAndGenomeMutationAmount = tryOutRareCutterAndFilterSmallest(inputFasta, expectPolyMorph, sequenceLength, pairedEnd, numberOfSnps=numberOfSnps)
        # doubleDigestedDnaCollection = combineFrequentCuttersCutsWithRareCutterCut(rareCutterCutsAndGenomeMutationAmount[0])
        # digestedDnaComparison = DoubleDigestedDnaComparison(doubleDigestedDnaCollection)
        # digestedDnaComparison.setFragmentCalculationDataframe(binningSizes, sequenceLength, pairedEnd)
        # digestedDnaComparison.filterSecondCutLessThanExpectedSNP(numberOfSnps, expectPolyMorph, pairedEnd)
        # digestedDnaComparison.filterSecondCutForTooManySNPs(numberOfSnps, expectPolyMorph, pairedEnd)
        #
        # if(len(digestedDnaComparison.DigestedDnaCollection) >= 1):
        #     return {
        #         'graph': digestedDnaComparison.createLineChart(),
        #         'dataFrames':  [digestedDna.fragmentCalculationDataframe.round().to_json() for digestedDna in digestedDnaComparison.DigestedDnaCollection]
        #     }
        # else:
        #     return {}

    except Exception as e:
        logger.error(e)
#
# def handleGenomeScanRequest(inputFasta, genomeScanRadSnpDensity, expectPolyMorph, sequenceLength, pairedEnd):
#
#     try:
#
#         binningSizes = np.append(np.arange(0, MAX_BINNING_LIMIT + BINNING_STEPS, BINNING_STEPS),
#                                  MAX_BINNING_LIMIT + BINNING_STEPS)
#
#         rareCutterCutsAndGenomeMutationAmount = tryOutRareCutterAndFilterSmallest(inputFasta, expectPolyMorph, sequenceLength, pairedEnd, genomeScanRadSnpDensity=genomeScanRadSnpDensity)
#         genomeMutationAmount = rareCutterCutsAndGenomeMutationAmount[1]
#         doubleDigestedDnaCollection = combineFrequentCuttersCutsWithRareCutterCut(rareCutterCutsAndGenomeMutationAmount[0])
#         digestedDnaComparison = DoubleDigestedDnaComparison(doubleDigestedDnaCollection)
#         digestedDnaComparison.setFragmentCalculationDataframe(binningSizes, sequenceLength, pairedEnd)
#         digestedDnaComparison.filterSecondCutLessThanExpectedSNP(genomeMutationAmount, expectPolyMorph, pairedEnd)
#         digestedDnaComparison.filterSecondCutForTooManySNPs(genomeMutationAmount, expectPolyMorph, pairedEnd)
#
#         if (len(digestedDnaComparison.DigestedDnaCollection) >= 1):
#             return {
#                 'graph': digestedDnaComparison.createLineChart(),
#                 'dataFrames': [digestedDna.fragmentCalculationDataframe.round().to_json() for digestedDna in
#                                digestedDnaComparison.DigestedDnaCollection],
#                 'expectedNumberOfSnps': rareCutterCutsAndGenomeMutationAmount[1]
#             }
#         else:
#             return {
#                 'expectedNumberOfSnps': 1
#             }
#
#     except Exception as e:
#         logger.error(e)
#
#
#
# def combineFrequentCuttersCutsWithRareCutterCut(rareCutterCuts):
#
#     listOfDoubleDigestedDna = []
#
#     for rareCutterCut in rareCutterCuts.values():
#
#         storedRestrictionEnzymes = [doubleDigestedDna.restrictionEnzymeCombination for doubleDigestedDna in listOfDoubleDigestedDna]
#
#         if rareCutterCut.name == 'EcoRI':
#             for frequentCutter in COMMONLYUSEDECORIFREQUENTCUTTERS:
#                 if(frequentCutter + '+' + rareCutterCut.name not in storedRestrictionEnzymes):
#                     listOfDoubleDigestedDna.append(rareCutterCut.digestDnaSecondTime(getRestrictionEnzymeObjectByName(frequentCutter)))
#
#         if rareCutterCut.name == 'PstI':
#             for frequentCutter in COMMONLYUSEDPSTIFREQUENTCUTTERS:
#                 if(frequentCutter + '+' + rareCutterCut.name not in storedRestrictionEnzymes):
#                     listOfDoubleDigestedDna.append(rareCutterCut.digestDnaSecondTime(getRestrictionEnzymeObjectByName(frequentCutter)))
#
#         if rareCutterCut.name == 'SbfI':
#             for frequentCutter in COMMONLYUSEDSBFIFREQUENTCUTTERS:
#                 if(frequentCutter + '+' + rareCutterCut.name not in storedRestrictionEnzymes):
#                     listOfDoubleDigestedDna.append(rareCutterCut.digestDnaSecondTime(getRestrictionEnzymeObjectByName(frequentCutter)))
#
#         if rareCutterCut.name == 'SphI':
#             for frequentCutter in COMMONLYUSEDSPHIFREQUENTCUTTERS:
#                 if(frequentCutter + '+' + rareCutterCut.name not in storedRestrictionEnzymes):
#                     listOfDoubleDigestedDna.append(rareCutterCut.digestDnaSecondTime(getRestrictionEnzymeObjectByName(frequentCutter)))
#
#     return listOfDoubleDigestedDna
#

def collectRestrictionEnzymePairs(restrictionEnzymePairList):

    restrictionEnzymePairs = []

    for restrictionEnzymePair in restrictionEnzymePairList:
        restrictionEnzymePairs.append(restrictionEnzymePair[0].name + '+' + restrictionEnzymePair[1].name)

    return restrictionEnzymePairs

def requestRestrictionEnzymes():

    return extractRestrictionEnzymesFromNewEnglandList()

def requestPopoverTexts():

    return readInPopoverTexts()

def requestInformationTexts():

    return readInInformationTexts()