import gzip
import logging
import os

from Bio import SeqIO

from backend.service.DigestSequence import digestFastaSequence, beginnerModeSelectionFiltering
from backend.settings import COMMONLYUSEDRARECUTTERS

logger = logging.getLogger(__name__)

def is_gz_file(inputFasta):
    with open(inputFasta, 'rb') as test_f:
        return test_f.read(2) == b'\x1f\x8b'


def countFragmentLengthOfInputFasta(inputFasta, restrictionEnzymePairList, doubleDigestedDnaComparison):

    try:

        if(is_gz_file(inputFasta)):
            with gzip.open(inputFasta, 'rt') as fasta:
                countFragmentLength(doubleDigestedDnaComparison, fasta, restrictionEnzymePairList)

        else:
            with open(inputFasta, 'r') as fasta:
                countFragmentLength(doubleDigestedDnaComparison, fasta, restrictionEnzymePairList)

    except EOFError as e:
        logger.error(e)
        raise Exception("An error occurred while paring, please try again!")
    except Exception as e:
        logger.error(e)
        raise Exception("No proper fasta file has been uploaded")

    finally:
        if os.path.exists(inputFasta):
            os.remove(inputFasta)
        else:
            logger.error("The file does not exist")


def countFragmentLength(doubleDigestedDnaComparison, fasta, restrictionEnzymePairList):
    fastaSequences = SeqIO.parse(fasta, 'fasta')
    for fastaPart in fastaSequences:

        for restrictionEnzymePair in restrictionEnzymePairList:
            digestFastaSequence(str(fastaPart.seq.upper()), restrictionEnzymePair[0],
                                restrictionEnzymePair[1], doubleDigestedDnaComparison)


def tryOutRareCutterAndFilterSmallest(inputFasta, restrictionEnzymePairList, doubleDigestedDnaComparison, expectPolyMorph, sequenceLength, pairedEnd, numberOfSnps=None, genomeScanRadSnpDensity=None):

    try:
        totalRareCutterDigestions = {}
        genomeSize = 0

        for rareCutter in COMMONLYUSEDRARECUTTERS:
            totalRareCutterDigestions[rareCutter] = 0

        if (is_gz_file(inputFasta)):
            with gzip.open(inputFasta, 'rt') as fasta:

                totalRareCutterDigestionsAndGenomeMutationAmount = countFragmentLengthAndTotalRareCutterDigestionsAndGenomeMutationAmount(
                    doubleDigestedDnaComparison, expectPolyMorph, fasta, genomeScanRadSnpDensity, genomeSize,
                    numberOfSnps, pairedEnd, restrictionEnzymePairList, sequenceLength, totalRareCutterDigestions)

        else:
            with open(inputFasta, 'r') as fasta:
                totalRareCutterDigestionsAndGenomeMutationAmount = countFragmentLengthAndTotalRareCutterDigestionsAndGenomeMutationAmount(
                    doubleDigestedDnaComparison, expectPolyMorph, fasta, genomeScanRadSnpDensity, genomeSize,
                    numberOfSnps, pairedEnd, restrictionEnzymePairList, sequenceLength, totalRareCutterDigestions)

        return totalRareCutterDigestionsAndGenomeMutationAmount

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


def countFragmentLengthAndTotalRareCutterDigestionsAndGenomeMutationAmount(doubleDigestedDnaComparison, expectPolyMorph,
                                                                           fasta, genomeScanRadSnpDensity, genomeSize,
                                                                           numberOfSnps, pairedEnd,
                                                                           restrictionEnzymePairList, sequenceLength,
                                                                           totalRareCutterDigestions):
    fastaSequences = SeqIO.parse(fasta, 'fasta')
    for fastaPart in fastaSequences:

        for restrictionEnzymePair in restrictionEnzymePairList:
            rareCutterDigestion = digestFastaSequence(str(fastaPart.seq.upper()), restrictionEnzymePair[0],
                                                      restrictionEnzymePair[1],
                                                      doubleDigestedDnaComparison)
            totalRareCutterDigestions[restrictionEnzymePair[0].name] += len(rareCutterDigestion)

        if genomeScanRadSnpDensity != None:
            genomeSize += len(fastaPart.seq)

    totalRareCutterDigestionsAndGenomeMutationAmount = beginnerModeSelectionFiltering(
        totalRareCutterDigestions, sequenceLength, pairedEnd, genomeSize, expectPolyMorph, numberOfSnps,
        genomeScanRadSnpDensity)

    return totalRareCutterDigestionsAndGenomeMutationAmount