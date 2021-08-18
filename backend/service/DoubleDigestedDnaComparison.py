import base64, io, urllib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from backend.settings import MAX_GRAPH_VIEW, BINNING_STEPS, DENSITY_MODIFIER, MAX_RECOMMENDATION_NUMBER


class DoubleDigestedDnaComparison:

  def __init__(self, DigestedDnaCollection):
    self.DigestedDnaCollection = DigestedDnaCollection
    self.digestedDnaCollectionDataframe = None

  def setFragmentCalculationDataframe(self, binningSizes, sequenceLength, pairedEnd):

    for doubleDigestedDna in self.DigestedDnaCollection:
      doubleDigestedDna.createBasicDataframeForGraph(binningSizes)
      if sequenceLength != None: doubleDigestedDna.calculateBaseSequencingCosts(binningSizes, sequenceLength, pairedEnd)

    if len(self.DigestedDnaCollection) > 1:
      self.digestedDnaCollectionDataframe = pd.concat([digestedDna.fragmentCalculationDataframe for digestedDna in self.DigestedDnaCollection], axis=1)

    if len(self.DigestedDnaCollection) == 1:
     self.DigestedDnaCollection[0].fragmentCalculationDataframe


  def filterSecondCutLessThanExpectedSNP(self, beginnerModeFilterNumber, expectPolyMorph):

    if(self.digestedDnaCollectionDataframe is  None):
      return pd.DataFrame()

    allEnzymeCuttingValues = np.split(self.digestedDnaCollectionDataframe, np.arange(4, len(self.digestedDnaCollectionDataframe.columns), 4), axis=1)
    filteredDigestedDnaCollectionDataframe = []
    indicesToDelete = []

    for index, enzymeCuttingValue in enumerate(allEnzymeCuttingValues):
      sumMostCommonlySelectedFragmentSize = enzymeCuttingValue.iloc[30:70,:]['numberSequencedBasesOfBin'].sum()
      if sumMostCommonlySelectedFragmentSize * (expectPolyMorph/DENSITY_MODIFIER) < beginnerModeFilterNumber:
        indicesToDelete.append(index)
      else:
        filteredDigestedDnaCollectionDataframe.append(enzymeCuttingValue)

    for index in sorted(indicesToDelete, reverse=True):
      del self.DigestedDnaCollection[index]

    self.digestedDnaCollectionDataframe = pd.concat(filteredDigestedDnaCollectionDataframe, axis=1) if len(filteredDigestedDnaCollectionDataframe) > 0 else pd.DataFrame()

  def filterSecondCutForTooManySNPs(self, beginnerModeFilterNumber, expectPolyMorph):

    if(self.digestedDnaCollectionDataframe is  None):
      return pd.DataFrame()

    allEnzymeCuttingValues = np.split(self.digestedDnaCollectionDataframe, np.arange(4, len(self.digestedDnaCollectionDataframe.columns), 4), axis=1)
    sortedEnzymeCuttingValues = sorted(allEnzymeCuttingValues, key=lambda enzymeCut: abs(enzymeCut.iloc[:,0].sum() * (expectPolyMorph/DENSITY_MODIFIER) - beginnerModeFilterNumber))

    if(len(sortedEnzymeCuttingValues) > MAX_RECOMMENDATION_NUMBER):
      filteredSortedEnzymeCuttingValues = sortedEnzymeCuttingValues[:MAX_RECOMMENDATION_NUMBER]
      indicesToDelete = []

      for outSortedEnzymeCut in sortedEnzymeCuttingValues[MAX_RECOMMENDATION_NUMBER:]:
        outSortedEnzymeCutName = outSortedEnzymeCut.columns[0]

        for index, enzymeCuttingValue in enumerate(allEnzymeCuttingValues):
          if outSortedEnzymeCutName == enzymeCuttingValue.columns[0]:
            indicesToDelete.append(index)

      for index in sorted(indicesToDelete, reverse=True):
        del self.DigestedDnaCollection[index]

      self.sortDigestedDnaCollectionBySelectedRecommendation(filteredSortedEnzymeCuttingValues)
      self.digestedDnaCollectionDataframe = pd.concat(filteredSortedEnzymeCuttingValues, axis=1) if len(filteredSortedEnzymeCuttingValues) > 0 else pd.DataFrame()

    else:
      self.digestedDnaCollectionDataframe = pd.concat(sortedEnzymeCuttingValues, axis=1) if len(sortedEnzymeCuttingValues) > 0 else pd.DataFrame()

  def sortDigestedDnaCollectionBySelectedRecommendation(self, filteredSortedEnzymeCuttingValues):

    sortedNamesOfSelectedRecommendations = [enzymeCut.columns[0] for enzymeCut in filteredSortedEnzymeCuttingValues]
    self.DigestedDnaCollection = [element for _, element in sorted(zip(sortedNamesOfSelectedRecommendations, self.DigestedDnaCollection))]

  def createLineChart(self):

    lineChartDataFrame = [columnName for columnName in self.digestedDnaCollectionDataframe.columns if '+' in columnName]
    self.digestedDnaCollectionDataframe[lineChartDataFrame].plot.line()

    plt.xlabel('Fragment size bin (bp)')
    plt.ylabel('Number of digested fragments')
    plt.ylim(ymin=0)
    plt.xticks(np.arange(0, MAX_GRAPH_VIEW + 20, step=20),
               labels=['(0-10]', '(200-210]', '(400-410]', '(600-610]', '(800-810]', '(1000-1010]'])
    plt.legend(bbox_to_anchor=(1.04, 1), loc='upper left')

    for linePosition in range(0, MAX_GRAPH_VIEW+BINNING_STEPS, BINNING_STEPS):
      plt.axvline(x=linePosition, c=(.83, .83, .83, 0.5))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png',bbox_inches='tight')
    buffer.seek(0)
    encodedImage = base64.b64encode(buffer.read())

    graphic = 'data:image/png;base64,' + urllib.parse.quote(encodedImage)

    plt.close()

    return graphic