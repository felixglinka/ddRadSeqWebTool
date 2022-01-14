import base64
import io
import urllib
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from backend.settings import MAX_GRAPH_VIEW, BINNING_STEPS, MAX_RECOMMENDATION_NUMBER, PAIRED_END_ENDING, \
  FIRST_BINNING_LIMIT

logger = logging.getLogger(__name__)

class DoubleDigestedDnaComparison:

  def __init__(self, sequencingYield, coverage, sequenceLength, pairedEnd):

    self.sequencingCalculation = False
    if sequencingYield != None and coverage != None and sequenceLength != None:
      self.sequencingCalculation = True
      self.sequenceLength = sequenceLength
    self.pairedEnd = pairedEnd
    self.digestedDnaCollectionDataframe = None

  def createEmptyDataFrame(self, restrictionEnzymeCombinations, binningSize):

    singleRestrictionEnzymeDataFrames=[]

    for restrictionEnzymeCombination in restrictionEnzymeCombinations:

      columnNames = [restrictionEnzymeCombination]

      if self.sequencingCalculation:
        columnNames.append(restrictionEnzymeCombination + ' numberSequencedBasesOfBin')
        columnNames.append(restrictionEnzymeCombination + ' adaptorContamination')
        if self.pairedEnd == PAIRED_END_ENDING:
          columnNames.append(restrictionEnzymeCombination + ' overlaps')

      singleRestrictionEnzymeDataFrame = pd.DataFrame(0, index=binningSize, columns=columnNames)
      singleRestrictionEnzymeDataFrames.append(singleRestrictionEnzymeDataFrame)

    self.digestedDnaCollectionDataframe = pd.concat(singleRestrictionEnzymeDataFrames, axis=1)

  def countGivenFragments(self, restrictionEnzymeCombinations, fragmentLengthList):

    if(len(fragmentLengthList) != 0):

      bins = list(self.digestedDnaCollectionDataframe.index)

      for fragmentLength in fragmentLengthList:
        for index, bin in enumerate(bins):
          if fragmentLength <= FIRST_BINNING_LIMIT:
            self.digestedDnaCollectionDataframe.loc[FIRST_BINNING_LIMIT, restrictionEnzymeCombinations] += 1
            break
          if fragmentLength > bin and fragmentLength <= bins[index+1]:
            self.digestedDnaCollectionDataframe.loc[bins[index+1], restrictionEnzymeCombinations] += 1
            break

  def calculateBaseSequencingCosts(self, restrictionEnzymeCombination):

    sequencingThreshold = self.sequenceLength

    if(self.pairedEnd == PAIRED_END_ENDING):
      sequencingThreshold = self.sequenceLength * 2

    multiplyVectorForSequencedBasesCalculation = np.array(self.digestedDnaCollectionDataframe.index)
    multiplyVectorForSequencedBasesCalculation[multiplyVectorForSequencedBasesCalculation > sequencingThreshold] = sequencingThreshold
    self.digestedDnaCollectionDataframe[restrictionEnzymeCombination + ' numberSequencedBasesOfBin'] = self.digestedDnaCollectionDataframe[restrictionEnzymeCombination].multiply(multiplyVectorForSequencedBasesCalculation)
    self.digestedDnaCollectionDataframe[restrictionEnzymeCombination + ' adaptorContamination'] = self.sumColumnUntilLimit(restrictionEnzymeCombination, 0, self.sequenceLength if self.sequenceLength < 1000 else 1000)
    if (self.pairedEnd == PAIRED_END_ENDING):
      self.digestedDnaCollectionDataframe[restrictionEnzymeCombination + ' overlaps'] = self.sumColumnUntilLimit(restrictionEnzymeCombination, self.sequenceLength, self.sequenceLength * 2 if self.sequenceLength < 505 else 1000)


  def sumColumnUntilLimit(self, restrictionEnzymeCombination, minSequenceLimit, maxSequenceLimit):

    contaminationList = [-1] * 101
    contaminationList[:int((maxSequenceLimit + 1) / 10)] = [idx for idx in range(0, int((maxSequenceLimit + 1) / 10))]
    contaminationList[:int((minSequenceLimit + 1) / 10)] = [int((minSequenceLimit) / 10) for idx in range(0, int((minSequenceLimit + 1) / 10))]

    return [self.digestedDnaCollectionDataframe[restrictionEnzymeCombination].iloc[row:int((maxSequenceLimit + 1) / 10)].sum() for row in contaminationList]


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

    sortedEnzymeCuttingValues = sorted(allEnzymeCuttingValues, key=lambda enzymeCut: abs(beginnerModeFilterNumber - enzymeCut.iloc[:,0].sum() * expectPolyMorph))

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

  def prepareDataframeData(self):

    binning = pd.concat([pd.Series([0]), pd.Series(self.digestedDnaCollectionDataframe.index * 10)]).astype(int)
    self.digestedDnaCollectionDataframe.index = pd.cut(pd.Series(self.digestedDnaCollectionDataframe.index * 10), binning)

    if (self.pairedEnd == PAIRED_END_ENDING):
      allEnzymeCuttingValues = np.split(self.digestedDnaCollectionDataframe, np.arange(4, len(self.digestedDnaCollectionDataframe.columns), 4), axis=1)
      allEnzymeCuttingValues = [allEnzymeCutting.rename(columns={allEnzymeCutting.columns[0] + ' numberSequencedBasesOfBin': 'numberSequencedBasesOfBin',
                                                                      allEnzymeCutting.columns[0] + ' adaptorContamination': 'adaptorContamination',
                                                                      allEnzymeCutting.columns[0] + ' overlaps': 'overlaps'})
                                for allEnzymeCutting in allEnzymeCuttingValues]
    else:
      allEnzymeCuttingValues = np.split(self.digestedDnaCollectionDataframe, np.arange(3, len(self.digestedDnaCollectionDataframe.columns), 3), axis=1)
      allEnzymeCuttingValues = [allEnzymeCutting.rename(columns={allEnzymeCutting.columns[0] + ' numberSequencedBasesOfBin': 'numberSequencedBasesOfBin',
                                                                      allEnzymeCutting.columns[0] + ' adaptorContamination': 'adaptorContamination'})
                                for allEnzymeCutting in allEnzymeCuttingValues]

    return [fragmentCounts.round().to_json() for fragmentCounts in allEnzymeCuttingValues]

  def createLineChart(self, restrictionEnzymePairs):

    self.digestedDnaCollectionDataframe.index = self.digestedDnaCollectionDataframe.index / 10
    self.digestedDnaCollectionDataframe[restrictionEnzymePairs].plot.line()

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