import numpy as np

from backend.service.DigestedDna import DigestedDna


def digestSequence(dnaSequence, restrictionEnzyme):

    restrictionEnzymeCutSite = restrictionEnzyme.cutSite5end + restrictionEnzyme.cutSite3end
    restrictionEnzymeCutSitePattern = restrictionEnzyme.cutSite5end + '|' + restrictionEnzyme.cutSite3end

    return str(dnaSequence).replace(restrictionEnzymeCutSite, restrictionEnzymeCutSitePattern).split('|')



def doubleDigestDna(digestedDnaSequence, restrictionEnzyme1, restrictionEnzyme2):

    digestedDnaBySecondCutter = digestEveryDnaFragment(digestedDnaSequence, restrictionEnzyme2)

    fragmentsFlankedByTwoSites = list(filter(
        lambda fragment: fragment.startswith(restrictionEnzyme1.cutSite3end) and fragment.endswith(
            restrictionEnzyme2.cutSite5end)
                         or fragment.startswith(restrictionEnzyme2.cutSite3end) and fragment.endswith(
            restrictionEnzyme1.cutSite5end), digestedDnaBySecondCutter))

    finalDigestedDna = DigestedDna(fragmentsFlankedByTwoSites)
    finalDigestedDna.setCutSizes(len(digestedDnaSequence) - 1, len(digestedDnaBySecondCutter) - len(digestedDnaSequence))

    return finalDigestedDna

def digestEveryDnaFragment(digestedDnaByFirstCutter, restrictionEnzyme2):

    allDigestedFragments = []

    for fragment in digestedDnaByFirstCutter:
        partiallyDigestedDnaBySecondCutter = digestSequence(fragment, restrictionEnzyme2)
        allDigestedFragments.append(partiallyDigestedDnaBySecondCutter)

    return [fragment for fragments in allDigestedFragments for fragment in fragments]