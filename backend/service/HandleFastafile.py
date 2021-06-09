from Bio import SeqIO
from backend.service.CreateDigestion import digestSequence


def readInFastaAndReturnOnlyFragments(inputFasta, restrictionEnzyme1, restrictionEnzyme3=None):

    digestedDNA = []
    fastaSequences = SeqIO.parse(inputFasta, 'fasta')

    if restrictionEnzyme3 != None:
        digestedDNA2 = []

    for fastaPart in fastaSequences:

        if restrictionEnzyme3 != None:
            tmp = str(fastaPart.seq.upper())
            digestedDNA2.append(digestSequence(tmp, restrictionEnzyme3))

        digestedDNA.append(digestSequence(str(fastaPart.seq.upper()), restrictionEnzyme1))

    if restrictionEnzyme3 != None:
        return {"digestedDNA": [fragment for fragments in digestedDNA for fragment in fragments],
                "digestedDNA2": [fragment for fragments in digestedDNA2 for fragment in fragments]}
    else:
        return [fragment for fragments in digestedDNA for fragment in fragments]