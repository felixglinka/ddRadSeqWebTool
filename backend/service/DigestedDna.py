import io, urllib, base64

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os
from backend.settings import STATIC_ROOT


class DigestedDna:

  def __init__(self, dnaFragments):
    self.fragments = dnaFragments
    self.cutByFirstRestrictionEnzyme = 0
    self.cutBySecondRestrictionEnzyme = 0

  def setCutSizes(self, numberFragmentsCutByFirstRestrictionEnzyme, numberFragmentsCutBySecondRestrictionEnzyme):
    self.cutByFirstRestrictionEnzyme = numberFragmentsCutByFirstRestrictionEnzyme
    self.cutBySecondRestrictionEnzyme = numberFragmentsCutBySecondRestrictionEnzyme

  def countFragmentInBins(self):

    lengthsOfFragments = list(map(len, self.fragments))

    if(len(lengthsOfFragments) == 0):
      return ""

    dfOfFragmentLength = pd.DataFrame({"fragmentLengths": lengthsOfFragments})
    ranges = np.arange(0, max(lengthsOfFragments)+10, 10)
    numbersFragementsInBins = dfOfFragmentLength.groupby(pd.cut(dfOfFragmentLength.fragmentLengths, ranges)).count()

    return numbersFragementsInBins

    #numbersFragementsInBins.to_csv(os.path.join(STATIC_ROOT,'fragmentLength.csv'))

  def createHistogrammOfDistribution(self):

    lengthsOfFragments = list(map(len, self.fragments))

    plt.figure(figsize=(8, 6), dpi=80)
    plt.hist(lengthsOfFragments, color="blue")
    #plt.xlim(0, max(lengthsOfFragments) + 10 if len(self.fragments) != 0 else 1)
    #plt.ylim(0, 0.4 * len(lengthsOfFragments) if len(self.fragments) != 0 else 1)
    plt.xlabel('Fragment size (bp)')
    plt.ylabel('Number of digested fragments')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    encodedImage = base64.b64encode(buffer.read())

    graphic = 'data:image/png;base64,' + urllib.parse.quote(encodedImage)

    plt.close()

    return graphic