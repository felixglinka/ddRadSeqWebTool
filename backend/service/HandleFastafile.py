import gzip
import io
import logging
import os
import zipfile

from Bio import SeqIO

from backend.service.DigestSequence import beginnerModeSelectionFiltering, DigestSequence
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
        elif(zipfile.is_zipfile(inputFasta)):
            handleZipFile(doubleDigestedDnaComparison, inputFasta, restrictionEnzymePairList)
        else:
            with open(inputFasta, 'r') as fasta:
                countFragmentLength(doubleDigestedDnaComparison, fasta, restrictionEnzymePairList)

    except EOFError as e:
        logger.error(e)
        raise Exception("An error occurred while parsing, please try again!")
    except FileExistsError as e:
        logger.error(e)
        os.remove(inputFasta)
        raise Exception("Too many files in the zip directory!")
    except Exception as e:
        logger.error(e)
        os.remove(inputFasta)
        raise Exception("No proper (g(zipped)) fasta file has been uploaded")

    # finally:
    #     if os.path.exists(inputFasta):
    #         os.remove(inputFasta)
    #     else:
    #         logger.error("The file does not exist")

def handleZipFile(doubleDigestedDnaComparison, inputFasta, restrictionEnzymePairList):

    with zipfile.ZipFile(inputFasta) as archive:
            if (len(archive.infolist()) != 1):
                raise FileExistsError
            else:
                files = archive.namelist()
                if archive.getinfo(files[0]).is_dir():
                    raise Exception
                else:
                    with archive.open(files[0]) as fasta:
                        fasta_as_text = io.TextIOWrapper(fasta)
                        countFragmentLength(doubleDigestedDnaComparison, fasta_as_text, restrictionEnzymePairList)

def handleZipFileBeginnerMode(doubleDigestedDnaComparison, inputFasta, expectPolyMorph, genomeScanRadSnpDensity, genomeSize,
                            numberOfSnps, pairedEnd, sequenceLength, totalRareCutterDigestions):
    with zipfile.ZipFile(inputFasta) as archive:
            if (len(archive.infolist()) != 1):
                raise FileExistsError
            else:
                files = archive.namelist()
                if archive.getinfo(files[0]).is_dir():
                    raise Exception
                else:
                    with archive.open(files[0]) as fasta:
                        fasta_as_text = io.TextIOWrapper(fasta)
                        return countFragmentLengthAndTotalRareCutterDigestionsAndGenomeMutationAmount(
                            doubleDigestedDnaComparison, expectPolyMorph, fasta_as_text, genomeScanRadSnpDensity, genomeSize,
                            numberOfSnps, pairedEnd, sequenceLength, totalRareCutterDigestions)

def countFragmentLength(doubleDigestedDnaComparison, fasta, restrictionEnzymePairList):

    fastaSequences = SeqIO.parse(fasta, 'fasta')
    restrictionEnzymes = tuple(set(map(lambda enzyme: enzyme.cutSite5end + enzyme.cutSite3end, tuple(set(sum(restrictionEnzymePairList, ()))))))

    for fastaPart in fastaSequences:

        digestingSequence = DigestSequence(str(fastaPart.seq.upper()), restrictionEnzymes)

        for restrictionEnzymePair in restrictionEnzymePairList:
            digestingSequence.addFragmentToSizeTable(restrictionEnzymePair[0],
                                                     restrictionEnzymePair[1], doubleDigestedDnaComparison.digestedDnaCollectionDataframe)
            # old counting method
            # digestFastaSequence(str(fastaPart.seq.upper()), restrictionEnzymePair[0],
            #                     restrictionEnzymePair[1], doubleDigestedDnaComparison)

def tryOutRareCutterAndFilterRareCutterWithNotHighEnoughValue(inputFasta, doubleDigestedDnaComparison, expectPolyMorph, sequenceLength, pairedEnd, numberOfSnps=None, genomeScanRadSnpDensity=None):

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

        elif (zipfile.is_zipfile(inputFasta)):
            totalRareCutterDigestionsAndGenomeMutationAmount = handleZipFileBeginnerMode(doubleDigestedDnaComparison, inputFasta, expectPolyMorph, genomeScanRadSnpDensity, genomeSize,
                            numberOfSnps, pairedEnd, sequenceLength, totalRareCutterDigestions)

        else:
            with open(inputFasta, 'r') as fasta:
                totalRareCutterDigestionsAndGenomeMutationAmount = countFragmentLengthAndTotalRareCutterDigestionsAndGenomeMutationAmount(
                    doubleDigestedDnaComparison, expectPolyMorph, fasta, genomeScanRadSnpDensity, genomeSize,
                    numberOfSnps, pairedEnd, sequenceLength, totalRareCutterDigestions)

        return totalRareCutterDigestionsAndGenomeMutationAmount


    except EOFError as e:
        logger.error(e)
        raise Exception("An error occurred while parsing, please try again!")
    except FileExistsError as e:
        logger.error(e)
        os.remove(inputFasta)
        raise Exception("Too many files in the zip directory!")
    except Exception as e:
        logger.error(e)
        os.remove(inputFasta)
        raise Exception("No proper (g(zipped)) fasta file has been uploaded")

