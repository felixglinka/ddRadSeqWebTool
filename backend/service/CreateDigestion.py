import re
from DigestedDna import DigestedDna

def digestDna(dnaSequence, restrictionEnzyme):

	dnaFragments = re.split(restrictionEnzyme.cutSite5end + restrictionEnzyme.cutSite3end, dnaSequence)

	return DigestedDna(dnaFragments)


def doubleDigestDna(dnaSequence, restrictionEnzyme1, restrictionEnzyme2):

	return DigestedDna([])