from backend.service.CreateDigestion import doubleDigestDna
from backend.service.DigestedDnaComparison import DigestedDnaComparison
from backend.service.ExtractRestrictionEnzymes import extractRestrictionEnzymesFromNewEnglandList
from backend.service.HandleFastafile import readInFastaAndReturnOnlyFragments

def handleDDRadSeqRequest(inputFasta, restrictionEnzyme1, restrictionEnzyme2):

    digestedSequencesFromFasta = readInFastaAndReturnOnlyFragments(inputFasta, restrictionEnzyme1)
    doubleDigestedSequence = doubleDigestDna(digestedSequencesFromFasta, restrictionEnzyme1, restrictionEnzyme2)

    #doubleDigestedSequence.countFragmentInBins()

    return doubleDigestedSequence.createHistogrammOfDistribution()

def handleDDRadSeqComparisonRequest(inputFasta, restrictionEnzyme1, restrictionEnzyme2, restrictionEnzyme3, restrictionEnzyme4):

    digestedSequencesFromFasta = readInFastaAndReturnOnlyFragments(inputFasta, restrictionEnzyme1, restrictionEnzyme3)

    doubleDigestedSequence1 = doubleDigestDna(digestedSequencesFromFasta['digestedDNA'], restrictionEnzyme1, restrictionEnzyme2)
    doubleDigestedSequence2 = doubleDigestDna(digestedSequencesFromFasta['digestedDNA2'], restrictionEnzyme3, restrictionEnzyme4)

    digestedDnaComparison = DigestedDnaComparison(doubleDigestedSequence1, doubleDigestedSequence2)

    return digestedDnaComparison.createLineChart({"restrictionEnzyme1": restrictionEnzyme1.name, "restrictionEnzyme2": restrictionEnzyme2.name,
                                                  "restrictionEnzyme3": restrictionEnzyme3.name, "restrictionEnzyme4": restrictionEnzyme4.name})

def requestRestrictionEnzymes():

    return extractRestrictionEnzymesFromNewEnglandList()