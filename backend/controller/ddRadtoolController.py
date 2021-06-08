from backend.models.RestrictionEnzyme import RestrictionEnzyme
from backend.service.CreateDigestion import doubleDigestDna
from backend.service.ExtractRestrictionEnzymes import extractRestrictionEnzymesFromNewEnglandList
from backend.service.HandleFastafile import readInFastaAndReturnOnlySequence

def handleDDRadSeqRequest(inputFasta, restrictionEnzyme1, restrictionEnzyme2):

    extractedSequencesFromFasta = readInFastaAndReturnOnlySequence(inputFasta)
    doubleDigestedSequence = doubleDigestDna(extractedSequencesFromFasta, restrictionEnzyme1, restrictionEnzyme2)

    doubleDigestedSequence.countFragmentInBins()

    return doubleDigestedSequence.createHistogrammOfDistribution()

def handleDDRadSeqComparisonRequest(inputFasta, restrictionEnzyme1, restrictionEnzyme2, restrictionEnzyme3, restrictionEnzyme4):

    extractedSequencesFromFasta = readInFastaAndReturnOnlySequence(inputFasta)

    doubleDigestedSequence1 = doubleDigestDna(extractedSequencesFromFasta, restrictionEnzyme1, restrictionEnzyme2)
    doubleDigestedSequence2 = doubleDigestDna(extractedSequencesFromFasta, restrictionEnzyme1, restrictionEnzyme2)

    return ''

def requestRestrictionEnzymes():

    return extractRestrictionEnzymesFromNewEnglandList()