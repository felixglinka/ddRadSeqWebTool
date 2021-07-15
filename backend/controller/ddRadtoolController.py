import numpy as np

from backend.service.DigestedDna import DigestedDna
from backend.service.DigestedDnaComparison import DigestedDnaComparison
from backend.service.ExtractRestrictionEnzymes import extractRestrictionEnzymesFromNewEnglandList
from backend.service.HandleFastafile import readInFastaAndReturnOnlyFragments
from backend.settings import MAX_BINNING_LIMIT, BINNING_STEPS

def handleDDRadSeqRequest(inputFasta, restrictionEnzymePairList, sequencingYield=None, coverage=None, sequenceLength=None, pairedEnd=None):

    binningSizes = np.append(np.arange(0, MAX_BINNING_LIMIT+BINNING_STEPS, BINNING_STEPS), MAX_BINNING_LIMIT+BINNING_STEPS)

    doubleDigestedSequencesFromFasta = readInFastaAndReturnOnlyFragments(inputFasta, restrictionEnzymePairList)
    doubleDigestedDnaCollection = fragmentDictToDigestedDnaCollection(doubleDigestedSequencesFromFasta)
    digestedDnaComparison = DigestedDnaComparison(doubleDigestedDnaCollection)
    digestedDnaComparison.setFragmentCalculationDataframe(binningSizes)

    if sequencingYield == None and coverage == None:
        return {
            'graph': digestedDnaComparison.createLineChart()
        }
    else:
        return {
            'graph': digestedDnaComparison.createLineChart(),
            'dataFrames': [digestedDna.fragmentCalculationDataframe.round().to_json() for digestedDna in digestedDnaComparison.DigestedDnaCollection],
        }

def fragmentDictToDigestedDnaCollection(doubleDigestedSequencesFromFasta):

    listOfDigestedDna = []

    for enzymeName in doubleDigestedSequencesFromFasta.keys():
        listOfDigestedDna.append(DigestedDna(enzymeName, doubleDigestedSequencesFromFasta[enzymeName]))

    return listOfDigestedDna

def requestRestrictionEnzymes():

    return extractRestrictionEnzymesFromNewEnglandList()