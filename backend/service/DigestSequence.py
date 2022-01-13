from backend.settings import MAX_BINNING_LIMIT, BINNING_STEPS

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
        totalRareCutterDigestions = {rareCutter: singleDigestedDna for rareCutter, singleDigestedDna in rareCutterCuts.items() if singleDigestedDna.calculateBpInGenomeToBeSequenced(sequenceLength, pairedEnd, expectPolyMorph) > numberOfSnps}

    if genomeScanRadSnpDensity != None:
        genomeMutationAmount = genomeScanRadSnpDensity * genomeSize
        totalRareCutterDigestions = {rareCutter: singleDigestedDna for rareCutter, singleDigestedDna in rareCutterCuts.items() if singleDigestedDna.calculateBpInGenomeToBeSequenced(sequenceLength, pairedEnd, expectPolyMorph) > genomeMutationAmount}

    return (totalRareCutterDigestions, genomeMutationAmount)