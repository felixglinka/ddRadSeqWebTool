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
    self.fragmentCalculationDataframe['adaptorContamination'] = self.sumColumnUntilLimit(restrictionEnzymeNames, sequenceLength if sequenceLength < 1000 else 1000)
    if (pairedEnd == PAIRED_END_ENDING):
      self.fragmentCalculationDataframe['overlaps'] = self.sumColumnUntilLimit(restrictionEnzymeNames, sequenceLength*2 if sequenceLength<505 else 1000)

  def sumColumnUntilLimit(self, restrictionEnzymeNames, sequenceLength):

    contaminationList = [-1] * 101
    contaminationList[:int((sequenceLength + 1) / 10)] = [idx for idx in range(int((sequenceLength + 1) / 10))]

    return [self.fragmentCalculationDataframe[restrictionEnzymeNames["firstRestrictionEnzyme"] + "+" + restrictionEnzymeNames["secondRestrictionEnzyme"]].iloc[row:int((sequenceLength + 1) / 10)].sum() for row in contaminationList]

  def countFragmentsInGivenRange(self, selectedMinSize, selectedMaxSize):

    if (len(self.fragments) == 0):
      return 0

    return len(list(filter(lambda fragmentLength: fragmentLength >= selectedMinSize and fragmentLength <= selectedMaxSize, self.fragments)))

  def createLineChart(self, restrictionEnzymeNames, selectedMinSize=None, selectedMaxSize=None):

    self.fragmentCalculationDataframe.plot.line()

    plt.xlabel('Fragment size bin (bp)')
    plt.ylabel('Number of digested fragments')
    plt.xticks(np.arange(0, MAX_GRAPH_VIEW + 20, step=20),
               labels=['(0-10]', '(200-210]', '(400-410]', '(600-610]', '(800-810]', '(1000-1010]'])
    plt.legend(bbox_to_anchor=(1.04, 1), loc='upper left')

    if selectedMinSize != None and selectedMaxSize != None and self.fragments != []:

      if selectedMinSize > MAX_GRAPH_RANGE: selectedMinSize = MAX_GRAPH_RANGE + BINNING_STEPS
      if selectedMaxSize > MAX_GRAPH_RANGE: selectedMaxSize = MAX_GRAPH_RANGE + BINNING_STEPS
      if selectedMinSize < 0: selectedMinSize = 0
      if selectedMaxSize < 0: selectedMaxSize = 0

      plt.text(MAX_GRAPH_VIEW + 12.5, 0.75*self.fragmentCalculationDataframe.iloc[0:MAX_GRAPH_VIEW+1,].to_numpy().max(),
               'Numbers of fragments \nwith a size of ' + str(selectedMinSize) + ' to ' + str(selectedMaxSize) + ' bp\n' +
               restrictionEnzymeNames["firstRestrictionEnzyme"] + "+" + restrictionEnzymeNames[
                 "secondRestrictionEnzyme"] + ': ' + str(
                 self.countFragmentsInGivenRange(selectedMinSize, selectedMaxSize)),
               bbox={'facecolor': 'khaki', 'alpha': 0.25})

      plt.axvspan(((selectedMinSize - 1) - ((selectedMinSize - 1) % BINNING_STEPS)) / 10 if selectedMinSize > 0 else 0,
                  ((selectedMaxSize - 1) - ((selectedMaxSize - 1) % BINNING_STEPS)) / 10 if selectedMaxSize > 0 else 0,
                  color='khaki', alpha=0.5)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png',bbox_inches='tight')
    buffer.seek(0)
    encodedImage = base64.b64encode(buffer.read())

    graphic = 'data:image/png;base64,' + urllib.parse.quote(encodedImage)

    plt.close()

    return graphic