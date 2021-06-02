from Bio import SeqIO

def readInFastaAndReturnOnlySequence(inputFasta):

    try:
        fasta_sequences = SeqIO.parse(inputFasta, 'fasta')
    except:
        print("This fastafile could not be parsed")
        raise

    allSequencesOfFasta = ""

    for fastaPart in fasta_sequences:
        sequence = str(fastaPart.seq)
        allSequencesOfFasta += sequence

    return allSequencesOfFasta.upper()