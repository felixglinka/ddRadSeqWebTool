import numpy as np
import matplotlib.pyplot as plt

class DigestedDna:

  def __init__(self, dnaFragments):
    self.fragments = dnaFragments

  def createHistogrammOfDistribution(self):

    lengthsOfFragments = list(map(len, self.fragments))
    plt.hist(lengthsOfFragments, bins=10)
    plt.show()
