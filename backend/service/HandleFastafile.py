from Bio import SeqIO

def readInFastaAndReturnOnlySequence(inputFasta):

    fasta_sequences = SeqIO.parse(inputFasta, 'fasta')

    allSequencesOfFasta = ""

    for fastaPart in fasta_sequences:
        sequence = str(fastaPart.seq)
        allSequencesOfFasta += sequence

    if allSequencesOfFasta == "":
        print("This fastafile could not be parsed")
        raise
    else:
        return allSequencesOfFasta.upper()