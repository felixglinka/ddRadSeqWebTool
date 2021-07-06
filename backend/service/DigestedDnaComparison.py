import io, urllib, base64
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from backend.settings import MAX_GRAPH_VIEW, MAX_GRAPH_RANGE, BINNING_STEPS, MAX_BINNING_LIMIT


class DigestedDnaComparison:

  def __init__(self, DigestedDna1, DigestedDna2):
    self.digestedDna1 = DigestedDna1
    self.digestedDna2 = DigestedDna2
    self.fragmentCalculationComparisonDataframe = None

  def setFragmentCalculationDataframe(self, restrictionEnzymeNames, ranges):

    self.digestedDna1.createBasicDataframeForGraph({"firstRestrictionEnzyme": restrictionEnzymeNames["restrictionEnzyme1"], "secondRestrictionEnzyme": restrictionEnzymeNames["restrictionEnzyme2"]}, ranges)
    self.digestedDna2.createBasicDataframeForGraph({"firstRestrictionEnzyme": restrictionEnzymeNames["restrictionEnzyme3"], "secondRestrictionEnzyme": restrictionEnzymeNames["restrictionEnzyme4"]}, ranges)

    self.fragmentCalculationComparisonDataframe = pd.concat([self.digestedDna1.fragmentCalculationDataframe, self.digestedDna2.fragmentCalculationDataframe], axis=1)


  def createLineChart(self, restrictionEnzymeNames):

    self.fragmentCalculationComparisonDataframe.plot.line()

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