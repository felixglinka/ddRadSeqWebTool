import regex as re

from backend.settings import MAX_BINNING_LIMIT, BINNING_STEPS, PAIRED_END_ENDING, FIRST_BINNING_LIMIT


class DigestSequence:

    def __init__(self, dnaSequence, restrictionEnzymes):

        self.restrictionEnzymePositions = None
        self.dnaSequence = dnaSequence
        self.restrictionEnzymes = restrictionEnzymes
        self.restrictionEnzymePositions = tuple((f.group(1), f.start(1)) for f in
                                                re.finditer(r'(' + '|'.join(self.restrictionEnzymes) + r')', self.dnaSequence, overlapped=True))

    def addFragmentToSizeTable(self, firstRestrictionEnzyme, secondRestrictionEnzyme, digestedDnaCollectionDataframe):

        restrictionEnzymeCombination = firstRestrictionEnzyme.name + '+' + secondRestrictionEnzyme.name

        filteredRestrictionEnzymePositions = list(filter(lambda enzymeCut: enzymeCut[0] == firstRestrictionEnzyme.getCompleteCutSite() or enzymeCut[0] == secondRestrictionEnzyme.getCompleteCutSite(),
                                      self.restrictionEnzymePositions))

        bins = tuple(digestedDnaCollectionDataframe.index)

        for previousPosition, currentPostion in zip(filteredRestrictionEnzymePositions, filteredRestrictionEnzymePositions[1:]):
            if(previousPosition[0] != currentPostion[0]):
                fragmentLength = currentPostion[1] - previousPosition[1] + len(self.getEnzymeByCompleteCutSide(currentPostion[0], firstRestrictionEnzyme, secondRestrictionEnzyme).cutSite5end) - len(self.getEnzymeByCompleteCutSide(previousPosition[0], firstRestrictionEnzyme, secondRestrictionEnzyme).cutSite5end)
                if(fragmentLength <= MAX_BINNING_LIMIT+BINNING_STEPS):
                    for index, bin in enumerate(bins):
                            if fragmentLength <= FIRST_BINNING_LIMIT:
                                digestedDnaCollectionDataframe.loc[FIRST_BINNING_LIMIT, restrictionEnzymeCombination] += 1
                                break
                            if fragmentLength > bin and fragmentLength <= bins[index + 1]:
                                digestedDnaCollectionDataframe.loc[bins[index + 1], restrictionEnzymeCombination] += 1
                                break

    def getEnzymeByCompleteCutSide(self, query, firstRestrictionEnzyme, secondRestrictionEnzyme):

        if(query == firstRestrictionEnzyme.getCompleteCutSite()):
            return firstRestrictionEnzyme
        if (query == secondRestrictionEnzyme.getCompleteCutSite()):
            return secondRestrictionEnzyme

def digestSequence(dnaSequence, restrictionEnzyme):

    restrictionEnzymeCutSite = restrictionEnzyme.cutSite5end + restrictionEnzyme.cutSite3end
    restrictionEnzymeCutSitePattern = restrictionEnzyme.cutSite5end + '|' + restrictionEnzyme.cutSite3end

    return str(dnaSequence).replace(restrictionEnzymeCutSite, restrictionEnzymeCutSitePattern).split('|')

def doubleDigestSequence(digestedDnaFragments, firstRestrictionEnzyme, secondRestrictionEnzyme, doubleDigestedDnaComparison):

    doubleDigestedDnaFragments = digestEveryDnaFragment(digestedDnaFragments, secondRestrictionEnzyme)

    lengthsFragmentsFlankedByTwoSites = list(filter(lambda fragLen: fragLen <= MAX_BINNING_LIMIT+BINNING_STEPS, (map(lambda frag: len(frag), filter(
        lambda fragment: fragment.startswith(firstRestrictionEnzyme.cutSite3end) and fragment.endswith(
            secondRestrictionEnzyme.cutSite5end)
                         or fragment.startswith(secondRestrictionEnzyme.cutSite3end) and fragment.endswith(
            firstRestrictionEnzyme.cutSite5end), doubleDigestedDnaFragments)))))

    restrictionEnzymeCombination = firstRestrictionEnzyme.name + '+' + secondRestrictionEnzyme.name

    doubleDigestedDnaComparison.countGivenFragments(restrictionEnzymeCombination, lengthsFragmentsFlankedByTwoSites)


def digestEveryDnaFragment(digestedDnaFragment, secondRestrictionEnzyme):

    allDigestedDnaFragments = []

    for dnaFragment in digestedDnaFragment:
        digestedDnaFragmentBySecondRestrictionEnzyme = digestSequence(dnaFragment, secondRestrictionEnzyme)
        allDigestedDnaFragments.extend(digestedDnaFragmentBySecondRestrictionEnzyme)

    return allDigestedDnaFragments

def digestFastaSequence(fastaPart, firstRestrictionEnzyme, secondRestrictionEnzyme, doubleDigestedDnaComparison):

    firstDigestion = digestSequence(fastaPart, firstRestrictionEnzyme)
    doubleDigestSequence(firstDigestion, firstRestrictionEnzyme, secondRestrictionEnzyme, doubleDigestedDnaComparison)

def beginnerModeSelectionFiltering(rareCutterCuts, sequenceLength, pairedEnd, genomeSize, expectPolyMorph, numberOfSnps=None, genomeScanRadSnpDensity=None):

    totalRareCutterDigestions={}
    genomeMutationAmount=0

    if numberOfSnps != None:
        totalRareCutterDigestions = [rareCutter for rareCutter, amountEnzymeCuts in rareCutterCuts.items() if calculateBpInGenomeToBeSequenced(amountEnzymeCuts, sequenceLength, pairedEnd, expectPolyMorph) > numberOfSnps]

    if genomeScanRadSnpDensity != None:
        genomeMutationAmount = genomeScanRadSnpDensity * genomeSize
        totalRareCutterDigestions = {rareCutter for rareCutter, amountEnzymeCuts in rareCutterCuts.items() if calculateBpInGenomeToBeSequenced(amountEnzymeCuts, sequenceLength, pairedEnd, expectPolyMorph) > genomeMutationAmount}

    return (totalRareCutterDigestions, genomeMutationAmount)

def calculateBpInGenomeToBeSequenced(countCutsByFirstRestrictionEnzyme, sequenceLength, pairedEnd, expectPolyMorph):

    pairedEndModifier = 2

    if pairedEnd == PAIRED_END_ENDING:
        pairedEndModifier = 4

    bpInGenomeToBeSequenced = countCutsByFirstRestrictionEnzyme * pairedEndModifier * sequenceLength

    return bpInGenomeToBeSequenced * expectPolyMorph