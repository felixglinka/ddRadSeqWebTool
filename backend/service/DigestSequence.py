def doubleDigestFastaPart(fastaPart, restrictionEnzyme1, restrictionEnzyme2):

    digestedFastaSeq = digestFastaSequence(str(fastaPart.seq.upper()), restrictionEnzyme1, restrictionEnzyme2)
    return {'fragmentLengths': list(map(len, digestedFastaSeq['fragmentsFlankedByTwoSites'])),
            'countCutsByFirstRestrictionEnzyme': digestedFastaSeq['countCutsByFirstRestrictionEnzyme'],
            'countCutsBySecondRestrictionEnzyme': digestedFastaSeq['countCutsBySecondRestrictionEnzyme']}

def digestSequence(dnaSequence, restrictionEnzyme):

    restrictionEnzymeCutSite = restrictionEnzyme.cutSite5end + restrictionEnzyme.cutSite3end
    restrictionEnzymeCutSitePattern = restrictionEnzyme.cutSite5end + '|' + restrictionEnzyme.cutSite3end

    return str(dnaSequence).replace(restrictionEnzymeCutSite, restrictionEnzymeCutSitePattern).split('|')

def doubleDigestSequence(digestedDnaFragments, firstRestrictionEnzyme, secondRestrictionEnzyme):

    doubleDigestedDnaFragments = digestEveryDnaFragment(digestedDnaFragments, secondRestrictionEnzyme)
    cutBySecondRestrictionEnzyme = len(doubleDigestedDnaFragments) - len(digestedDnaFragments)

    fragmentsFlankedByTwoSites = list(filter(
        lambda fragment: fragment.startswith(firstRestrictionEnzyme.cutSite3end) and fragment.endswith(
            secondRestrictionEnzyme.cutSite5end)
                         or fragment.startswith(secondRestrictionEnzyme.cutSite3end) and fragment.endswith(
            firstRestrictionEnzyme.cutSite5end), doubleDigestedDnaFragments))

    return {"fragmentsFlankedByTwoSites": fragmentsFlankedByTwoSites, "cutBySecondRestrictionEnzyme": cutBySecondRestrictionEnzyme}

def digestEveryDnaFragment(digestedDnaFragment, secondRestrictionEnzyme):

    allDigestedDnaFragments = []

    for dnaFragment in digestedDnaFragment:
        digestedDnaFragmentBySecondRestrictionEnzyme = digestSequence(dnaFragment, secondRestrictionEnzyme)
        allDigestedDnaFragments.extend(digestedDnaFragmentBySecondRestrictionEnzyme)

    return allDigestedDnaFragments

def digestFastaSequence(fastaSequence, firstRestrictionEnzyme, secondRestrictionEnzyme):

    firstDigestion = digestSequence(fastaSequence, firstRestrictionEnzyme)
    secondDigestion = doubleDigestSequence(firstDigestion, firstRestrictionEnzyme, secondRestrictionEnzyme)

    return {
        "countCutsByFirstRestrictionEnzyme": len(firstDigestion) - 1,
        "countCutsBySecondRestrictionEnzyme": secondDigestion["cutBySecondRestrictionEnzyme"],
        "fragmentsFlankedByTwoSites": secondDigestion["fragmentsFlankedByTwoSites"]
    }