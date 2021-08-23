import base64
import io
import urllib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from backend.settings import MAX_GRAPH_VIEW, BINNING_STEPS, MAX_RECOMMENDATION_NUMBER, PAIRED_END_ENDING


class DoubleDigestedDnaComparison:

  def __init__(self, DigestedDnaCollection):
    self.DigestedDnaCollection = DigestedDnaCollection
    self.digestedDnaCollectionDataframe = None

  def setFragmentCalculationDataframe(self, binningSizes, sequenceLength, pairedEnd):

    for doubleDigestedDna in self.DigestedDnaCollection:
      doubleDigestedDna.createBasicDataframeForGraph(binningSizes)
      if sequenceLength != None: doubleDigestedDna.calculateBaseSequencingCosts(binningSizes, sequenceLength, pairedEnd)

    if len(self.DigestedDnaCollection) >= 1:
      self.digestedDnaCollectionDataframe = pd.concat([digestedDna.fragmentCalculationDataframe for digestedDna in self.DigestedDnaCollection], axis=1)

    if len(self.DigestedDnaCollection) == 0:
     self.digestedDnaCollectionDataframe = pd.DataFrame()


  def filterSecondCutLessThanExpectedSNP(self, beginnerModeFilterNumber, expectPolyMorph, pairedEnd):

    if(self.digestedDnaCollectionDataframe.empty):
      return

    if (pairedEnd == PAIRED_END_ENDING):
      allEnzymeCuttingValues = np.split(self.digestedDnaCollectionDataframe, np.arange(4, len(self.digestedDnaCollectionDataframe.columns), 4), axis=1)
    else:
      allEnzymeCuttingValues = np.split(self.digestedDnaCollectionDataframe,np.arange(3, len(self.digestedDnaCollectionDataframe.columns), 3), axis=1)

    filteredDigestedDnaCollectionDataframe = []
    indicesToDelete = []

    for index, enzymeCuttingValue in enumerate(allEnzymeCuttingValues):
      sumMostCommonlySelectedFragmentSize = enzymeCuttingValue.iloc[30:70,:]['numberSequencedBasesOfBin'].sum()
      if sumMostCommonlySelectedFragmentSize * expectPolyMorph < beginnerModeFilterNumber:
        indicesToDelete.append(index)
      else:
        filteredDigestedDnaCollectionDataframe.append(enzymeCuttingValue)

    for index in sorted(indicesToDelete, reverse=True):
      del self.DigestedDnaCollection[index]

    self.digestedDnaCollectionDataframe = pd.concat(filteredDigestedDnaCollectionDataframe, axis=1) if len(filteredDigestedDnaCollectionDataframe) > 0 else pd.DataFrame()

  def filterSecondCutForTooManySNPs(self, beginnerModeFilterNumber, expectPolyMorph, pairedEnd):

    if (self.digestedDnaCollectionDataframe.empty):
      return

    if (pairedEnd == PAIRED_END_ENDING):
      allEnzymeCuttingValues = np.split(self.digestedDnaCollectionDataframe, np.arange(4, len(self.digestedDnaCollectionDataframe.columns), 4), axis=1)
    else:
      allEnzymeCuttingValues = np.split(self.digestedDnaCollectionDataframe, np.arange(3, len(self.digestedDnaCollectionDataframe.columns), 3), axis=1)

    sortedEnzymeCuttingValues = sorted(allEnzymeCuttingValues, key=lambda enzymeCut: abs(enzymeCut.iloc[:,0].sum() * expectPolyMorph - beginnerModeFilterNumber))

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
      self.sortDigestedDnaCollectionBySelectedRecommendation(sortedEnzymeCuttingValues)
      self.digestedDnaCollectionDataframe = pd.concat(sortedEnzymeCuttingValues, axis=1) if len(sortedEnzymeCuttingValues) > 0 else pd.DataFrame()

  def sortDigestedDnaCollectionBySelectedRecommendation(self, filteredSortedEnzymeCuttingValues):

    sortedNamesOfSelectedRecommendations = [enzymeCut.columns[0] for enzymeCut in filteredSortedEnzymeCuttingValues]
    self.DigestedDnaCollection = [digestedDna for sortedRecommendation in sortedNamesOfSelectedRecommendations for digestedDna in self.DigestedDnaCollection if digestedDna.restrictionEnzymeCombination == sortedRecommendation]

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