import csv, os

from backend.models.RestrictionEnzyme import RestrictionEnzyme
from backend.settings import STATIC_ROOT


def extractRestrictionEnzymesFromNewEnglandList():

    with open(os.path.join(STATIC_ROOT,'restrictionEnzymes/newEnglandEnzymeList.csv'), encoding='utf-8-sig') as csvFile:
        csvDictReader = csv.DictReader(csvFile, delimiter=";")
        newEnglandEnzymeList = list(csvDictReader)

    filteredNewEnglandEnzymeList = list(filter(lambda enzyme: enzyme["Enzyme"] != "" and
                                                              enzyme["Sequence"] != "" and
                                                              all(character in "ACGT/" for character in enzyme["Sequence"]), newEnglandEnzymeList))

    filteredNewEnglandEnzymeList = removeAllHFFromList(filteredNewEnglandEnzymeList)
    allAvailableRestrictionEnzymes = list(map(lambda restrictionEnzyme: createRestrictionEnzymeObjectFromDictionary(restrictionEnzyme), filteredNewEnglandEnzymeList))

    return allAvailableRestrictionEnzymes

def removeAllHFFromList(enzymeList):

    for enzyme in enzymeList:
        enzyme.update((enzymeKey, enzymeValue[:enzymeValue.rfind("-HF")]) for enzymeKey, enzymeValue in enzyme.items())

    return sorted([dict(enzymeTuple) for enzymeTuple in {tuple(enzymes.items()) for enzymes in enzymeList}], key=lambda enzyme: enzyme['Enzyme'])

def createRestrictionEnzymeObjectFromDictionary(dictionaryOfRestrictionEnzyme):

    cutSites = dictionaryOfRestrictionEnzyme["Sequence"].split("/") if "/" in dictionaryOfRestrictionEnzyme["Sequence"] else [dictionaryOfRestrictionEnzyme["Sequence"][:int(len(dictionaryOfRestrictionEnzyme["Sequence"])/2)], dictionaryOfRestrictionEnzyme["Sequence"][int(len(dictionaryOfRestrictionEnzyme["Sequence"])/2):]]
    cutSite5end = cutSites[0]
    cutSite3end = cutSites[1] if cutSites[1] != "" else ""

    return RestrictionEnzyme(dictionaryOfRestrictionEnzyme["Enzyme"], cutSite5end, cutSite3end)

def getRestrictionEnzymeObjectByName(name):

    with open(os.path.join(STATIC_ROOT, 'restrictionEnzymes/newEnglandEnzymeList.csv'), encoding='utf-8-sig') as csvFile:
        csvDictReader = csv.DictReader(csvFile, delimiter=";")
        newEnglandEnzymeList = list(csvDictReader)

    queryRestrictionEnzyme = next(enzyme for enzyme in newEnglandEnzymeList if enzyme["Enzyme"] == name)

    return createRestrictionEnzymeObjectFromDictionary(queryRestrictionEnzyme)