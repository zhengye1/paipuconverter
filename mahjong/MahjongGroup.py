import copy
import math

from KobalabPaipu import Yaku
from MahjongUtil import OYA_POINT, KODOMO_POINT
from mahjong.util.MAJING_CONSTANT import LIANGMIAN, NORMAL, SEVEN_PAIR, SINGLE_WAIT, KOKUSHI, KEZI, SHUANGPENG, SHUNZI, \
    GANG, EAST, OYA_YAKUMAN, KODOMO_YAKUMAN, HATSU
from mahjong.util.YAKU_LIST import YAKU_LIST, YAKUHAI


class MahjongGroup:
    def __init__(self):
        # 记录双风2符，切上满贯，累计役满，多倍役满，复合役满，岭上自摸2符，绿一色带发（连盟规则）
        self.ruleSet = {"doubleWind": False, "kiriage": False, "kazoeyakuman": False, "baiYakuman": False,
                        "multiYakuman": True, "lingsyantsumo2fu": True, "RyuiisouWithHatsu": False}
        self.fu = 20
        self.fan = 0
        self.score = 0
        self.ronType = 0
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
        self.chantaIndex = -1
        self.houRouTouIndex = -1
        self.iishoukuIndex = -1
        self.isPinfuKei = False

    def setDora(self, dora=[], ura=[]):
        self.dora = dora
        self.uraDora = ura

    def setSpecial(self, selfWind, placeWind, isRiichi=False, isWReach=False,
                   isYifa=False, isLingShang=False, isQiangGang=False, tianhe=False, dihe=False):
        self.isTianhe = tianhe
        self.isDihe = dihe
        self.selfWind = selfWind
        self.placeWind = placeWind
        self.isRiichi = isRiichi
        self.isWReach = isWReach
        self.isYifa = isYifa
        self.isLingShang = isLingShang
        self.isQiangGang = isQiangGang

    def finalCheck(self):
        ronType = self.getRonType()
        tempFu = tempFan = tempScore = 0
        temp_yaku = []
        for rt in ronType:
            # 每次for loop要reset一下以下符数翻数还有分数，因为直接改在了自身object 上
            self.fan = 0
            self.fu = 0
            self.score = 0
            self.checkYakus(rt)
            self.fuCalculation(rt)
            self.score = self.getPoint()
            if len(self.yakumans) != 0:
                self.fu = None
                self.fan = None
                self.yakus = self.yakumans
                return

            if tempScore == self.score:
                if self.fan > tempFan:
                    tempFan = self.fan
                    tempFu = self.fu
                    temp_yaku = copy.deepcopy(self.yakus)
                elif self.fan == tempFan:
                    if self.fu >= tempFu:
                        tempFan = self.fan
                        tempFu = self.fu
                        temp_yaku = copy.deepcopy(self.yakus)
                        tempScore = self.score
            elif self.score > tempScore:
                temp_yaku = copy.deepcopy(self.yakus)
                tempFan = self.fan
                tempFu = self.fu
                tempScore = self.score
            # 清空查下一个役种可能性
            self.yakus.clear()
            self.yakumans.clear()
        self.fu = tempFu
        self.fan = tempFan
        self.yakus = temp_yaku
        self.score = tempScore

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

            if self.ruleSet['lingsyantsumo2fu'] and self.isLingShang and self.isZimo:
                jumpFu += 2
            elif not self.ruleSet['lingsyantsumo2fu'] and self.isLingShang and self.isZimo:
                jumpFu += 0
            elif self.isZimo:
                jumpFu += 2

            for mianzi in self.mianzis:
                if mianzi.mianziType == KEZI:
                    if mianzi.fulou or (mianzi.startTile == self.ronTile and not self.isZimo):
                        if 2 <= mianzi.startTile % 10 <= 8 and not mianzi.startTile // 10 == 4:
                            jumpFu += 2
                        else:
                            jumpFu += 4
                    else:
                        if 2 <= mianzi.startTile % 10 <= 8 and not mianzi.startTile // 10 == 4:
                            jumpFu += 4
                        else:
                            jumpFu += 8
                elif mianzi.mianziType == GANG:
                    if mianzi.fulou:
                        if 2 <= mianzi.startTile % 10 <= 8 and not mianzi.startTile // 10 == 4:
                            jumpFu += 8
                        else:
                            jumpFu += 16
                    else:
                        if 2 <= mianzi.startTile % 10 <= 8 and not mianzi.startTile // 10 == 4:
                            jumpFu += 16
                        else:
                            jumpFu += 32

            # 看看是跳了几级
            jumpLevel = (jumpFu - 2) // 10 * 10
            self.fu += jumpLevel

    def getPoint(self):
        if len(self.yakumans) == 0:
            for yaku in self.yakus:
                self.fan += yaku.fanshu
            finalFan = self.fan
            if ((self.fu == 30 and self.fan == 4) or (self.fu == 60 and self.fan == 3)) and self.ruleSet['kiriage']:
                finalFan += 1

            if finalFan >= 13 and not self.ruleSet['kazoeyakuman']:
                finalFan = 12
            elif finalFan >= 13:
                finalFan = 13

            if self.selfWind == EAST:
                return OYA_POINT[self.fu][finalFan]
            else:
                return KODOMO_POINT[self.fu][finalFan]
        else:
            lengthYakuman = 0
            for yakuman in self.yakumans:
                lengthYakuman += len(yakuman.fanshu)

            if self.selfWind == EAST:
                if self.ruleSet['multiYakuman']:
                    return OYA_YAKUMAN * lengthYakuman
                else:
                    return OYA_YAKUMAN
            else:
                if self.ruleSet['multiYakuman']:
                    return KODOMO_YAKUMAN * lengthYakuman
                else:
                    return KODOMO_YAKUMAN

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

    def checkYakus(self, ronType):
        self.checkYakuman()
        if len(self.yakumans) == 0:
            self.checkRiichi()
            self.checkIppatsu()
            self.checkMenzenTsumo()
            self.checkPinfu(ronType)
            self.checkTanyao()
            self.checkIppbeiko()
            self.checkYakuHai()
            self.checkLastCardAgari()
            self.checkQiangGang()
            self.checkLingShang()
            self.checkChiiDuiZi()
            self.checkItTsu()
            self.checkSanShoukuTouChun()
            self.checkChanTa()
            self.checkSanShoukuTonKou()
            self.checkSanAnKou(ronType)
            self.checkDuiDui()
            self.checkShouSanGen()
            self.checkHonnRoTou()
            self.checkSanGangZi()
            self.checkHonItTsu()
            self.checkJunChan()
            self.checkRyanBeiKou()
            self.checkChinnItTsu()
            self.checkDora()

    def checkYakuman(self):
        self.firstTurnAgari()
        self.checkKoukushi()
        self.checkSuuAnKou()
        self.checkChuuRen()
        self.checkSuShi()
        self.checkDaiSanGen()
        self.checkRyuuIiSou()
        self.checkTsuIiSou()
        self.checkChinnRouTou()
        self.checkSuGangZi()

    def checkRiichi(self):
        if self.isRiichi:
            self.yakus.append(Yaku(YAKU_LIST[0], 1))
        elif self.isWReach:
            self.yakus.append(Yaku(YAKU_LIST[11], 2))

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
            if not (2 <= tile % 10 <= 8) or tile > 40:
                return
        self.yakus.append(Yaku(YAKU_LIST[4], 1))

    def checkIppbeiko(self):
        # 两杯口的情况后续处理....
        if self.isMenzen:
            if len(self.mianzis) != 0:  # 因为七对国士没法组成面子
                for i in range(3):  # 必定4组面子
                    fMianzi = self.mianzis[i]
                    sMianzi = self.mianzis[i + 1]
                    if fMianzi.mianziType == sMianzi.mianziType == SHUNZI and fMianzi.startTile == sMianzi.startTile:
                        self.yakus.append(Yaku(YAKU_LIST[5], 1))
                        self.ippbeikoIndex = len(self.yakus) - 1
                        return

    def checkYakuHai(self):
        for mianzi in self.mianzis:
            if mianzi.mianziType == KEZI:
                # 场风
                if mianzi.startTile == self.placeWind + 41:
                    self.yakus.append(Yaku(YAKU_LIST[6] + ' ' + YAKUHAI[0], 1))
                # 自风
                if mianzi.startTile == self.selfWind + 41:
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

    def checkChiiDuiZi(self):
        if self.yakuType == SEVEN_PAIR:
            self.yakus.append(Yaku(YAKU_LIST[12], 2))

    def checkItTsu(self):
        for i in range(len(self.mianzis)):
            for j in range(i + 1, len(self.mianzis)):
                for k in range(i + 2, len(self.mianzis)):
                    fMianzi = self.mianzis[i]
                    sMianzi = self.mianzis[i + 1]
                    tMianzi = self.mianzis[i + 2]
                    if fMianzi.mianziType == sMianzi.mianziType == tMianzi.mianziType == SHUNZI and (
                            fMianzi.startTile // 10 == sMianzi.startTile // 10 == tMianzi.startTile // 10):
                        startTileLst = [fMianzi.startTile % 10, sMianzi.startTile % 10, tMianzi.startTile % 10]
                        startTileLst.sort()
                        if startTileLst == [1, 4, 7]:
                            if self.isMenzen:
                                self.yakus.append(Yaku(YAKU_LIST[13], 2))
                            else:
                                self.yakus.append(Yaku(YAKU_LIST[13], 1))
                            return

    def checkSanShoukuTouChun(self):
        for i in range(len(self.mianzis)):
            for j in range(i + 1, len(self.mianzis)):
                for k in range(i + 2, len(self.mianzis)):
                    fMianzi = self.mianzis[i]
                    sMianzi = self.mianzis[i + 1]
                    tMianzi = self.mianzis[i + 2]
                    if fMianzi.mianziType == sMianzi.mianziType == tMianzi.mianziType == SHUNZI and (
                            fMianzi.startTile % 10 == sMianzi.startTile % 10 == tMianzi.startTile % 10):
                        startTileLst = [fMianzi.startTile // 10, sMianzi.startTile // 10, tMianzi.startTile // 10]
                        startTileLst.sort()
                        if startTileLst == [1, 2, 3]:
                            if self.isMenzen:
                                self.yakus.append(Yaku(YAKU_LIST[14], 2))
                            else:
                                self.yakus.append(Yaku(YAKU_LIST[14], 1))
                            return

    def checkChanTa(self):
        # 先查对子
        if 41 <= self.duizi <= 47 or (self.duizi % 10 == 1 or self.duizi % 10 == 9):
            for mianzi in self.mianzis:
                if mianzi.mianziType == KEZI:
                    if 2 <= mianzi.startTile % 10 <= 8 and mianzi.startTile < 40:
                        return
                else:
                    if mianzi.startTile != 1 and mianzi.startTile != 7:
                        return
            if self.isMenzen:
                self.yakus.append(Yaku(YAKU_LIST[15], 2))
            else:
                self.yakus.append(Yaku(YAKU_LIST[15], 1))
            self.chantaIndex = len(self.yakus) - 1

    def checkSanShoukuTonKou(self):
        for i in range(len(self.mianzis)):
            for j in range(i + 1, len(self.mianzis)):
                for k in range(i + 2, len(self.mianzis)):
                    fMianzi = self.mianzis[i]
                    sMianzi = self.mianzis[i + 1]
                    tMianzi = self.mianzis[i + 2]
                    if (fMianzi.mianziType == sMianzi.mianziType == tMianzi.mianziType == KEZI) and (
                            fMianzi.startTile % 10 == sMianzi.startTile % 10 == tMianzi.startTile % 10):
                        startTileLst = [fMianzi.startTile // 10, sMianzi.startTile // 10, tMianzi.startTile // 10]
                        startTileLst.sort()
                        if startTileLst == [1, 2, 3]:
                            self.yakus.append(Yaku(YAKU_LIST[16], 2))

    def checkSanAnKou(self, ronType):
        for i in range(len(self.mianzis)):
            for j in range(i + 1, len(self.mianzis)):
                for k in range(i + 2, len(self.mianzis)):
                    fMianzi = self.mianzis[i]
                    sMianzi = self.mianzis[i + 1]
                    tMianzi = self.mianzis[i + 2]
                    if (fMianzi.mianziType >= KEZI and sMianzi.mianziType >= KEZI and tMianzi.mianziType >= KEZI) and \
                            (not fMianzi.fulou and not sMianzi.fulou and not tMianzi.fulou):
                        if self.ronTile in [fMianzi.startTile, sMianzi.startTile,
                                            tMianzi.startTile] and not self.isZimo and ronType == SHUANGPENG:
                            continue
                        self.yakus.append(Yaku(YAKU_LIST[17], 2))
                        return

    def checkDuiDui(self):
        if len(self.mianzis) > 0:
            for mianzi in self.mianzis:
                if mianzi.mianziType == SHUNZI:
                    return
            self.yakus.append(Yaku(YAKU_LIST[18], 2))

    def checkShouSanGen(self):
        for i in range(len(self.mianzis)):
            for j in range(i + 1, len(self.mianzis)):
                fMianzi = self.mianzis[i]
                sMianzi = self.mianzis[j]
                if fMianzi.mianziType >= KEZI and sMianzi.mianziType >= KEZI:
                    startTileLst = [fMianzi.startTile, sMianzi.startTile, self.duizi]
                    startTileLst.sort()
                    if [45, 46, 47] == startTileLst:
                        self.yakus.append(Yaku(YAKU_LIST[19], 2))
                        return

    def checkHonnRoTou(self):
        for tile in self.tiles:
            if tile % 10 != 1 and tile % 10 != 9 and tile < 40:
                return
            if self.chantaIndex >= 0:
                del self.yakus[self.chantaIndex]
        self.yakus.append(Yaku(YAKU_LIST[20], 2))

    def checkSanGangZi(self):
        for i in range(len(self.mianzis)):
            for j in range(i + 1, len(self.mianzis)):
                for k in range(i + 2, len(self.mianzis)):
                    fMianzi = self.mianzis[i]
                    sMianzi = self.mianzis[j]
                    tMianzi = self.mianzis[k]
                    if fMianzi.mianziType == sMianzi.mianziType == tMianzi.mianziType == GANG:
                        self.yakus.append(Yaku(YAKU_LIST[21], 2))
                        return

    def checkHonItTsu(self):
        suit = -1
        for tile in self.tiles:
            if tile < 40:
                # 先设置颜色
                if suit == -1:
                    suit = tile // 10
                elif suit != tile // 10:
                    return
        if suit > 0:
            if self.isMenzen:
                self.yakus.append(Yaku(YAKU_LIST[22], 3))
            else:
                self.yakus.append(Yaku(YAKU_LIST[22], 2))
            self.iishoukuIndex = len(self.yakus) - 1

    def checkJunChan(self):
        if (self.duizi % 10 == 1 or self.duizi % 10 == 9) and self.duizi < 40:
            for mianzi in self.mianzis:
                if mianzi.mianziType == SHUNZI:
                    if mianzi.startTile != 1 or mianzi.startTile != 7:
                        return
                else:
                    if mianzi.startTile > 40 or mianzi.startTile % 10 != 1 or mianzi.startTile % 10 != 9:
                        return
            if self.chantaIndex >= 0:
                del self.yakus[self.chantaIndex]
            if self.isMenzen:
                self.yakus.append(Yaku(YAKU_LIST[23], 3))
            else:
                self.yakus.append(Yaku(YAKU_LIST[23], 2))

    def checkRyanBeiKou(self):
        if self.ippbeikoIndex >= 0 and len(self.mianzis) > 0:
            firstMianzi = self.mianzis[0]
            secondMianzi = self.mianzis[1]
            thirdMianzi = self.mianzis[2]
            fourthMianzi = self.mianzis[3]
            if firstMianzi.mianziType == secondMianzi.mianziType == thirdMianzi.mianziType == fourthMianzi.mianziType == SHUNZI:
                if (firstMianzi.startTile == secondMianzi.startTile) and (
                        thirdMianzi.startTile == fourthMianzi.startTile):
                    del self.yakus[self.ippbeikoIndex]
                    if self.iishoukuIndex > self.ippbeikoIndex:
                        self.iishoukuIndex -= 1
                    self.yakus.append(Yaku(YAKU_LIST[24], 3))

    def checkIiShoukuKei(self):
        suit = -1
        for tile in self.tiles:
            if tile < 40:
                if suit == -1:
                    suit = tile // 10
                elif suit != tile // 10:
                    return False
            elif tile > 40:
                return False
        return True

    def checkChinnItTsu(self):
        if self.checkIiShoukuKei():
            if self.isMenzen:
                self.yakus.append(Yaku(YAKU_LIST[25], 6))
            else:
                self.yakus.append(Yaku(YAKU_LIST[25], 5))
            del self.yakus[self.iishoukuIndex]

    def checkKoukushi(self):
        if self.yakuType == KOKUSHI:
            if self.ruleSet['baiYakuman']:
                # 查13面
                copyTile = copy.deepcopy(self.tiles[0:-1])
                copyTile.sort()
                kyokushiTiles = [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]
                if copyTile == kyokushiTiles:
                    self.yakumans.append(Yaku(YAKU_LIST[37], '**'))
            else:
                self.yakumans.append(Yaku(YAKU_LIST[26], '*'))

    def checkSuuAnKou(self):
        if len(self.mianzis) > 0:
            firstMianzi = self.mianzis[0]
            secondMianzi = self.mianzis[1]
            thirdMianzi = self.mianzis[2]
            fourthMianzi = self.mianzis[3]
            if self.ruleSet['baiYakuman']:
                if firstMianzi.mianziType >= KEZI and secondMianzi.mianziType >= KEZI and thirdMianzi.mianziType >= KEZI \
                        and fourthMianzi.mianziType >= KEZI and self.isMenzen and self.ronTile == self.duizi:
                    self.yakumans.append(Yaku(YAKU_LIST[39], '**'))
            else:
                if firstMianzi.mianziType >= KEZI and secondMianzi.mianziType >= KEZI and thirdMianzi.mianziType >= KEZI \
                        and fourthMianzi.mianziType >= KEZI and self.isMenzen:
                    self.yakumans.append(Yaku(YAKU_LIST[28], '*'))

    def checkChuuRen(self):
        chuuren = [1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9]
        if len(self.mianzis) > 0 and self.checkIiShoukuKei() and self.isMenzen:
            if self.ruleSet['baiYakuman']:
                copyTile = copy.deepcopy(self.tiles[0:-1])
                copyTile.sort()
                originalInner = []
                [originalInner.append(tile % 10) for tile in copyTile]
                if originalInner == chuuren:
                    self.yakumans.append(Yaku(YAKU_LIST[40], '**'))
            else:
                copyTile = copy.deepcopy(self.tiles)
                copyTile.sort()
                color = copyTile[0] // 10
                [copyTile.remove(color * 10 + tile) for tile in chuuren if color * 10 + tile in copyTile]
                if len(copyTile) == 1:
                    if copyTile[0] == self.ronTile:
                        self.yakumans.append(Yaku(YAKU_LIST[33], '*'))

    def checkSuShi(self):
        if len(self.mianzis) > 0:
            firstMianzi = self.mianzis[0]
            secondMianzi = self.mianzis[1]
            thirdMianzi = self.mianzis[2]
            fourthMianzi = self.mianzis[3]
            startTileLst = [firstMianzi.startTile, secondMianzi.startTile, thirdMianzi.startTile,
                            fourthMianzi.startTile]
            startTileLst.sort()
            windLst = [41, 42, 43, 44]
            [windLst.remove(tile) for tile in startTileLst if tile in windLst]
            if len(windLst) == 0:
                if self.ruleSet['baiYakuman']:
                    self.yakumans.append(Yaku(YAKU_LIST[38], '**'))
                else:
                    self.yakumans.append(Yaku(YAKU_LIST[38], '*'))
            elif len(windLst) == 1:
                if 41 <= self.duizi <= 44 and windLst[0] == self.duizi:
                    self.yakumans.append(Yaku(YAKU_LIST[29], '*'))

    def checkDaiSanGen(self):
        if len(self.mianzis) > 0:
            firstMianzi = self.mianzis[0]
            secondMianzi = self.mianzis[1]
            thirdMianzi = self.mianzis[2]
            fourthMianzi = self.mianzis[3]
            startTileLst = [firstMianzi.startTile, secondMianzi.startTile, thirdMianzi.startTile,
                            fourthMianzi.startTile]
            startTileLst.sort()
            sanGenMianzi = [45, 46, 47]
            if all(tile in startTileLst for tile in sanGenMianzi):
                self.yakumans.append(Yaku(YAKU_LIST[27], '*'))

    def checkRyuuIiSou(self):
        for tile in self.tiles:
            if tile == HATSU and self.ruleSet['RyuiisouWithHatsu']:
                return
            else:
                ryuuIISouTile = [22, 23, 24, 26, 28, 46]
                if tile not in ryuuIISouTile:
                    return
        self.yakumans.append(Yaku(YAKU_LIST[31], '*'))

    def checkTsuIiSou(self):
        for tile in self.tiles:
            if tile < 40:
                return
        self.yakumans.append(Yaku(YAKU_LIST[30], '*'))

    def checkChinnRouTou(self):
        if len(self.mianzis) > 0:
            for tile in self.tiles:
                if tile > 40 or (tile % 10 != 1 or tile % 10 != 9):
                    return
            self.yakumans.append(Yaku(YAKU_LIST[32], '*'))

    def checkSuGangZi(self):
        if len(self.mianzis) > 0:
            for mianzi in self.mianzis:
                if mianzi.mianziType != GANG:
                    return
            self.yakumans.append(Yaku(YAKU_LIST[34], '*'))

    def firstTurnAgari(self):
        if self.isTianhe:
            self.yakumans.append(Yaku(YAKU_LIST[35], '*'))
        elif self.isDihe:
            self.yakumans.append(Yaku(YAKU_LIST[36], '*'))

    def checkDora(self):
        numDora = 0
        numUra = 0
        for tile in self.tiles:
            if tile in self.dora:
                numDora += 1
            if tile in self.uraDora:
                numUra += 1

        numAka = len(self.akaSet)

        if numDora > 0:
            self.yakus.append(Yaku(YAKU_LIST[41], numDora))

        if numUra > 0:
            self.yakus.append(Yaku(YAKU_LIST[42], numUra))

        if numAka > 0:
            self.yakus.append(Yaku(YAKU_LIST[43], numAka))

    def scoreDisplay(self):
        if self.isZimo:
            if self.selfWind == EAST:
                basePay = int(math.ceil(self.score / 3 / 100) * 100)
                return str(basePay) + '点∀'
            else:
                basePay = int(math.ceil(self.score / 2 / 100) * 100)
                highPay = basePay
                basePay = int(math.ceil(basePay / 2 / 100) * 100)
                lowPay = basePay
                return str(lowPay) + '-' + str(highPay)
        else:
            return str(self.score)

    def __str__(self):
        return "Yaku Type: " + str(self.yakuType) + " with Mianzis: " + str(
            [str(mianzi) for mianzi in self.mianzis]) + " Duizi " + str(self.duizi) + "\n" + str(
            self.fu) + " fu " + str(self.fan) + " fan with score " + self.scoreDisplay() + "\nYaku List:" + \
               str([str(yakuman) for yakuman in self.yakumans] if len(self.yakumans) > 0
                   else [str(yaku) for yaku in self.yakus]) + " is Menzen: " + str(
            self.isMenzen) + " and " + ("Zimo " if self.isZimo else "Ron") + str(
            self.tiles) + " aka list: " + str(self.akaSet)
