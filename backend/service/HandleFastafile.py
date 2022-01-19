import logging
import os

from Bio import SeqIO

from backend.service.DigestSequence import digestFastaSequence, digestSequence, beginnerModeSelectionFiltering
from backend.service.ExtractRestrictionEnzymes import getRestrictionEnzymeObjectByName
from backend.settings import COMMONLYUSEDRARECUTTERS

logger = logging.getLogger(__name__)

def countFragmentLengthOfInputFasta(inputFasta, restrictionEnzymePairList, doubleDigestedDnaComparison):

    try:
        with open(inputFasta, 'r') as fasta:
            fastaSequences = SeqIO.parse(fasta, 'fasta')

            for fastaPart in fastaSequences:

                for restrictionEnzymePair in restrictionEnzymePairList:
                    digestFastaSequence(str(fastaPart.seq.upper()), restrictionEnzymePair[0], restrictionEnzymePair[1], doubleDigestedDnaComparison)

    except EOFError as e:
        logger.error(e)
        raise Exception("An error occured while paring, please try again!")
    except Exception as e:
        logger.error(e)
        raise Exception("No proper fasta file has been uploaded")

    finally:
        if os.path.exists(inputFasta):
            os.remove(inputFasta)
        else:
            logger.error("The file does not exist")


def tryOutRareCutterAndFilterSmallest(inputFasta, expectPolyMorph, sequenceLength, pairedEnd, numberOfSnps=None, genomeScanRadSnpDensity=None):

    try:
        totalRareCutterDigestions = {}
        genomeSize = 0

        for rareCutter in COMMONLYUSEDRARECUTTERS:
            totalRareCutterDigestions[rareCutter] = 0

        with open(inputFasta, 'r') as fasta:
            fastaSequences = SeqIO.parse(fasta, 'fasta')

            for fastaPart in fastaSequences:

                if genomeScanRadSnpDensity != None:
                    genomeSize += len(fastaPart.seq)

                for rareCutter in COMMONLYUSEDRARECUTTERS:
                    rareCutterDigestion = digestSequence(str(fastaPart.seq.upper()), getRestrictionEnzymeObjectByName(rareCutter))
                    totalRareCutterDigestions[rareCutter] += len(rareCutterDigestion)

            totalRareCutterDigestionsAndGenomeMutationAmount = beginnerModeSelectionFiltering(totalRareCutterDigestions, sequenceLength, pairedEnd, genomeSize, expectPolyMorph, numberOfSnps, genomeScanRadSnpDensity)

        return totalRareCutterDigestionsAndGenomeMutationAmount

    except EOFError as e:
        logger.error(e)
        raise Exception("An error occured while paring, please try again!")
    except Exception as e:
        logger.error(e)
        raise Exception("No proper fasta file has been uploaded")