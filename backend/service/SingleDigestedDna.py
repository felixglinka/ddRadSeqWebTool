from backend.service.DigestSequence import doubleDigestSequence
from backend.service.DoubleDigestedDna import DoubleDigestedDna
from backend.service.ExtractRestrictionEnzymes import getRestrictionEnzymeObjectByName
from backend.settings import PAIRED_END_ENDING


class SingleDigestedDna:

    def __init__(self,name):
        self.name = name
        self.fragments = []
        self.countCutsByFirstRestrictionEnzyme = -1
        self.countCutsBySecondRestrictionEnzyme = 0


    def calculateBpInGenomeToBeSequenced(self, sequenceLength, pairedEnd, genomeSize, expectPolyMorph):

        pairedEndModifier = 2

        if pairedEnd == PAIRED_END_ENDING:
            pairedEndModifier = 4

        bpInGenomeToBeSequenced = self.countCutsByFirstRestrictionEnzyme * pairedEndModifier * sequenceLength

        return bpInGenomeToBeSequenced * (expectPolyMorph/1000)

    def digestDnaSecondTime(self, secondRestrictionEnzyme):

        secondDigestion = doubleDigestSequence(self.fragments, getRestrictionEnzymeObjectByName(self.name), secondRestrictionEnzyme)

        return DoubleDigestedDna(self.name + '+' + secondRestrictionEnzyme.name,  list(map(len, secondDigestion['fragmentsFlankedByTwoSites'])))
