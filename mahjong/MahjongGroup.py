from mahjong.util.MAJING_CONSTANT import LIANGMIAN, NORMAL, SEVEN_PAIR, SINGLE_WAIT, KOKUSHI, KEZI, SHUANGPENG, SHUNZI


class MahjongGroup:
    def __init__(self):
        self.fu = 20
        self.fan = 0
        self.ronTile = 0
        self.akaSet = []
        self.yakus = []
        self.yakumans = []  # 复合役满的情况
        self.isYifa = False
        self.isHaidi = False
        self.isHeidi = False
        self.isLingShang = False
        self.isQiangGang = False
        self.isTianhe = False
        self.isDihe = False
        self.isWReach = False
        self.placeWind = 0
        self.selfWind = 0
        self.mianzis = []
        self.duizi = 0
        self.dora = []
        self.uraDora = []
        self.tiles = []
        self.baiYakuman = False
        self.kiriage = False
        self.yakuType = NORMAL

    def ronType(self):
        ronType = []
        if self.yakuType == SEVEN_PAIR or self.yakuType == KOKUSHI:
            ronType.append(SINGLE_WAIT)
            return ronType
        if self.ronTile == self.duizi:
            ronType.append(SINGLE_WAIT)
        for mianzi in self.mianzis:
            if mianzi.mianziType == KEZI and self.ronTile in mianzi:
                ronType.append(SHUANGPENG)
            if mianzi.mianziType == SHUNZI:
                if self.ronTile == mianzi.startTile:
                    if self.ronTile % 10 == 7:
                        ronType.append(SINGLE_WAIT)
                    else:
                        ronType.append(LIANGMIAN)
                elif self.ronTile == mianzi.startTile + 1:
                    ronType.append(SINGLE_WAIT)
                elif self.ronTile == mianzi.startTile + 2:
                    if self.ronTile % 10 == 3:
                        ronType.append(SINGLE_WAIT)
                    else:
                        ronType.append(LIANGMIAN)
        finalRonType = []
        [finalRonType.append(rt) for rt in ronType if rt not in finalRonType]
        return finalRonType

    def __str__(self):
        return "Mianzis: " + str([str(mianzi) for mianzi in self.mianzis]) + " Duizi " + str(self.duizi) + "\n" + str(
            self.fu) + " fu " + str(self.fan) + " fan" + "\nYaku List:" + str(
            self.yakus)
