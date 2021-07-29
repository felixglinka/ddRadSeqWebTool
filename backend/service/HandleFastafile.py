import logging

from Bio import SeqIO

from backend.service.ExtractRestrictionEnzymes import getRestrictionEnzymeObjectByName
from backend.settings import COMMONLYUSEDRARECUTTERS

logger = logging.getLogger(__name__)

def countFragmentLengthOfInputFasta(inputFasta, restrictionEnzymePairList):

    try:
        digestedDNAFragmentsByRestrictionEnzymes = {}
        for restrictionEnzymePair in restrictionEnzymePairList:
            digestedDNAFragmentsByRestrictionEnzymes[restrictionEnzymePair[0].name + '+' + restrictionEnzymePair[1].name] = []
        fastaSequences = SeqIO.parse(inputFasta, 'fasta')

        for fastaPart in fastaSequences:

            for restrictionEnzymePair in restrictionEnzymePairList:
                doubleDigestedFastaPart = doubleDigestFastaPart(fastaPart, restrictionEnzymePair[0], restrictionEnzymePair[1])
                digestedDNAFragmentsByRestrictionEnzymes[restrictionEnzymePair[0].name + '+' + restrictionEnzymePair[1].name].append(doubleDigestedFastaPart['fragmentLengths'])

        for restrictionEnzymePair in digestedDNAFragmentsByRestrictionEnzymes.keys():
            digestedDNAFragmentsByRestrictionEnzymes[restrictionEnzymePair] = [fragment for fragments in digestedDNAFragmentsByRestrictionEnzymes[restrictionEnzymePair] for fragment in fragments]

        return digestedDNAFragmentsByRestrictionEnzymes

    except Exception as e:
        logger.error(e)
        raise Exception("No proper fasta file has been uploaded")

def tryOutEnzymesDependingOnRareCutterLimit(inputFasta, rareCutterLimit):

    try:
        digestedDNAFragmentsByRestrictionEnzymes = {}
        fastaSequences = SeqIO.parse(inputFasta, 'fasta')

        for fastaPart in fastaSequences:

            totalRareCutterDigestions = {}
            totalRareCutterCutsCount = 0

            for rareCutter in COMMONLYUSEDRARECUTTERS:
                rareCutterDigestion = digestSequence(str(fastaPart.seq.upper()), getRestrictionEnzymeObjectByName(rareCutter))
                totalRareCutterDigestions[rareCutter] = rareCutterDigestion
                totalRareCutterCutsCount += len(rareCutterDigestion) - 1

        return digestedDNAFragmentsByRestrictionEnzymes

    except Exception as e:
        logger.error(e)
        raise Exception("No proper fasta file has been uploaded")

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
        allDigestedDnaFragments.append(digestedDnaFragmentBySecondRestrictionEnzyme)

    return [dnaFragment for DnaFragments in allDigestedDnaFragments for dnaFragment in DnaFragments]

def digestFastaSequence(fastaSequence, firstRestrictionEnzyme, secondRestrictionEnzyme):

    firstDigestion = digestSequence(fastaSequence, firstRestrictionEnzyme)
    secondDigestion = doubleDigestSequence(firstDigestion, firstRestrictionEnzyme, secondRestrictionEnzyme)

    return {
        "countCutsByFirstRestrictionEnzyme": len(firstDigestion) - 1,
        "countCutsBySecondRestrictionEnzyme": secondDigestion["cutBySecondRestrictionEnzyme"],
        "fragmentsFlankedByTwoSites": secondDigestion["fragmentsFlankedByTwoSites"]
    }