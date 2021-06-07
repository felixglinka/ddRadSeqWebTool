from backend.models.RestrictionEnzyme import RestrictionEnzyme
from backend.service.CreateDigestion import doubleDigestDna
from backend.service.ExtractRestrictionEnzymes import extractRestrictionEnzymesFromNewEnglandList
from backend.service.HandleFastafile import readInFastaAndReturnOnlySequence

def handleDDRadSeqRequest(inputFasta, restrictionEnzyme1, restrictionEnzyme2):

    extractedSequencesFromFasta = readInFastaAndReturnOnlySequence(inputFasta)
    doubleDigestedSequence = doubleDigestDna(extractedSequencesFromFasta, restrictionEnzyme1, restrictionEnzyme2)

    return doubleDigestedSequence.createHistogrammOfDistribution()

def requestRestrictionEnzymes():

    return extractRestrictionEnzymesFromNewEnglandList()