def countFragmentLengthAndTotalRareCutterDigestionsAndGenomeMutationAmount(doubleDigestedDnaComparison, expectPolyMorph,
                                                                           fasta, genomeScanRadSnpDensity, genomeSize,
                                                                           numberOfSnps, pairedEnd, sequenceLength,
                                                                           totalRareCutterDigestions):
    fastaSequences = SeqIO.parse(fasta, 'fasta')

    rareCutters = [getRestrictionEnzymeObjectByName(rareCutterName) for rareCutterName in COMMONLYUSEDRARECUTTERS]
    # frequentEcoRICutters = [getRestrictionEnzymeObjectByName(frequentEcoRICutterName) for frequentEcoRICutterName in COMMONLYUSEDECORIFREQUENTCUTTERS]
    # frequentPstICutters = [getRestrictionEnzymeObjectByName(frequentPstICutterName) for frequentPstICutterName in COMMONLYUSEDPSTIFREQUENTCUTTERS]
    # frequentSbfICutters = [getRestrictionEnzymeObjectByName(frequentSbfICutterName) for frequentSbfICutterName in COMMONLYUSEDSBFIFREQUENTCUTTERS]
    # frequentSphICutters = [getRestrictionEnzymeObjectByName(frequentSphICutterName) for frequentSphICutterName in COMMONLYUSEDSPHIFREQUENTCUTTERS]

    ecoRICuttingPairs = [(getRestrictionEnzymeObjectByName('EcoRI'), getRestrictionEnzymeObjectByName(frequentEcoRICutterName)) for frequentEcoRICutterName in COMMONLYUSEDECORIFREQUENTCUTTERS]
    pstICuttingPairs = [(getRestrictionEnzymeObjectByName('PstI'), getRestrictionEnzymeObjectByName(frequentPstICutterName)) for frequentPstICutterName in COMMONLYUSEDPSTIFREQUENTCUTTERS]
    sbfICuttingPairs = [(getRestrictionEnzymeObjectByName('SbfI'), getRestrictionEnzymeObjectByName(frequentSbfICutterName)) for frequentSbfICutterName in COMMONLYUSEDSBFIFREQUENTCUTTERS]
    sphICuttingPairs = [(getRestrictionEnzymeObjectByName('SphI'), getRestrictionEnzymeObjectByName(frequentSphICutterName)) for frequentSphICutterName in COMMONLYUSEDSPHIFREQUENTCUTTERS]
    restrictionEnzymePairList = []

    restrictionEnzymePairList.extend(ecoRICuttingPairs+pstICuttingPairs+sbfICuttingPairs+sphICuttingPairs)
    restrictionEnzymes = tuple(set(map(lambda enzyme: enzyme.cutSite5end + enzyme.cutSite3end,
                                       tuple(set(sum(restrictionEnzymePairList, ()))))))

    for fastaPart in fastaSequences:

        digestingSequence = DigestSequence(str(fastaPart.seq.upper()), restrictionEnzymes)

        for restrictionEnzymePair in restrictionEnzymePairList:
            digestingSequence.addFragmentToSizeTable(restrictionEnzymePair[0],
                                                     restrictionEnzymePair[1],
                                                     doubleDigestedDnaComparison.digestedDnaCollectionDataframe)

        for rareCutter in rareCutters:
            totalRareCutterDigestions[rareCutter.name] += sum(position[0] == rareCutter.cutSite5end + rareCutter.cutSite3end for position in digestingSequence.restrictionEnzymePositions)

        # old counting method
        #     rareCutterDigestion = digestSequence(str(fastaPart.seq.upper()), rareCutter)
        #
        #     if rareCutter.name == 'EcoRI':
        #         for frequentCutter in frequentEcoRICutters:
        #             doubleDigestSequence(rareCutterDigestion, rareCutter, frequentCutter, doubleDigestedDnaComparison)
        #
        #     if rareCutter.name == 'PstI':
        #         for frequentCutter in frequentPstICutters:
        #             doubleDigestSequence(rareCutterDigestion, rareCutter, frequentCutter, doubleDigestedDnaComparison)
        #
        #     if rareCutter.name == 'SbfI':
        #         for frequentCutter in frequentSbfICutters:
        #             doubleDigestSequence(rareCutterDigestion, rareCutter, frequentCutter, doubleDigestedDnaComparison)
        #
        #     if rareCutter.name == 'SphI':
        #         for frequentCutter in frequentSphICutters:
        #             doubleDigestSequence(rareCutterDigestion, rareCutter, frequentCutter, doubleDigestedDnaComparison)
        #
            # totalRareCutterDigestions[rareCutter.name] += len(rareCutterDigestion)

        if genomeScanRadSnpDensity != None:
            genomeSize += len(fastaPart.seq)

    totalRareCutterDigestionsAndGenomeMutationAmount = beginnerModeSelectionFiltering(
        totalRareCutterDigestions, sequenceLength, pairedEnd, genomeSize, expectPolyMorph, numberOfSnps,
        genomeScanRadSnpDensity)

    return totalRareCutterDigestionsAndGenomeMutationAmount