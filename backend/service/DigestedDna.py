import io, urllib, base64, math
import matplotlib.pyplot as plt

class DigestedDna:

  def __init__(self, dnaFragments):
    self.fragments = dnaFragments
    self.cutByFirstRestrictionEnzyme = 0
    self.cutBySecondRestrictionEnzyme = 0

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