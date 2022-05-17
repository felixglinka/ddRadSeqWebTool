import gzip
import logging
import os

from Bio import SeqIO

from backend.service.DigestSequence import digestFastaSequence, beginnerModeSelectionFiltering, digestSequence, \
    doubleDigestSequence
from backend.service.ExtractRestrictionEnzymes import getRestrictionEnzymeObjectByName
from backend.settings import COMMONLYUSEDRARECUTTERS, COMMONLYUSEDECORIFREQUENTCUTTERS, COMMONLYUSEDPSTIFREQUENTCUTTERS, \
    COMMONLYUSEDSBFIFREQUENTCUTTERS, COMMONLYUSEDSPHIFREQUENTCUTTERS

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
        os.remove(inputFasta)
        raise Exception("No proper fasta file has been uploaded")

    # finally:
    #     if os.path.exists(inputFasta):
    #         os.remove(inputFasta)
    #     else:
    #         logger.error("The file does not exist")


def countFragmentLength(doubleDigestedDnaComparison, fasta, restrictionEnzymePairList):
    fastaSequences = SeqIO.parse(fasta, 'fasta')
    for fastaPart in fastaSequences:

        for restrictionEnzymePair in restrictionEnzymePairList:
            digestFastaSequence(str(fastaPart.seq.upper()), restrictionEnzymePair[0],
                                restrictionEnzymePair[1], doubleDigestedDnaComparison)


def tryOutRareCutterAndFilterSmallest(inputFasta, doubleDigestedDnaComparison, expectPolyMorph, sequenceLength, pairedEnd, numberOfSnps=None, genomeScanRadSnpDensity=None):

    try:
        totalRareCutterDigestions = {}
        genomeSize = 0

        for rareCutter in COMMONLYUSEDRARECUTTERS:
            totalRareCutterDigestions[rareCutter] = 0

        if (is_gz_file(inputFasta)):
            with gzip.open(inputFasta, 'rt') as fasta:

                totalRareCutterDigestionsAndGenomeMutationAmount = countFragmentLengthAndTotalRareCutterDigestionsAndGenomeMutationAmount(
                    doubleDigestedDnaComparison, expectPolyMorph, fasta, genomeScanRadSnpDensity, genomeSize,
                    numberOfSnps, pairedEnd, sequenceLength, totalRareCutterDigestions)

        else:
            with open(inputFasta, 'r') as fasta:
                totalRareCutterDigestionsAndGenomeMutationAmount = countFragmentLengthAndTotalRareCutterDigestionsAndGenomeMutationAmount(
                    doubleDigestedDnaComparison, expectPolyMorph, fasta, genomeScanRadSnpDensity, genomeSize,
                    numberOfSnps, pairedEnd, sequenceLength, totalRareCutterDigestions)

        return totalRareCutterDigestionsAndGenomeMutationAmount

    except EOFError as e:
        logger.error(e)
        raise Exception("An error occured while paring, please try again!")
    except Exception as e:
        logger.error(e)
        raise Exception("No proper fasta file has been uploaded")
    # finally:
    #     if os.path.exists(inputFasta):
    #         os.remove(inputFasta)
    #     else:
    #         logger.error("The file does not exist")


def countFragmentLengthAndTotalRareCutterDigestionsAndGenomeMutationAmount(doubleDigestedDnaComparison, expectPolyMorph,
                                                                           fasta, genomeScanRadSnpDensity, genomeSize,
                                                                           numberOfSnps, pairedEnd, sequenceLength,
                                                                           totalRareCutterDigestions):
    fastaSequences = SeqIO.parse(fasta, 'fasta')

    rareCutters = [getRestrictionEnzymeObjectByName(rareCutterName) for rareCutterName in COMMONLYUSEDRARECUTTERS]
    frequentEcoRICutters = [getRestrictionEnzymeObjectByName(frequentEcoRICutterName) for frequentEcoRICutterName in COMMONLYUSEDECORIFREQUENTCUTTERS]
    frequentPstICutters = [getRestrictionEnzymeObjectByName(frequentPstICutterName) for frequentPstICutterName in COMMONLYUSEDPSTIFREQUENTCUTTERS]
    frequentSbfICutters = [getRestrictionEnzymeObjectByName(frequentSbfICutterName) for frequentSbfICutterName in COMMONLYUSEDSBFIFREQUENTCUTTERS]
    frequentSphICutters = [getRestrictionEnzymeObjectByName(frequentSphICutterName) for frequentSphICutterName in COMMONLYUSEDSPHIFREQUENTCUTTERS]

    for fastaPart in fastaSequences:

        for rareCutter in rareCutters:

            rareCutterDigestion = digestSequence(str(fastaPart.seq.upper()), rareCutter)

            if rareCutter.name == 'EcoRI':
                for frequentCutter in frequentEcoRICutters:
                    doubleDigestSequence(rareCutterDigestion, rareCutter, frequentCutter, doubleDigestedDnaComparison)

            if rareCutter.name == 'PstI':
                for frequentCutter in frequentPstICutters:
                    doubleDigestSequence(rareCutterDigestion, rareCutter, frequentCutter, doubleDigestedDnaComparison)

            if rareCutter.name == 'SbfI':
                for frequentCutter in frequentSbfICutters:
                    doubleDigestSequence(rareCutterDigestion, rareCutter, frequentCutter, doubleDigestedDnaComparison)

            if rareCutter.name == 'SphI':
                for frequentCutter in frequentSphICutters:
                    doubleDigestSequence(rareCutterDigestion, rareCutter, frequentCutter, doubleDigestedDnaComparison)

            totalRareCutterDigestions[rareCutter.name] += len(rareCutterDigestion)

        if genomeScanRadSnpDensity != None:
            genomeSize += len(fastaPart.seq)

    totalRareCutterDigestionsAndGenomeMutationAmount = beginnerModeSelectionFiltering(
        totalRareCutterDigestions, sequenceLength, pairedEnd, genomeSize, expectPolyMorph, numberOfSnps,
        genomeScanRadSnpDensity)

    return totalRareCutterDigestionsAndGenomeMutationAmount