import base64
import io
import urllib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from backend.settings import MAX_GRAPH_VIEW, BINNING_STEPS, MAX_GRAPH_RANGE, PAIRED_END_ENDING


class DigestedDna:

  def __init__(self, dnaFragments):
    self.fragments = dnaFragments
    self.cutByFirstRestrictionEnzyme = 0
    self.cutBySecondRestrictionEnzyme = 0
    self.fragmentCalculationDataframe = None

  def setCutSizes(self, numberFragmentsCutByFirstRestrictionEnzyme, numberFragmentsCutBySecondRestrictionEnzyme):
    self.cutByFirstRestrictionEnzyme = numberFragmentsCutByFirstRestrictionEnzyme
    self.cutBySecondRestrictionEnzyme = numberFragmentsCutBySecondRestrictionEnzyme

  def createBasicDataframeForGraph(self, restrictionEnzymeNames, ranges):

    if(len(self.fragments) == 0):
      self.fragmentCalculationDataframe = pd.DataFrame(index=ranges, columns=[restrictionEnzymeNames["firstRestrictionEnzyme"] + "+" + restrictionEnzymeNames["secondRestrictionEnzyme"]])

    basicDataframeForGraph = pd.DataFrame({restrictionEnzymeNames["firstRestrictionEnzyme"] + "+" + restrictionEnzymeNames["secondRestrictionEnzyme"]: self.fragments})
    basicDataframeForGraph = basicDataframeForGraph.groupby(pd.cut(basicDataframeForGraph[restrictionEnzymeNames["firstRestrictionEnzyme"] + "+" + restrictionEnzymeNames["secondRestrictionEnzyme"]], ranges)).count()

    self.fragmentCalculationDataframe = basicDataframeForGraph

  def calculateBaseSequencingCosts(self, restrictionEnzymeNames, ranges, sequencingYield, coverage, sequenceLength, pairedEnd):

    sequencingThreshold = sequenceLength

    if(pairedEnd == PAIRED_END_ENDING):
      sequencingThreshold = sequenceLength * 2

    multiplyVectorForSequencedBasesCalculation = ranges[:101] + 10
    multiplyVectorForSequencedBasesCalculation[multiplyVectorForSequencedBasesCalculation > sequencingThreshold] = sequencingThreshold
    self.fragmentCalculationDataframe['numberSequencedBasesOfBin'] = self.fragmentCalculationDataframe[restrictionEnzymeNames["firstRestrictionEnzyme"] + "+" + restrictionEnzymeNames["secondRestrictionEnzyme"]].multiply(multiplyVectorForSequencedBasesCalculation)
    self.fragmentCalculationDataframe['adaptorContamination'] = self.sumColumnUntilLimit(restrictionEnzymeNames, 0, sequenceLength if sequenceLength < 1000 else 1000)
    if (pairedEnd == PAIRED_END_ENDING):
      self.fragmentCalculationDataframe['overlaps'] = self.sumColumnUntilLimit(restrictionEnzymeNames, sequenceLength, sequenceLength*2 if sequenceLength<505 else 1000)

  def sumColumnUntilLimit(self, restrictionEnzymeNames, minSequenceLimit, maxSequenceLimit):

    contaminationList = [-1] * 101
    contaminationList[:int((maxSequenceLimit + 1) / 10)] = [idx for idx in range(0, int((maxSequenceLimit + 1) / 10))]
    contaminationList[:int((minSequenceLimit + 1) / 10)] = [int((minSequenceLimit) / 10) for idx in range(0, int((minSequenceLimit + 1) / 10))]

    return [self.fragmentCalculationDataframe[restrictionEnzymeNames["firstRestrictionEnzyme"] + "+" + restrictionEnzymeNames["secondRestrictionEnzyme"]].iloc[row:int((maxSequenceLimit + 1) / 10)].sum() for row in contaminationList]

  def countFragmentsInGivenRange(self, selectedMinSize, selectedMaxSize):

    if (len(self.fragments) == 0):
      return 0

    return len(list(filter(lambda fragmentLength: fragmentLength >= selectedMinSize and fragmentLength <= selectedMaxSize, self.fragments)))

  def createLineChart(self, restrictionEnzymeNames):

    self.fragmentCalculationDataframe.plot.line()

    plt.xlabel('Fragment size bin (bp)')
    plt.ylabel('Number of digested fragments')
    plt.ylim(ymin=0)
    plt.xticks(np.arange(0, MAX_GRAPH_VIEW + 20, step=20),
               labels=['(0-10]', '(200-210]', '(400-410]', '(600-610]', '(800-810]', '(1000-1010]'])
    plt.legend(bbox_to_anchor=(1.04, 1), loc='upper left')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png',bbox_inches='tight')
    buffer.seek(0)
    encodedImage = base64.b64encode(buffer.read())

    graphic = 'data:image/png;base64,' + urllib.parse.quote(encodedImage)

    plt.close()

    return graphic