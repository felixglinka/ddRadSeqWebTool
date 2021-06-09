import io, urllib, base64
import matplotlib.pyplot as plt
import pandas as pd


class DigestedDnaComparison:

  def __init__(self, DigestedDna1, DigestedDna2):
    self.digestedDna1 = DigestedDna1
    self.digestedDna2 = DigestedDna2

  def createLineChart(self, restrictionEnzymeNames):

    digestedDna1Bins = self.digestedDna1.countFragmentInBins()
    digestedDna1Bins = digestedDna1Bins.rename(columns={'fragmentLengths': restrictionEnzymeNames["restrictionEnzyme1"] + "+" + restrictionEnzymeNames["restrictionEnzyme2"]}, inplace=False)

    digestedDna2Bins = self.digestedDna2.countFragmentInBins()
    digestedDna2Bins = digestedDna2Bins.rename(columns={'fragmentLengths': restrictionEnzymeNames["restrictionEnzyme3"] + "+" + restrictionEnzymeNames["restrictionEnzyme4"]}, inplace=False)

    digestedDnaDf = pd.concat([digestedDna1Bins, digestedDna2Bins],axis=1)

    plt.figure(figsize=(8, 6), dpi=80)
    #digestedDnaDf.plot.hist(bins=40, alpha=0.5)
    digestedDnaDf.plot.line()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    encodedImage = base64.b64encode(buffer.read())

    graphic = 'data:image/png;base64,' + urllib.parse.quote(encodedImage)

    plt.close()

    return graphic