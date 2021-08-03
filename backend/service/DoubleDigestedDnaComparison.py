import io, urllib, base64
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd

from backend.settings import MAX_GRAPH_VIEW, MAX_GRAPH_RANGE, BINNING_STEPS, MAX_BINNING_LIMIT


class DoubleDigestedDnaComparison:

  def __init__(self, DigestedDnaCollection):
    self.DigestedDnaCollection = DigestedDnaCollection
    self.digestedDnaCollectionDataframe = None

  def setFragmentCalculationDataframe(self, binningSizes, sequenceLength, pairedEnd):

    for doubleDigestedDna in self.DigestedDnaCollection:
      doubleDigestedDna.createBasicDataframeForGraph(binningSizes)
      if sequenceLength != None: doubleDigestedDna.calculateBaseSequencingCosts(binningSizes, sequenceLength, pairedEnd)

    self.digestedDnaCollectionDataframe = pd.concat([digestedDna.fragmentCalculationDataframe for digestedDna in self.DigestedDnaCollection], axis=1) if len(self.DigestedDnaCollection) > 1 else self.DigestedDnaCollection[0].fragmentCalculationDataframe

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