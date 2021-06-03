import re
import numpy as np

from backend.service.DigestedDna import DigestedDna


def digestDna(dnaSequence, restrictionEnzyme):

    restrictionEnzymeCutSite = restrictionEnzyme.cutSite5end + restrictionEnzyme.cutSite3end
    restrictionEnzymeCutSitePattern = restrictionEnzyme.cutSite5end + '|' + restrictionEnzyme.cutSite3end

    dnaFragments = dnaSequence.replace(restrictionEnzymeCutSite, restrictionEnzymeCutSitePattern).split('|')

    return DigestedDna(dnaFragments)


def doubleDigestDna(dnaSequence, restrictionEnzyme1, restrictionEnzyme2):

    digestedDnaByFirstCutter = digestDna(dnaSequence, restrictionEnzyme1)
    digestedDnaBySecondCutter = digestEveryDnaFragment(digestedDnaByFirstCutter, restrictionEnzyme2)

    fragmentsFlankedByTwoSites = list(filter(
        lambda fragment: fragment.startswith(restrictionEnzyme1.cutSite3end) and fragment.endswith(
            restrictionEnzyme2.cutSite5end)
                         or fragment.startswith(restrictionEnzyme2.cutSite3end) and fragment.endswith(
            restrictionEnzyme1.cutSite5end), digestedDnaBySecondCutter))

    finalDigestedDna = DigestedDna(fragmentsFlankedByTwoSites)
    finalDigestedDna.cutByFirstRestrictionEnzyme = len(digestedDnaByFirstCutter.fragments) - 1
    finalDigestedDna.cutBySecondRestrictionEnzyme = len(digestedDnaBySecondCutter) - len(digestedDnaByFirstCutter.fragments)

    return finalDigestedDna

def digestEveryDnaFragment(digestedDnaByFirstCutter, restrictionEnzyme):

    allDigestedFragments = []

    for fragment in digestedDnaByFirstCutter.fragments:
        partiallyDigestedDnaBySecondCutter = digestDna(fragment, restrictionEnzyme)
        allDigestedFragments.append(partiallyDigestedDnaBySecondCutter.fragments)

    return list(np.concatenate(allDigestedFragments).flat)