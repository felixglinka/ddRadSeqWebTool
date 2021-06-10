import csv, os

from django.templatetags.static import static
from backend.models.RestrictionEnzyme import RestrictionEnzyme
from backend.settings import STATIC_ROOT


def extractRestrictionEnzymesFromNewEnglandList():

    with open(os.path.join(STATIC_ROOT,'restrictionEnzymes/newEnglandEnzymeList.csv'), encoding='utf-8-sig') as csvFile:
        csvDictReader = csv.DictReader(csvFile, delimiter=";")
        newEnglandEnzymeList = list(csvDictReader)

    filteredNewEnglandEnzymeList = list(filter(lambda enzyme: enzyme["Enzyme"] != "" and
                                                              enzyme["Cut Site"] != "" and
                                                              not enzyme["Cut Site"].startswith("/") and
                                                              not enzyme["Cut Site"].endswith("/") and
                                                              all(character in "ACGT/" for character in enzyme["Cut Site"]), newEnglandEnzymeList))

    allAvailableRestrictionEnzymes = list(map(lambda restrictionEnzyme: createRestrictionEnzymeObjectFromDictionary(restrictionEnzyme), filteredNewEnglandEnzymeList))

    return allAvailableRestrictionEnzymes

def createRestrictionEnzymeObjectFromDictionary(dictionaryOfRestrictionEnzyme):

    cutSites = dictionaryOfRestrictionEnzyme["Cut Site"].split("/")
    cutSite5end = cutSites[0]
    cutSite3end = cutSites[1]

    return RestrictionEnzyme(dictionaryOfRestrictionEnzyme["Enzyme"], cutSite5end, cutSite3end)