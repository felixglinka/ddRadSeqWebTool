from backend.models.RestrictionEnzyme import RestrictionEnzyme
from backend.service.CreateDigestion import doubleDigestDna
from backend.service.HandleFastafile import readInFastaAndReturnOnlySequence

def handleDDRadSeqRequest(inputFasta):

    extractedSequencesFromFasta = readInFastaAndReturnOnlySequence(inputFasta)
    doubleDigestedSequence = doubleDigestDna(extractedSequencesFromFasta, EcoRI, BfaI)

    return doubleDigestedSequence.createHistogrammOfDistribution()

EcoRI = RestrictionEnzyme("EcoRI", "G" , "AATTC")
BfaI = RestrictionEnzyme("BfaI", "C" , "TAG")