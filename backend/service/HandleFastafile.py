import logging
import os
from tempfile import NamedTemporaryFile

from Bio import SeqIO

from backend.service.DigestSequence import doubleDigestFastaPart, digestSequence, beginnerModeSelectionFiltering
from backend.service.ExtractRestrictionEnzymes import getRestrictionEnzymeObjectByName
from backend.service.SingleDigestedDna import SingleDigestedDna
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
                doubleDigestedFastaPart = doubleDigestFastaPart(fastaPart, restrictionEnzymePair[0],
                                                                restrictionEnzymePair[1])
                digestedDNAFragmentsByRestrictionEnzymes[
                    restrictionEnzymePair[0].name + '+' + restrictionEnzymePair[1].name].extend(
                    doubleDigestedFastaPart['fragmentLengths'])

        return digestedDNAFragmentsByRestrictionEnzymes

    except Exception as e:
        logger.error(e)
        raise Exception("No proper fasta file has been uploaded")

def tryOutRareCutterAndFilterSmallest(inputFasta, expectPolyMorph, sequenceLength, pairedEnd, numberOfSnps=None, genomeScanRadSnpDensity=None):

    try:
        totalRareCutterDigestions = {}
        genomeSize = 0

        for rareCutter in COMMONLYUSEDRARECUTTERS:
            totalRareCutterDigestions[rareCutter] = SingleDigestedDna(rareCutter)

        fastaSequences = SeqIO.parse(inputFasta, 'fasta')

        for fastaPart in fastaSequences:

            genomeSize += len(fastaPart.seq)

            for rareCutter in COMMONLYUSEDRARECUTTERS:
                rareCutterDigestion = digestSequence(str(fastaPart.seq.upper()), getRestrictionEnzymeObjectByName(rareCutter))
                totalRareCutterDigestions[rareCutter].fragments.extend(rareCutterDigestion)
                totalRareCutterDigestions[rareCutter].countCutsByFirstRestrictionEnzyme += len(rareCutterDigestion)

        totalRareCutterDigestionsAndGenomeMutationAmount = beginnerModeSelectionFiltering(totalRareCutterDigestions, sequenceLength, pairedEnd, genomeSize, expectPolyMorph, numberOfSnps, genomeScanRadSnpDensity)

        return totalRareCutterDigestionsAndGenomeMutationAmount


    except Exception as e:
        logger.error(e)
        raise Exception("No proper fasta file has been uploaded")