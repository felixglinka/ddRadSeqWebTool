import numpy as np

from backend.service.DoubleDigestedDna import DoubleDigestedDna
from backend.service.DoubleDigestedDnaComparison import DoubleDigestedDnaComparison
from backend.service.ExtractRestrictionEnzymes import extractRestrictionEnzymesFromNewEnglandList, \
    getRestrictionEnzymeObjectByName
from backend.service.HandleFastafile import countFragmentLengthOfInputFasta, tryOutRareCutterAndFilterSmallest
from backend.settings import MAX_BINNING_LIMIT, BINNING_STEPS, COMMONLYUSEDFREQUENTCUTTERS


def handleDDRadSeqRequest(inputFasta, restrictionEnzymePairList, sequencingYield=None, coverage=None, sequenceLength=None, pairedEnd=None):

    binningSizes = np.append(np.arange(0, MAX_BINNING_LIMIT+BINNING_STEPS, BINNING_STEPS), MAX_BINNING_LIMIT+BINNING_STEPS)

    doubleDigestedSequencesFromFasta = countFragmentLengthOfInputFasta(inputFasta, restrictionEnzymePairList)
    doubleDigestedDnaCollection = fragmentDictToDigestedDnaCollection(doubleDigestedSequencesFromFasta)
    digestedDnaComparison = DoubleDigestedDnaComparison(doubleDigestedDnaCollection)
    digestedDnaComparison.setFragmentCalculationDataframe(binningSizes, sequenceLength, pairedEnd)

    if sequencingYield == None and coverage == None:
        return {
            'graph': digestedDnaComparison.createLineChart()
        }
    else:
        return {
            'graph': digestedDnaComparison.createLineChart(),
            'dataFrames': [digestedDna.fragmentCalculationDataframe.round().to_json() for digestedDna in digestedDnaComparison.DigestedDnaCollection],
        }

def handlePopulationStructureRequest(inputFasta, numberOfSnps, expectPolyMorph, sequenceLength, pairedEnd):

    binningSizes = np.append(np.arange(0, MAX_BINNING_LIMIT+BINNING_STEPS, BINNING_STEPS), MAX_BINNING_LIMIT+BINNING_STEPS)

    rareCutterCuts = tryOutRareCutterAndFilterSmallest(inputFasta, numberOfSnps, expectPolyMorph, sequenceLength, pairedEnd)
    doubleDigestedDnaCollection = combineFrequentCuttersCutsWithRareCutterCut(rareCutterCuts)
    digestedDnaComparison = DoubleDigestedDnaComparison(doubleDigestedDnaCollection)
    digestedDnaComparison.setFragmentCalculationDataframe(binningSizes, sequenceLength, pairedEnd)

    return {
        'graph': digestedDnaComparison.createLineChart(),
        'dataFrames': [digestedDna.fragmentCalculationDataframe.round().to_json() for digestedDna in
                       digestedDnaComparison.DigestedDnaCollection],
    }


def fragmentDictToDigestedDnaCollection(doubleDigestedSequencesFromFasta):

    listOfDigestedDna = []

    for enzymeName in doubleDigestedSequencesFromFasta.keys():
        listOfDigestedDna.append(DoubleDigestedDna(enzymeName, doubleDigestedSequencesFromFasta[enzymeName]))

    return listOfDigestedDna


def combineFrequentCuttersCutsWithRareCutterCut(rareCutterCuts):

    listOfDoubleDigestedDna = []

    for rareCutterCut in rareCutterCuts.values():
        for frequentCutter in COMMONLYUSEDFREQUENTCUTTERS:
            listOfDoubleDigestedDna.append(rareCutterCut.digestDnaSecondTime(getRestrictionEnzymeObjectByName(frequentCutter)))

    return listOfDoubleDigestedDna

def requestRestrictionEnzymes():

    return extractRestrictionEnzymesFromNewEnglandList()