class RuleSet:
    def __init__(self, startPoint, endPoint, placementBonus, akaAri, uraAri, kanAri, yifa, kiriageMangan, doubleWind,
                 ryuiisouWithHatsu, rinnsyantsumofu, multipleYakuman, baiYakuman, tiebreaker, allLastRiichiBou,
                 kyukyu=False, allReach=False, allWindDiscard=False, fourKang=False):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.placementBonus = placementBonus
        self.akaAri = akaAri
        self.uraAri = uraAri
        self.kanAri = kanAri
        self.yifa = yifa
        self.kiriageMangan = kiriageMangan
        self.doubleWind = doubleWind
        self.ryuiisouWithHatsu = ryuiisouWithHatsu
        self.rinnsyantsumofu = rinnsyantsumofu
        self.multipleYakuman = multipleYakuman
        self.baiYakuman = baiYakuman
        self.tiebreaker = tiebreaker
        self.allLastRiichiBou = allLastRiichiBou  # removed or top
        self.kyukyu = kyukyu
        self.allReach = allReach
        self.allWindDiscard=allWindDiscard
        self.fourKang = fourKang

    def calculatePoint(self, defen, rank):
        # calculate the actual point
        actualPlacementBonus = self.placementBonus
        if len(self.placementBonus) > 1:
            numberOfOver3k = sum(map(lambda x: x >= self.endPoint, defen))
            numberOfRank = [sum(map(lambda x: x == 1, rank)), sum(map(lambda x: x == 2, rank)), sum(
                map(lambda x: x == 3, rank)), sum(map(lambda x: x == 4, rank))]

            if numberOfOver3k == 1:
                actualPlacementBonus = [p for p in self.placementBonus[0]]
                copyVer = [p for p in self.placementBonus[0]]
                if numberOfRank[2] == 2:
                    actualPlacementBonus[2] = actualPlacementBonus[3] = (copyVer[2] + copyVer[3]) / 2
                if numberOfRank[1] == 2:
                    actualPlacementBonus[1] = actualPlacementBonus[2] = (copyVer[1] + copyVer[2]) / 2
                if numberOfRank[1] == 3:
                    actualPlacementBonus[1] = actualPlacementBonus[2] = actualPlacementBonus[3] = (copyVer[1] + copyVer[
                        2] + copyVer[3]) / 3

            elif numberOfOver3k == 3:
                actualPlacementBonus = [p for p in self.placementBonus[2]]
                copyVer = [p for p in self.placementBonus[2]]
                if numberOfRank[1] == 2:
                    actualPlacementBonus[1] = actualPlacementBonus[2] = (copyVer[1] + copyVer[2]) / 2
                if numberOfRank[0] == 2:
                    actualPlacementBonus[0] = actualPlacementBonus[1] = (copyVer[0] + copyVer[1]) / 2
                if numberOfRank[0] == 3:
                    actualPlacementBonus[0] = actualPlacementBonus[1] = actualPlacementBonus[2] = (copyVer[0] + copyVer[
                        1] + copyVer[2]) / 3
            else:
                actualPlacementBonus = [p for p in self.placementBonus[1]]
                copyVer = [p for p in self.placementBonus[1]]
                if numberOfOver3k == 4:
                    actualPlacementBonus = [0, 0, 0, 0]
                if numberOfRank[2] == 2:
                    actualPlacementBonus[2] = actualPlacementBonus[3] = (copyVer[2] + copyVer[3]) / 2
                if numberOfRank[1] == 2:
                    actualPlacementBonus[1] = actualPlacementBonus[2] = (copyVer[1] + copyVer[2]) / 2
                if numberOfRank[0] == 2:
                    actualPlacementBonus[0] = actualPlacementBonus[1] = (copyVer[0] + copyVer[1]) / 2
        point = []
        for i in range(len(defen)):
            point.append((defen[i] - self.endPoint) / 1000 + actualPlacementBonus[rank[i] - 1])
        return point
