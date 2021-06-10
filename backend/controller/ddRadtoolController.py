from backend.service.DigestedDna import DigestedDna
from backend.service.DigestedDnaComparison import DigestedDnaComparison
from backend.service.ExtractRestrictionEnzymes import extractRestrictionEnzymesFromNewEnglandList
from backend.service.HandleFastafile import readInFastaAndReturnOnlyFragments

def handleDDRadSeqRequest(inputFasta, restrictionEnzyme1, restrictionEnzyme2):

    doubleDigestedSequencesFromFasta = readInFastaAndReturnOnlyFragments(inputFasta, restrictionEnzyme1, restrictionEnzyme2)
    doubleDigestedDna = DigestedDna(doubleDigestedSequencesFromFasta['digestedDNA']["digestedFragments"])
    doubleDigestedDna.setCutSizes(doubleDigestedSequencesFromFasta['digestedDNA']["cutByFirstRestrictionEnzyme"], doubleDigestedSequencesFromFasta['digestedDNA']["cutBySecondRestrictionEnzyme"])

    #doubleDigestedDna.countFragmentInBins()

    return doubleDigestedDna.createHistogrammOfDistribution()

def handleDDRadSeqComparisonRequest(inputFasta, restrictionEnzyme1, restrictionEnzyme2, restrictionEnzyme3, restrictionEnzyme4):

    digestedSequencesFromFasta = readInFastaAndReturnOnlyFragments(inputFasta, restrictionEnzyme1, restrictionEnzyme2, restrictionEnzyme3, restrictionEnzyme4)

    doubleDigestedDna1 = DigestedDna(digestedSequencesFromFasta['digestedDNA']['digestedFragments'])
    doubleDigestedDna1.setCutSizes(digestedSequencesFromFasta['digestedDNA']["cutByFirstRestrictionEnzyme"], digestedSequencesFromFasta['digestedDNA']["cutBySecondRestrictionEnzyme"])
    doubleDigestedDna2 = DigestedDna(digestedSequencesFromFasta['digestedDNA2']['digestedFragments'])
    doubleDigestedDna2.setCutSizes(digestedSequencesFromFasta['digestedDNA2']["cutByFirstRestrictionEnzyme"], digestedSequencesFromFasta['digestedDNA2']["cutBySecondRestrictionEnzyme"])


    digestedDnaComparison = DigestedDnaComparison(doubleDigestedDna1, doubleDigestedDna2)

    return digestedDnaComparison.createLineChart({"restrictionEnzyme1": restrictionEnzyme1.name, "restrictionEnzyme2": restrictionEnzyme2.name,
                                                  "restrictionEnzyme3": restrictionEnzyme3.name, "restrictionEnzyme4": restrictionEnzyme4.name})

def requestRestrictionEnzymes():

    return extractRestrictionEnzymesFromNewEnglandList()