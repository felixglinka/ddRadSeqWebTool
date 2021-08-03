import pandas as pd

from backend.settings import PAIRED_END_ENDING


class DoubleDigestedDna:

  def __init__(self, restrictionEnzymeCombination, dnaFragments):
    self.restrictionEnzymeCombination = restrictionEnzymeCombination
    self.fragments = dnaFragments
    self.fragmentCalculationDataframe = None

  def createBasicDataframeForGraph(self, binningSizes):

    if(len(self.fragments) == 0):
      self.fragmentCalculationDataframe = pd.DataFrame(index=binningSizes, columns=[self.restrictionEnzymeCombination])

    basicDataframeForGraph = pd.DataFrame({self.restrictionEnzymeCombination: self.fragments})
    basicDataframeForGraph = basicDataframeForGraph.groupby(pd.cut(basicDataframeForGraph[self.restrictionEnzymeCombination], binningSizes)).count()

    self.fragmentCalculationDataframe = basicDataframeForGraph

  def calculateBaseSequencingCosts(self, binningSizes, sequenceLength, pairedEnd):

    sequencingThreshold = sequenceLength

    if(pairedEnd == PAIRED_END_ENDING):
      sequencingThreshold = sequenceLength * 2

    multiplyVectorForSequencedBasesCalculation = binningSizes[:101] + 10
    multiplyVectorForSequencedBasesCalculation[multiplyVectorForSequencedBasesCalculation > sequencingThreshold] = sequencingThreshold
    self.fragmentCalculationDataframe['numberSequencedBasesOfBin'] = self.fragmentCalculationDataframe[self.restrictionEnzymeCombination].multiply(multiplyVectorForSequencedBasesCalculation)
    self.fragmentCalculationDataframe['adaptorContamination'] = self.sumColumnUntilLimit(0, sequenceLength if sequenceLength < 1000 else 1000)
    if (pairedEnd == PAIRED_END_ENDING):
      self.fragmentCalculationDataframe['overlaps'] = self.sumColumnUntilLimit(sequenceLength, sequenceLength * 2 if sequenceLength < 505 else 1000)

  def sumColumnUntilLimit(self, minSequenceLimit, maxSequenceLimit):

    contaminationList = [-1] * 101
    contaminationList[:int((maxSequenceLimit + 1) / 10)] = [idx for idx in range(0, int((maxSequenceLimit + 1) / 10))]
    contaminationList[:int((minSequenceLimit + 1) / 10)] = [int((minSequenceLimit) / 10) for idx in range(0, int((minSequenceLimit + 1) / 10))]

    return [self.fragmentCalculationDataframe[self.restrictionEnzymeCombination].iloc[row:int((maxSequenceLimit + 1) / 10)].sum() for row in contaminationList]

  def countFragmentsInGivenRange(self, selectedMinSize, selectedMaxSize):

    if (len(self.fragments) == 0):
      return 0

    return len(list(filter(lambda fragmentLength: fragmentLength >= selectedMinSize and fragmentLength <= selectedMaxSize, self.fragments)))
