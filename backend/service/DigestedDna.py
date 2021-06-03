import io, urllib, base64

import matplotlib.pyplot as plt

class DigestedDna:

  def __init__(self, dnaFragments):
    self.fragments = dnaFragments
    self.cutByFirstRestrictionEnzyme = 0
    self.cutBySecondRestrictionEnzyme = 0

  def createHistogrammOfDistribution(self):

    lengthsOfFragments = list(map(len, self.fragments))

    plt.hist(lengthsOfFragments, bins=15, color="blue")
    plt.xlabel('Length of digested fragments')
    plt.ylabel('Number of digested fragments')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    encodedImage = base64.b64encode(buffer.read())

    graphic = 'data:image/png;base64,' + urllib.parse.quote(encodedImage)

    plt.close()

    return graphic