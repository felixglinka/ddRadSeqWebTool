import csv

from backend.models.RestrictionEnzyme import RestrictionEnzyme

def extractRestrictionEnzymesFromNewEnglandList():

    with open('../../newEnglandEnzymeList.csv', encoding='utf-8-sig') as csvFile:
        csvDictReader = csv.DictReader(csvFile, delimiter=";")
        newEnglandEnzymeList = list(csvDictReader)

    filteredNewEnglandEnzymeList = list(filter(lambda enzyme: enzyme["Enzyme"] != "" and enzyme["Cut Site"] != "" and all(character in "ACGT/" for character in enzyme["Cut Site"]), newEnglandEnzymeList))

    allAvailableRestrictionEnzymes = list(map(lambda restrictionEnzyme: createRestrictionEnzymeObjectFromDictionary(restrictionEnzyme), filteredNewEnglandEnzymeList))

    return allAvailableRestrictionEnzymes

def createRestrictionEnzymeObjectFromDictionary(dictionaryOfRestrictionEnzyme):

    cutSites = dictionaryOfRestrictionEnzyme["Cut Site"].split("/")
    cutSite5end = cutSites[0]
    cutSite3end = cutSites[1]

    return RestrictionEnzyme(dictionaryOfRestrictionEnzyme["Enzyme"], cutSite5end, cutSite3end)