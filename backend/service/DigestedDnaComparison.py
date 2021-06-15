import io, urllib, base64
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from backend.settings import MAX_GRAPH_VIEW, MAX_GRAPH_RANGE, BINNING_STEPS


class DigestedDnaComparison:

  def __init__(self, DigestedDna1, DigestedDna2):
    self.digestedDna1 = DigestedDna1
    self.digestedDna2 = DigestedDna2

  def createLineChart(self, restrictionEnzymeNames, selectedMinSize=None, selectedMaxSize=None):

    digestedDna1Bins = self.digestedDna1.countFragmentInBins()
    digestedDna1Bins = digestedDna1Bins.rename(columns={'fragmentLengths': restrictionEnzymeNames["restrictionEnzyme1"] + "+" + restrictionEnzymeNames["restrictionEnzyme2"]}, inplace=False)

    digestedDna2Bins = self.digestedDna2.countFragmentInBins()
    digestedDna2Bins = digestedDna2Bins.rename(columns={'fragmentLengths': restrictionEnzymeNames["restrictionEnzyme3"] + "+" + restrictionEnzymeNames["restrictionEnzyme4"]}, inplace=False)

    digestedDnaDf = pd.concat([digestedDna1Bins, digestedDna2Bins],axis=1)

    # digestedDnaDf.plot.hist(bins = 20, alpha=0.5)
    # digestedDnaDf.plot.bar(alpha=0.5)
    digestedDnaDf.iloc[0:MAX_GRAPH_VIEW+1,].plot.line()

    plt.xlabel('Fragment size bin (bp)')
    plt.ylabel('Number of digested fragments')
    plt.xticks(np.arange(0, MAX_GRAPH_VIEW + 20, step=20),
               labels=['(0-10]', '(200-210]', '(400-410]', '(600-610]', '(800-810]', '(1000-1010]'])
    plt.legend(bbox_to_anchor=(1.04, 1), loc='upper left')

    if selectedMinSize !=None and selectedMaxSize != None \
            and self.digestedDna2.fragments != [] and self.digestedDna1.fragments != []:

      if selectedMinSize > MAX_GRAPH_RANGE: selectedMinSize = MAX_GRAPH_RANGE+BINNING_STEPS
      if selectedMaxSize > MAX_GRAPH_RANGE: selectedMaxSize = MAX_GRAPH_RANGE+BINNING_STEPS
      if selectedMinSize < 0: selectedMinSize = 0
      if selectedMaxSize < 0: selectedMaxSize = 0

      plt.text(MAX_GRAPH_VIEW + 12.5, 0.65*digestedDnaDf.iloc[0:MAX_GRAPH_VIEW+1,].to_numpy().max(),
               'Numbers of fragments \nwith a size of ' + str(selectedMinSize) + ' to ' + str(selectedMaxSize) + ' bp\n' +
               restrictionEnzymeNames["restrictionEnzyme1"] + "+" + restrictionEnzymeNames[
                 "restrictionEnzyme2"] + ': ' + str(
                 self.digestedDna1.countFragmentsInGivenRange(selectedMinSize, selectedMaxSize)) + '\n' +
               restrictionEnzymeNames["restrictionEnzyme3"] + "+" + restrictionEnzymeNames[
                 "restrictionEnzyme4"] + ': ' + str(
                 self.digestedDna2.countFragmentsInGivenRange(selectedMinSize, selectedMaxSize)),
               bbox={'facecolor': 'khaki', 'alpha': 0.25})

      plt.axvspan(((selectedMinSize-1) - ((selectedMinSize-1)%BINNING_STEPS))/10 if selectedMinSize > 0 else 0,
                  ((selectedMaxSize-1) - ((selectedMaxSize-1)%BINNING_STEPS))/10 if selectedMaxSize > 0 else 0,
                  color='khaki', alpha=0.5)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png',bbox_inches='tight')
    buffer.seek(0)
    encodedImage = base64.b64encode(buffer.read())

    graphic = 'data:image/png;base64,' + urllib.parse.quote(encodedImage)

    plt.close()

    return graphic