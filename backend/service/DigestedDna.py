import base64
from io import BytesIO

import matplotlib.pyplot as plt

class DigestedDna:

  def __init__(self, dnaFragments):
    self.fragments = dnaFragments
    self.cutByFirstRestrictionEnzyme = 0
    self.cutBySecondRestrictionEnzyme = 0


  def createHistogrammOfDistribution(self):

    lengthsOfFragments = list(map(len, self.fragments))
    plt.hist(lengthsOfFragments, bins=10, color="blue")

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

