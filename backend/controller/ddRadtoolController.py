from backend.service.DigestedDna import DigestedDna
from backend.service.DigestedDnaComparison import DigestedDnaComparison
from backend.service.ExtractRestrictionEnzymes import extractRestrictionEnzymesFromNewEnglandList
from backend.service.HandleFastafile import readInFastaAndReturnOnlyFragments

def handleDDRadSeqRequest(inputFasta, restrictionEnzyme1, restrictionEnzyme2, selectedMinSize=None, selectedMaxSize=None):

    restrictionEnzymeNames = {"firstRestrictionEnzyme": restrictionEnzyme1.name, "secondRestrictionEnzyme": restrictionEnzyme2.name}

    doubleDigestedSequencesFromFasta = readInFastaAndReturnOnlyFragments(inputFasta, restrictionEnzyme1, restrictionEnzyme2)
    doubleDigestedDna = DigestedDna(doubleDigestedSequencesFromFasta['digestedDNA']["digestedFragments"])
    doubleDigestedDna.setCutSizes(doubleDigestedSequencesFromFasta['digestedDNA']["cutByFirstRestrictionEnzyme"], doubleDigestedSequencesFromFasta['digestedDNA']["cutBySecondRestrictionEnzyme"])

    digestedDnaBins = doubleDigestedDna.calculateIlluminaValues(restrictionEnzymeNames)

    return {
        'graph': doubleDigestedDna.createLineChart(digestedDnaBins[[restrictionEnzyme1.name + '+' + restrictionEnzyme2.name]], restrictionEnzymeNames, selectedMinSize, selectedMaxSize),
        'dataFrame': digestedDnaBins.iloc[:,2:].to_json()
    }


def handleDDRadSeqComparisonRequest(inputFasta, restrictionEnzyme1, restrictionEnzyme2, restrictionEnzyme3, restrictionEnzyme4, selectedMinSize=None, selectedMaxSize=None):

    digestedSequencesFromFasta = readInFastaAndReturnOnlyFragments(inputFasta, restrictionEnzyme1, restrictionEnzyme2, restrictionEnzyme3, restrictionEnzyme4)

    doubleDigestedDna1 = DigestedDna(digestedSequencesFromFasta['digestedDNA']['digestedFragments'])
    doubleDigestedDna1.setCutSizes(digestedSequencesFromFasta['digestedDNA']["cutByFirstRestrictionEnzyme"], digestedSequencesFromFasta['digestedDNA']["cutBySecondRestrictionEnzyme"])
    doubleDigestedDna2 = DigestedDna(digestedSequencesFromFasta['digestedDNA2']['digestedFragments'])
    doubleDigestedDna2.setCutSizes(digestedSequencesFromFasta['digestedDNA2']["cutByFirstRestrictionEnzyme"], digestedSequencesFromFasta['digestedDNA2']["cutBySecondRestrictionEnzyme"])

    digestedDnaComparison = DigestedDnaComparison(doubleDigestedDna1, doubleDigestedDna2)

    digestedDna1Bins=doubleDigestedDna1.calculateIlluminaValues({"firstRestrictionEnzyme": restrictionEnzyme1.name, "secondRestrictionEnzyme": restrictionEnzyme2.name})
    digestedDna2Bins=doubleDigestedDna2.calculateIlluminaValues({"firstRestrictionEnzyme": restrictionEnzyme3.name, "secondRestrictionEnzyme": restrictionEnzyme4.name})

    return {
        'graph': digestedDnaComparison.createLineChart(digestedDna1Bins[[restrictionEnzyme1.name + '+' + restrictionEnzyme2.name]], digestedDna2Bins[[restrictionEnzyme3.name + '+' + restrictionEnzyme4.name]],
                                                 {"restrictionEnzyme1": restrictionEnzyme1.name, "restrictionEnzyme2": restrictionEnzyme2.name,
                                                  "restrictionEnzyme3": restrictionEnzyme3.name, "restrictionEnzyme4": restrictionEnzyme4.name},
                                                 selectedMinSize, selectedMaxSize),
        'dataFrame1': digestedDna1Bins.iloc[:,2:].to_json(),
        'dataFrame2': digestedDna2Bins.iloc[:,2:].to_json()
    }


def requestRestrictionEnzymes():

    return extractRestrictionEnzymesFromNewEnglandList()