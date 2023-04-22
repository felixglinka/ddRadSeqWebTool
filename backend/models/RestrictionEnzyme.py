class RestrictionEnzyme:

  def __init__(self, name, cutSite5end, cutSite3end):
    self.name = name
    self.cutSite5end = cutSite5end
    self.cutSite3end = cutSite3end

  def getNameByCompleteCutSite(self, cutSideQuery):

    if self.cutSite5end + self.cutSite3end == cutSideQuery:
      return self.name

  def getCompleteCutSite(self):
    return self.cutSite5end + self.cutSite3end
