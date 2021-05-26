import re
from DigestedDna import DigestedDna

def digestDna(dnaSequence, restrictionEnzyme):

	restrictionEnzymeCutSite = restrictionEnzyme.cutSite5end + restrictionEnzyme.cutSite3end

	dnaFragments = re.split(restrictionEnzymeCutSite, dnaSequence)

	return DigestedDna(dnaFragments)


def doubleDigestDna(dnaSequence, restrictionEnzyme1, restrictionEnzyme2):

	digestedDnaByFirstCutter = digestDna(dnaSequence, restrictionEnzyme1)

	allDigestedFragements = []

	for fragment in digestedDnaByFirstCutter.fragments:
		partiallyDigestedDnaBySecondCutter = digestDna(fragment, restrictionEnzyme2)
		allDigestedFragements.append(partiallyDigestedDnaBySecondCutter.fragments)

	fragmentsFlankedByTwoSites = filter(lambda fragment: fragment.startswith(restrictionEnzyme1.cutSite5end) and fragment.endswith(restrictionEnzyme2.cutSite3end)
														 or fragment.startswith(restrictionEnzyme2.cutSite5end) and fragment.endswith(restrictionEnzyme1.cutSite3end), allDigestedFragements)

	return DigestedDna(fragmentsFlankedByTwoSites)