import logging
import numpy as np

from backend.service.DoubleDigestedDnaComparison import DoubleDigestedDnaComparison
from backend.service.ExtractRestrictionEnzymes import extractRestrictionEnzymesFromNewEnglandList, \
    getRestrictionEnzymeObjectByName
from backend.service.HandleFastafile import countFragmentLengthOfInputFasta, tryOutRareCutterAndFilterSmallest
from backend.service.ReadInJsonFiles import readInPopoverTexts, readInInformationTexts
from backend.settings import MAX_BINNING_LIMIT, BINNING_STEPS, COMMONLYUSEDECORIFREQUENTCUTTERS, \
    COMMONLYUSEDPSTIFREQUENTCUTTERS, COMMONLYUSEDSBFIFREQUENTCUTTERS, COMMONLYUSEDSPHIFREQUENTCUTTERS, \
    FIRST_BINNING_LIMIT, COMMONLYUSEDRARECUTTERS

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



def handlePopulationStructureRequest(inputFasta, numberOfSnps, expectPolyMorph, sequenceLength, pairedEnd, sequencingYield=None, coverage=None):

    try:

        binningSizes = np.append(np.arange(FIRST_BINNING_LIMIT, MAX_BINNING_LIMIT+BINNING_STEPS, BINNING_STEPS), MAX_BINNING_LIMIT+BINNING_STEPS)

        restrictionEnzymePairs = combineFrequentCuttersCutsWithRareCutterCut()

        doubleDigestedDnaComparison = DoubleDigestedDnaComparison(sequencingYield, coverage, sequenceLength, pairedEnd)
        doubleDigestedDnaComparison.createEmptyDataFrame(restrictionEnzymePairs, binningSizes)

        rareCutterCutsAndGenomeMutationAmount = tryOutRareCutterAndFilterSmallest(inputFasta, doubleDigestedDnaComparison, expectPolyMorph, sequenceLength, pairedEnd, numberOfSnps=numberOfSnps)

        restrictionEnzymePairList = doubleDigestedDnaComparison.filterFirstCutLessThanValue(rareCutterCutsAndGenomeMutationAmount[0])

        if doubleDigestedDnaComparison.sequencingCalculation:
            for restrictionEnzymePair in restrictionEnzymePairList:
                doubleDigestedDnaComparison.calculateBaseSequencingCosts(restrictionEnzymePair)

        doubleDigestedDnaComparison.filterSecondCutLessThanExpectedSNP(numberOfSnps, expectPolyMorph)
        doubleDigestedDnaComparison.filterSecondCutForTooManySNPs(numberOfSnps, expectPolyMorph)

        chosenRestrictionEnzymePairs = doubleDigestedDnaComparison.getRestrictionEnzymeList()

        if (doubleDigestedDnaComparison.digestedDnaCollectionDataframe.empty):
            return {}
        else:
            return {
                    'graph': doubleDigestedDnaComparison.createLineChart(chosenRestrictionEnzymePairs),
                    'dataFrames': doubleDigestedDnaComparison.prepareDataframeData()
                }

    except Exception as e:
        logger.error(e)

def handleGenomeScanRequest(inputFasta, genomeScanRadSnpDensity, expectPolyMorph, sequenceLength, pairedEnd, sequencingYield=None, coverage=None):

    try:

        binningSizes = np.append(np.arange(FIRST_BINNING_LIMIT, MAX_BINNING_LIMIT + BINNING_STEPS, BINNING_STEPS),
                                 MAX_BINNING_LIMIT + BINNING_STEPS)

        restrictionEnzymePairs = combineFrequentCuttersCutsWithRareCutterCut()

        doubleDigestedDnaComparison = DoubleDigestedDnaComparison(sequencingYield, coverage, sequenceLength, pairedEnd)
        doubleDigestedDnaComparison.createEmptyDataFrame(restrictionEnzymePairs, binningSizes)

        rareCutterCutsAndGenomeMutationAmount = tryOutRareCutterAndFilterSmallest(inputFasta,
                                                                                  doubleDigestedDnaComparison,
                                                                                  expectPolyMorph, sequenceLength,
                                                                                  pairedEnd, genomeScanRadSnpDensity=genomeScanRadSnpDensity)
        genomeMutationAmount = rareCutterCutsAndGenomeMutationAmount[1]

        restrictionEnzymePairList = doubleDigestedDnaComparison.filterFirstCutLessThanValue(
            rareCutterCutsAndGenomeMutationAmount[0])

        if doubleDigestedDnaComparison.sequencingCalculation:
            for restrictionEnzymePair in restrictionEnzymePairList:
                doubleDigestedDnaComparison.calculateBaseSequencingCosts(restrictionEnzymePair)

        doubleDigestedDnaComparison.filterSecondCutLessThanExpectedSNP(genomeMutationAmount, expectPolyMorph)
        doubleDigestedDnaComparison.filterSecondCutForTooManySNPs(genomeMutationAmount, expectPolyMorph)

        chosenRestrictionEnzymePairs = doubleDigestedDnaComparison.getRestrictionEnzymeList()

        if (doubleDigestedDnaComparison.digestedDnaCollectionDataframe.empty):
            return {
                'expectedNumberOfSnps': 1
            }
        else:
            return {
                'graph': doubleDigestedDnaComparison.createLineChart(chosenRestrictionEnzymePairs),
                'dataFrames': doubleDigestedDnaComparison.prepareDataframeData(),
                'expectedNumberOfSnps': rareCutterCutsAndGenomeMutationAmount[1]
            }

    except Exception as e:
        logger.error(e)

def combineFrequentCuttersCutsWithRareCutterCut():

    enzymePairsToDoubleDigest = []

    for rareCutter in COMMONLYUSEDRARECUTTERS:

        if rareCutter == 'EcoRI':
            for frequentCutter in COMMONLYUSEDECORIFREQUENTCUTTERS:
                enzymePairsToDoubleDigest.append(rareCutter + '+' + frequentCutter)

        if rareCutter == 'PstI':
            for frequentCutter in COMMONLYUSEDPSTIFREQUENTCUTTERS:
                enzymePairsToDoubleDigest.append(rareCutter + '+' + frequentCutter)

        if rareCutter == 'SbfI':
            for frequentCutter in COMMONLYUSEDSBFIFREQUENTCUTTERS:
                enzymePairsToDoubleDigest.append(rareCutter + '+' + frequentCutter)

        if rareCutter == 'SphI':
            for frequentCutter in COMMONLYUSEDSPHIFREQUENTCUTTERS:
                enzymePairsToDoubleDigest.append(rareCutter + '+' + frequentCutter)

    return enzymePairsToDoubleDigest

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