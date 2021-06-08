from Bio import SeqIO
from backend.service.CreateDigestion import digestSequence


def readInFastaAndReturnOnlySequence(inputFasta, restrictionEnzyme1):

    digestedDNA = []
    fastaSequences = SeqIO.parse(inputFasta, 'fasta')

    for fastaPart in fastaSequences:
        digestedDNA.append(digestSequence(str(fastaPart.seq.upper()), restrictionEnzyme1))

    return [fragment for fragments in digestedDNA for fragment in fragments]