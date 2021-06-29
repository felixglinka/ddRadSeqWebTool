import numpy as np

from backend.service.DigestedDna import DigestedDna
from backend.service.DigestedDnaComparison import DigestedDnaComparison
from backend.service.ExtractRestrictionEnzymes import extractRestrictionEnzymesFromNewEnglandList
from backend.service.HandleFastafile import readInFastaAndReturnOnlyFragments
from backend.settings import MAX_BINNING_LIMIT, BINNING_STEPS


def handleDDRadSeqRequest(inputFasta, restrictionEnzyme1, restrictionEnzyme2, selectedMinSize=None, selectedMaxSize=None, sequencingYield=None, coverage=None, sequenceLength=None, pairedEnd=None):

    restrictionEnzymeNames = {"firstRestrictionEnzyme": restrictionEnzyme1.name, "secondRestrictionEnzyme": restrictionEnzyme2.name}

    doubleDigestedSequencesFromFasta = readInFastaAndReturnOnlyFragments(inputFasta, restrictionEnzyme1, restrictionEnzyme2)
    doubleDigestedDna = DigestedDna(doubleDigestedSequencesFromFasta['digestedDNA']["digestedFragments"])
    doubleDigestedDna.setCutSizes(doubleDigestedSequencesFromFasta['digestedDNA']["cutByFirstRestrictionEnzyme"], doubleDigestedSequencesFromFasta['digestedDNA']["cutBySecondRestrictionEnzyme"])

    ranges = np.append(np.arange(0, MAX_BINNING_LIMIT+BINNING_STEPS, BINNING_STEPS), MAX_BINNING_LIMIT+BINNING_STEPS)
    doubleDigestedDna.createBasicDataframeForGraph(restrictionEnzymeNames, ranges)

    if sequencingYield == None and coverage == None:
        return {
            'graph': doubleDigestedDna.createLineChart(restrictionEnzymeNames, selectedMinSize, selectedMaxSize)
        }
    else:
        digestionGraph = doubleDigestedDna.createLineChart(restrictionEnzymeNames, selectedMinSize, selectedMaxSize)
        doubleDigestedDna.calculateBaseSequencingCosts(restrictionEnzymeNames, ranges, sequencingYield, coverage, sequenceLength, pairedEnd)
        return {
            'graph': digestionGraph,
            'dataFrame': doubleDigestedDna.fragmentCalculationDataframe.round().to_json()
        }


def handleDDRadSeqComparisonRequest(inputFasta, restrictionEnzyme1, restrictionEnzyme2, restrictionEnzyme3, restrictionEnzyme4, selectedMinSize=None, selectedMaxSize=None, sequencingYield=None, coverage=None, sequenceLength=None, pairedEnd=None):

    digestedSequencesFromFasta = readInFastaAndReturnOnlyFragments(inputFasta, restrictionEnzyme1, restrictionEnzyme2, restrictionEnzyme3, restrictionEnzyme4)
    restrictionEnzymeNames = {"restrictionEnzyme1": restrictionEnzyme1.name, "restrictionEnzyme2": restrictionEnzyme2.name, "restrictionEnzyme3": restrictionEnzyme3.name, "restrictionEnzyme4": restrictionEnzyme4.name}

    doubleDigestedDna1 = DigestedDna(digestedSequencesFromFasta['digestedDNA']['digestedFragments'])
    doubleDigestedDna1.setCutSizes(digestedSequencesFromFasta['digestedDNA']["cutByFirstRestrictionEnzyme"], digestedSequencesFromFasta['digestedDNA']["cutBySecondRestrictionEnzyme"])
    doubleDigestedDna2 = DigestedDna(digestedSequencesFromFasta['digestedDNA2']['digestedFragments'])
    doubleDigestedDna2.setCutSizes(digestedSequencesFromFasta['digestedDNA2']["cutByFirstRestrictionEnzyme"], digestedSequencesFromFasta['digestedDNA2']["cutBySecondRestrictionEnzyme"])

    digestedDnaComparison = DigestedDnaComparison(doubleDigestedDna1, doubleDigestedDna2)
    ranges = np.append(np.arange(0, MAX_BINNING_LIMIT + BINNING_STEPS, BINNING_STEPS), MAX_BINNING_LIMIT + BINNING_STEPS)
    digestedDnaComparison.setFragmentCalculationDataframe(restrictionEnzymeNames, ranges)

    if sequencingYield == None and coverage == None:
        return {
            'graph': digestedDnaComparison.createLineChart(restrictionEnzymeNames, selectedMinSize, selectedMaxSize)
        }
    else:
        digestedDnaComparison.digestedDna1.calculateBaseSequencingCosts(
            {"firstRestrictionEnzyme": restrictionEnzyme1.name, "secondRestrictionEnzyme": restrictionEnzyme2.name},
            ranges, sequencingYield, coverage, sequenceLength, pairedEnd)
        digestedDnaComparison.digestedDna2.calculateBaseSequencingCosts(
            {"firstRestrictionEnzyme": restrictionEnzyme3.name, "secondRestrictionEnzyme": restrictionEnzyme4.name},
            ranges, sequencingYield, coverage, sequenceLength, pairedEnd)
        return {
        'graph': digestedDnaComparison.createLineChart(restrictionEnzymeNames, selectedMinSize, selectedMaxSize),
        'dataFrame1': digestedDnaComparison.digestedDna1.fragmentCalculationDataframe.round().to_json(),
        'dataFrame2': digestedDnaComparison.digestedDna2.fragmentCalculationDataframe.round().to_json()
        }


def requestRestrictionEnzymes():

    return extractRestrictionEnzymesFromNewEnglandList()