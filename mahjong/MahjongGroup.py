from KobalabPaipu import Yaku
from mahjong.util.MAJING_CONSTANT import LIANGMIAN, NORMAL, SEVEN_PAIR, SINGLE_WAIT, KOKUSHI, KEZI, SHUANGPENG, SHUNZI, \
    GANG
from mahjong.util.YAKU_LIST import YAKU_LIST, YAKUHAI


class MahjongGroup:
    def __init__(self):
        # 记录双风2符，切上满贯，累计役满，多倍役满，复合役满，岭上自摸2符，绿一色带发（连盟规则）
        self.ruleSet = {"doubleWind": False, "kiriage": False, "kazoeyakuman": False, "baiYakuman": False,
                        "multiYakuman": True, "lingsyantsumo2fu": True, "RyuiisouWithHatsu": False}
        self.fu = 20
        self.fan = 0
        self.ronTile = 0
        self.akaSet = []
        self.yakus = []
        self.yakumans = []  # 复合役满的情况
        self.isRiichi = False
        self.isZimo = True
        self.isYifa = False
        self.isHaidi = False
        self.isHedi = False
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
        self.yakuType = NORMAL
        self.isMenzen = True
        self.ippbeikoIndex = -1
        self.isPinfuKei = False

    # https://majyan-item.com/tensu-keisan-kaisetu/
    def fuCalculation(self, ronType):
        if self.isPinfuKei:
            if self.isZimo:
                self.fu = 20
            else:
                self.fu = 30
        elif self.yakuType == SEVEN_PAIR:
            self.fu = 25
        else:
            if self.isMenzen:
                if self.isZimo:
                    self.fu = 30
                else:
                    self.fu = 40
            else:
                self.fu = 30

            # 算有没有跳符情况
            jumpFu = 0
            if self.ruleSet['doubleWind'] and self.placeWind + 41 == self.duizi and self.selfWind + 41 == self.duizi:
                jumpFu += 2
            else:
                if self.placeWind + 41 == self.duizi:
                    jumpFu += 2
                if self.selfWind + 41 == self.duizi:
                    jumpFu += 2
            if 45 <= self.duizi <= 47:
                jumpFu += 2

            if ronType == SINGLE_WAIT:
                jumpFu += 2

            if self.isZimo:
                jumpFu += 2

            for mianzi in self.mianzis:
                if mianzi.mianziType == KEZI:
                    if mianzi.fulou:
                        if 2 <= mianzi.startTile % 10 <= 8 and not mianzi.startTile / 10 == 4:
                            jumpFu += 2
                        else:
                            jumpFu += 4
                    else:
                        if 2 <= mianzi.startTile % 10 <= 8 and not mianzi.startTile / 10 == 4:
                            jumpFu += 4
                        else:
                            jumpFu += 8
                elif mianzi.mianziType == GANG:
                    if mianzi.fulou:
                        if 2 <= mianzi.startTile % 10 <= 8 and not mianzi.startTile / 10 == 4:
                            jumpFu += 8
                        else:
                            jumpFu += 16
                    else:
                        if 2 <= mianzi.startTile % 10 <= 8 and not mianzi.startTile / 10 == 4:
                            jumpFu += 16
                        else:
                            jumpFu += 32

            # 看看是跳了几级
            jumpLevel = (jumpFu - 2) // 10 * 10
            self.fu += jumpLevel

    def updateMenzenStatus(self):
        if self.yakuType != NORMAL:  # 七对子国士肯定是门清
            self.isMenzen = True
        else:  # 那全是面子了
            for mianzi in self.mianzis:
                if mianzi.fulou:
                    self.isMenzen = False
                    break

    def getRonType(self):
        ronType = []
        if self.yakuType == SEVEN_PAIR or self.yakuType == KOKUSHI:
            ronType.append(SINGLE_WAIT)
            return ronType
        if self.ronTile == self.duizi:
            ronType.append(SINGLE_WAIT)
        for mianzi in self.mianzis:
            if mianzi.mianziType == KEZI and self.ronTile in mianzi.toList():
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

    def checkYakus(self):
        checkRiichi()
        checkDoubleRiichi()
        checkIpptatsu()
        checkMenzenTsumo()
        checkPinfu()
        checkTanyao()
        checkYakuHai()
        checkLastCardAgari()
        checkQiangGang()
        checkLingShang()

        pass

    def checkRiichi(self):
        if self.isRiichi:
            self.yakus.append(Yaku(YAKU_LIST[0], 1))

    def checkDoubleRiichi(self):
        if self.isWReach:
            self.yakus.append(Yaku(YAKU_LIST[11], 1))

    def checkIppatsu(self):
        if self.isYifa:
            self.yakus.append(Yaku(YAKU_LIST[1], 1))

    def checkMenzenTsumo(self):
        if self.isMenzen and self.isZimo:
            self.yakus.append(Yaku(YAKU_LIST[2], 1))

    def checkAllShunzi(self):
        for mianzi in self.mianzis:
            if mianzi.mianziType != SHUNZI:
                return False
        return True

    def checkPinfu(self, ronType):
        if self.isMenzen and self.checkAllShunzi() and ronType == LIANGMIAN and \
                41 <= self.duizi <= 44 and self.duizi != self.selfWind + 41 and self.duizi != self.placeWind + 41:
            self.yakus.append(Yaku(YAKU_LIST[3], 1))
            self.isPinfuKei = True

    def checkTanyao(self):
        for tile in self.tiles:
            if not (2 <= tile % 10 <= 8):
                break
        self.yakus.append(Yaku(YAKU_LIST[4], 1))

    def checkIppbeiko(self):
        # 两杯口的情况后续处理....
        if self.isMenzen:
            if self.mianzis:  # 因为七对国士没法组成面子
                for i in range(3):  # 必定4组面子
                    fMianzi = self.mianzis[i]
                    sMianzi = self.mianzis[i + 1]
                    if fMianzi.mianziType == sMianzi.mianziType == SHUNZI and fMianzi.startTile == sMianzi.startTile:
                        self.yakus.append(Yaku(YAKU_LIST[5], 1))
                        self.ippbeikoIndex = len(self.yakus) - 1
                        break

    def checkYakupai(self):
        for mianzi in self.mianzis:
            if mianzi.mianziType == KEZI:
                # 场风
                if mianzi.startTile == self.placeWind:
                    self.yakus.append(Yaku(YAKU_LIST[6] + ' ' + YAKUHAI[0], 1))
                # 自风
                if mianzi.startTile == self.selfWind:
                    self.yakus.append(Yaku(YAKU_LIST[6] + ' ' + YAKUHAI[1], 1))
                    # 役牌
                    if 45 <= mianzi.startTile <= 47:
                        self.yakus.append(Yaku(YAKU_LIST[6] + ' ' + YAKUHAI[mianzi.startTile % 10 - 3], 1))

    def checkLastCardAgari(self):
        if self.isHaidi:
            self.yakus.append(Yaku(YAKU_LIST[7], 1))
        elif self.isHedi:
            self.yakus.append(Yaku(YAKU_LIST[8], 1))

    def checkQiangGang(self):
        if self.isQiangGang:
            self.yakus.append(Yaku(YAKU_LIST[9], 1))

    def checkLingShang(self):
        if self.isLingShang:
            self.yakus.append(Yaku(YAKU_LIST[10], 1))

    def __str__(self):
        return "Yaku Type: " + str(self.yakuType) + " with Mianzis: " + str(
            [str(mianzi) for mianzi in self.mianzis]) + " Duizi " + str(self.duizi) + "\n" + str(
            self.fu) + " fu " + str(self.fan) + " fan" + "\nYaku List:" + str(
            self.yakus) + " is Menzen: " + str(self.isMenzen) + " and " + ("Zimo " if self.isZimo else "Ron") + str(
            self.tiles)
