from Bio import SeqIO
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def readInFastaAndReturnOnlySequence(inputFasta):

    allSequencesOfFasta = ""
    fasta_sequences = SeqIO.parse(inputFasta, 'fasta')

    for fastaPart in fasta_sequences:
        sequence = str(fastaPart.seq)
        allSequencesOfFasta += sequence

    if allSequencesOfFasta == "":
        logger.error("This fastafile could not be parsed (properly)")
        raise
    else:
        return allSequencesOfFasta.upper()