from Bio import SeqIO

def readInFastaAndReturnOnlyFragments(inputFasta, restrictionEnzyme1, restrictionEnzyme2, restrictionEnzyme3=None, restrictionEnzyme4=None):

    countCutsByFirstRestrictionEnzyme = 0
    countCutsBySecondRestrictionEnzyme = 0
    digestedDNA = []
    fastaSequences = SeqIO.parse(inputFasta, 'fasta')

    if restrictionEnzyme3 != None and restrictionEnzyme4 != None:
        countCutsByFirstRestrictionEnzyme2 = 0
        countCutsBySecondRestrictionEnzyme2 = 0
        digestedDNA2 = []

    for fastaPart in fastaSequences:

        if restrictionEnzyme3 != None and restrictionEnzyme4 != None:
            tmpSeq = str(fastaPart.seq.upper())
            digestedFastaSeq2 = digestFastaSeq(tmpSeq, restrictionEnzyme3, restrictionEnzyme4)
            countCutsByFirstRestrictionEnzyme2 += digestedFastaSeq2["countCutsByFirstRestrictionEnzyme"]
            countCutsBySecondRestrictionEnzyme2 += digestedFastaSeq2["countCutsBySecondRestrictionEnzyme"]
            digestedDNA2.append(list(map(len, digestedFastaSeq2["fragmentsFlankedByTwoSites"])))

        digestedFastaSeq = digestFastaSeq(str(fastaPart.seq.upper()), restrictionEnzyme1, restrictionEnzyme2)
        countCutsByFirstRestrictionEnzyme += digestedFastaSeq["countCutsByFirstRestrictionEnzyme"]
        countCutsBySecondRestrictionEnzyme += digestedFastaSeq["countCutsBySecondRestrictionEnzyme"]
        digestedDNA.append(list(map(len, digestedFastaSeq["fragmentsFlankedByTwoSites"])))

    doubleDigestedDnaFragments = [fragment for fragments in digestedDNA for fragment in fragments]

    if restrictionEnzyme3 != None and restrictionEnzyme4 != None:
        doubleDigestedDnaFragments2 = [fragment for fragments in digestedDNA2 for fragment in fragments]
        return {"digestedDNA": {
            "digestedFragments": doubleDigestedDnaFragments,
            "cutByFirstRestrictionEnzyme": countCutsByFirstRestrictionEnzyme,
            "cutBySecondRestrictionEnzyme": countCutsBySecondRestrictionEnzyme},
                "digestedDNA2": {
            "digestedFragments": doubleDigestedDnaFragments2,
            "cutByFirstRestrictionEnzyme": countCutsByFirstRestrictionEnzyme2,
            "cutBySecondRestrictionEnzyme": countCutsBySecondRestrictionEnzyme2}}
    else:
        return {"digestedDNA": {
            "digestedFragments": doubleDigestedDnaFragments,
            "cutByFirstRestrictionEnzyme": countCutsByFirstRestrictionEnzyme,
            "cutBySecondRestrictionEnzyme": countCutsBySecondRestrictionEnzyme}}

def digestSequence(dnaSequence, restrictionEnzyme):

    restrictionEnzymeCutSite = restrictionEnzyme.cutSite5end + restrictionEnzyme.cutSite3end
    restrictionEnzymeCutSitePattern = restrictionEnzyme.cutSite5end + '|' + restrictionEnzyme.cutSite3end

    return str(dnaSequence).replace(restrictionEnzymeCutSite, restrictionEnzymeCutSitePattern).split('|')

def doubleDigestDnaFragments(digestedDnaFragments, firstRestrictionEnzyme, secondRestrictionEnzyme):

    digestedDnaFragmentsBySecondCutter = digestEveryDnaFragment(digestedDnaFragments, secondRestrictionEnzyme)
    cutBySecondRestrictionEnzyme = len(digestedDnaFragmentsBySecondCutter) - len(digestedDnaFragments)

    fragmentsFlankedByTwoSites = list(filter(
        lambda fragment: fragment.startswith(firstRestrictionEnzyme.cutSite3end) and fragment.endswith(
            secondRestrictionEnzyme.cutSite5end)
                         or fragment.startswith(secondRestrictionEnzyme.cutSite3end) and fragment.endswith(
            firstRestrictionEnzyme.cutSite5end), digestedDnaFragmentsBySecondCutter))

    return {"fragmentsFlankedByTwoSites": fragmentsFlankedByTwoSites, "cutBySecondRestrictionEnzyme": cutBySecondRestrictionEnzyme}

def digestEveryDnaFragment(digestedDnaFragment, secondRestrictionEnzyme):

    allDigestedDnaFragments = []

    for dnaFragment in digestedDnaFragment:
        digestedDnaFragmentBySecondRestrictionEnzyme = digestSequence(dnaFragment, secondRestrictionEnzyme)
        allDigestedDnaFragments.append(digestedDnaFragmentBySecondRestrictionEnzyme)

    return [dnaFragment for DnaFragments in allDigestedDnaFragments for dnaFragment in DnaFragments]

def digestFastaSeq(fastaSequence, firstRestrictionEnzyme, secondRestrictionEnzyme):

    firstDigestion = digestSequence(fastaSequence, firstRestrictionEnzyme)
    secondDigestion = doubleDigestDnaFragments(firstDigestion, firstRestrictionEnzyme, secondRestrictionEnzyme)

    return {
        "countCutsByFirstRestrictionEnzyme": len(firstDigestion) - 1,
        "countCutsBySecondRestrictionEnzyme": secondDigestion["cutBySecondRestrictionEnzyme"],
        "fragmentsFlankedByTwoSites": secondDigestion["fragmentsFlankedByTwoSites"]
    }

