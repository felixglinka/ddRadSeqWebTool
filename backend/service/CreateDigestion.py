import re
import numpy as np
from DigestedDna import DigestedDna

def digestDna(dnaSequence, restrictionEnzyme):

	restrictionEnzymeCutSite = restrictionEnzyme.cutSite5end + restrictionEnzyme.cutSite3end
	restrictionEnzymeCutSitePattern = restrictionEnzyme.cutSite5end + '|' + restrictionEnzyme.cutSite3end

	dnaFragments = dnaSequence.replace(restrictionEnzymeCutSite, restrictionEnzymeCutSitePattern).split('|')

	return DigestedDna(dnaFragments)


def doubleDigestDna(dnaSequence, restrictionEnzyme1, restrictionEnzyme2):

	digestedDnaByFirstCutter = digestDna(dnaSequence, restrictionEnzyme1)

	allDigestedFragments = []

	for fragment in digestedDnaByFirstCutter.fragments:
		partiallyDigestedDnaBySecondCutter = digestDna(fragment, restrictionEnzyme2)
		allDigestedFragments.append(partiallyDigestedDnaBySecondCutter.fragments)

	allDigestedFragments = list(np.concatenate(allDigestedFragments).flat)

	fragmentsFlankedByTwoSites = filter(lambda fragment: fragment.startswith(restrictionEnzyme1.cutSite3end) and fragment.endswith(restrictionEnzyme2.cutSite5end)
														 or fragment.startswith(restrictionEnzyme2.cutSite3end) and fragment.endswith(restrictionEnzyme1.cutSite5end), allDigestedFragments)

	return DigestedDna(fragmentsFlankedByTwoSites)