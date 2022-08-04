import copy

from mahjong.MahjongGroup import MahjongGroup
from mahjong.Mianzi import Mianzi
from mahjong.exception.MahjongException import MahjongNumberException, TileSplitException
from mahjong.util.MAJING_CONSTANT import SEVEN_PAIR, KOKUSHI, INNER, SHUNZI, KEZI, FULOU, GANG, SOUTH, EAST, NORTH, WEST


class MahjongTransfer:
    """
     lst should be in Tenhou paipu format, will be easier to determine the final group
     innerTiles(list) : The hand which is not fulou
     outerTiles(list) : The fulou list
     ronTile(int) : the ron tile
    """

    def __init__(self, innerTiles=[], outerTiles=[], ronTile=0, ronFormat='Z'):
        print(f'innerTiles {sorted(innerTiles[0:-1]) + [innerTiles[-1]]}, outerTiles {outerTiles} ronTile {ronTile}')
        if len(innerTiles) + len(outerTiles) * 3 != 14 or (ronTile > 0 and ronTile not in innerTiles):
            raise MahjongNumberException

        self.innerTiles = innerTiles
        self.outerTiles = outerTiles
        self.manzi = []
        self.pinzi = []
        self.souzi = []
        self.jipai = []
        self.akaSet = []
        self.ronFormat = ronFormat

        # need this part because for combine
        for i, tile in enumerate(self.innerTiles):
            if tile % 10 == 0:
                self.akaSet.append(tile)
                self.innerTiles.remove(tile)
                tile += 5
                self.innerTiles.insert(i, tile)

        if ronTile % 10 == 0:
            self.ronTile = ronTile + 5
        else:
            self.ronTile = ronTile
        for t in self.innerTiles:
            if 11 <= t <= 19:
                self.manzi.append(t)
            elif 21 <= t <= 29:
                self.pinzi.append(t)
            elif 31 <= t <= 39:
                self.souzi.append(t)
            elif 41 <= t <= 47:
                self.jipai.append(t)

    def possibles(self, tileLst):
        result = []
        if len(tileLst) == 0:
            result.append([])
            return result
        for i in range(len(tileLst)):
            remainTile = tileLst[i + 1:]
            tempPossibleRemain = self.possibles(remainTile)
            possibleRemain = []
            [possibleRemain.append(lst) for lst in tempPossibleRemain if lst not in possibleRemain]
            for lst in possibleRemain:
                lst1 = []
                result.append(lst1)
                lst.insert(0, tileLst[i])
                result.append(lst)
        return result

    def arrangeRemain(self, tileLst):
        result = []
        if len(tileLst) % 3 == 2:
            occurenceDict = self.countOccurence(tileLst)
            for key in occurenceDict.keys():
                tilesCopy = copy.deepcopy(tileLst)
                if occurenceDict[key] >= 2:
                    tilesCopy.remove(key)
                    tilesCopy.remove(key)
                    re = []
                    try:
                        re = self.arrangeShunzi(tilesCopy)
                    except TileSplitException:
                        continue
                    re.append(key)
                    re.append(key)
                    result.append(re)
        else:
            try:
                result.append(self.arrangeShunzi(tileLst))
            except TileSplitException:
                pass
        return result

    def validShunziCombination(self, tileLst, index):
        tile = tileLst[index]
        if tile >= 40:
            return False
        else:
            return tile + 1 in tileLst and tile + 2 in tileLst

    def arrangeShunzi(self, tileLst):
        tilesCopy = copy.deepcopy(tileLst)
        tilesCopy.sort()
        result = []
        while True:
            if len(tilesCopy) == 0:
                return result
            elif len(tilesCopy) >= 3:
                shunziStart = 0
                if self.validShunziCombination(tilesCopy, 0):
                    shunziStart = tilesCopy[0]
                else:
                    raise TileSplitException
                result.append(shunziStart)
                result.append(shunziStart + 1)
                result.append(shunziStart + 2)
                tilesCopy.remove(shunziStart)
                tilesCopy.remove(shunziStart + 1)
                tilesCopy.remove(shunziStart + 2)
            else:
                raise TileSplitException

    def splitTiles(self, tileLst):
        result = []
        if len(tileLst) == 0:
            result.append([])
            return result
        occurDict = self.countOccurence(tileLst)
        keziList = [tiles for tiles in occurDict.keys() if occurDict[tiles] >= 3]

        # return the unique list that contains the possible kezi
        tempPossibleSet = self.possibles(keziList)
        possibleSet = []
        [possibleSet.append(lst) for lst in tempPossibleSet if lst not in possibleSet]
        for ps in possibleSet:
            splitTilesLst = []
            copyTiles = copy.deepcopy(tileLst)
            for tile in ps:
                for i in range(3):
                    copyTiles.remove(tile)
                    splitTilesLst.append(tile)
            tempRemainSet = self.arrangeRemain(copyTiles)
            remainSet = []
            [remainSet.append(lst) for lst in tempRemainSet if lst not in remainSet]
            for lst in remainSet:
                splitTileCopy = copy.deepcopy(splitTilesLst)
                splitTileCopy += lst
                result.append(splitTileCopy)
        return result

    def countOccurence(self, tileLst):
        result = dict(map(lambda t: (t, list(tileLst).count(t)), tileLst))
        return result

    def concat(self, currentLst, newSplitLst):
        if len(currentLst) % 3 == 2:
            # which means current lst contains atama
            resultLst = currentLst[0:-2] + newSplitLst + currentLst[-2:]
        else:
            resultLst = currentLst + newSplitLst
        return resultLst

    def genTile(self, tileLst, currentLst):
        result = []
        tempList = self.splitTiles(tileLst)
        finalTempList = []
        [finalTempList.append(lst) for lst in tempList if lst not in finalTempList]
        for lst in finalTempList:
            for currentTileList in currentLst:
                result.append(self.concat(copy.deepcopy(currentTileList), copy.deepcopy(lst)))
        return result

    def finalTiles(self):
        result = self.splitTiles(self.manzi)
        result = self.genTile(self.pinzi, result)
        result = self.genTile(self.souzi, result)
        result = self.genTile(self.jipai, result)
        finalResult = []
        [finalResult.append(lst) for lst in result if lst not in finalResult]
        return finalResult

    def kokushi(self):
        mahjongGroup = None
        if len(self.innerTiles) != 14:
            return None
        copyTiles = copy.deepcopy(self.innerTiles)
        kyokushiTiles = [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]
        [copyTiles.remove(tile) for tile in kyokushiTiles if tile in copyTiles]
        if len(copyTiles) != 1:
            return None
        if copyTiles[0] not in kyokushiTiles:
            return None
        mahjongGroup = MahjongGroup()
        mahjongGroup.tiles = copy.deepcopy(self.innerTiles)
        mahjongGroup.yakuType = KOKUSHI
        return mahjongGroup

    def sevenPair(self):
        mahjongGroup = None
        if len(self.innerTiles) != 14:
            return None
        occurrenceDict = self.countOccurence(self.innerTiles)
        if len(occurrenceDict.keys()) == 7:
            for key, value in occurrenceDict.items():
                if value != 2:
                    return None

            mahjongGroup = MahjongGroup()
            mahjongGroup.tiles = copy.deepcopy(self.innerTiles)
            mahjongGroup.yakuType = SEVEN_PAIR
        return mahjongGroup

    def toMahjongGroup(self):
        tempGroupResult = []

        # check seven pair
        mahjongGroup = self.sevenPair()
        if mahjongGroup is not None:
            mahjongGroup.fu = 25
            mahjongGroup.ronTile = self.ronTile
            mahjongGroup.akaSet = self.akaSet
            if self.ronFormat == 'R':
                mahjongGroup.isZimo = False
            tempGroupResult.append(mahjongGroup)

        # check kokushi
        mahjongGroup = self.kokushi()
        if mahjongGroup is not None:
            mahjongGroup.fu = 20
            mahjongGroup.ronTile = self.ronTile
            if self.ronFormat == 'R':
                mahjongGroup.isZimo = False
            tempGroupResult.append(mahjongGroup)

        finalSetGroup = []

        # now Normal group
        finalNormalGroup = self.finalTiles()

        # cover 两杯口情况
        if len(finalNormalGroup) != 0:
            if len(tempGroupResult) != 0 and tempGroupResult[0].yakuType is SEVEN_PAIR:
                del tempGroupResult[0]

        # fulou part
        # outerTiles should have the format [cpkam, t, t, t, (t)]
        fulouMianzi = []
        for lst in self.outerTiles:
            if len(lst) != 0:
                outerLst = copy.deepcopy(lst[1:])
                for i, tile in enumerate(outerLst):
                    if tile % 10 == 0:
                        self.akaSet.append(tile)
                        outerLst.remove(tile)
                        tile += 5
                        outerLst.insert(i, tile)

                outerLst.sort()
                if outerLst[0] == (outerLst[1] - 1) == (outerLst[2] - 2):
                    shunziMianzi = Mianzi(outerLst[0], FULOU, SHUNZI)
                    shunziMianzi.fulou = True
                    fulouMianzi.append(shunziMianzi)

                else:
                    if len(outerLst) == 4:
                        kangMianzi = Mianzi(outerLst[0], FULOU, GANG)
                        if lst[0] != 'a':
                            kangMianzi.fulou = True
                        fulouMianzi.append(kangMianzi)

                    else:
                        keziMianzi = Mianzi(outerLst[0], FULOU, KEZI)
                        keziMianzi.fulou = True
                        fulouMianzi.append(keziMianzi)

        for g in finalNormalGroup:
            mahjongGroup = MahjongGroup()
            length = len(g) // 3
            mahjongGroup.duizi = g[-1]
            for groupNo in range(length):
                index = groupNo * 3
                if g[index] != g[index + 1]:
                    mahjongGroup.mianzis.append(Mianzi(g[index], INNER, SHUNZI))
                else:
                    mahjongGroup.mianzis.append(Mianzi(g[index], INNER, KEZI))
            mahjongGroup.ronTile = self.ronTile
            mahjongGroup.akaSet = self.akaSet
            mahjongGroup.tiles = copy.deepcopy(self.innerTiles[0:-1])  # 确保把和牌的放在最后一个上
            for outerLst in self.outerTiles:
                mahjongGroup.tiles.extend(outerLst[1:])

            mahjongGroup.tiles.append(self.ronTile)
            if self.ronFormat == 'R':
                mahjongGroup.isZimo = False
            [mahjongGroup.mianzis.append(fulouM) for fulouM in fulouMianzi]
            mahjongGroup.updateMenzenStatus()

            tempGroupResult.append(mahjongGroup)
        [finalSetGroup.append(x) for x in tempGroupResult if x not in finalSetGroup]
        return finalSetGroup


# transfer = MahjongTransfer([14, 10, 21, 22, 23, 24, 25, 26, 28, 28, 34, 30, 36, 16], [], 16)
# transfer.ronFormat = 'R'
# group = transfer.toMahjongGroup()
# for g in group:
#     g.setSpecial(SOUTH, EAST, isRiichi=True)
#     g.setDora([33], [24])
#     g.finalCheck()
#     print(g)
#     print("=================")
#
# group.sort(key=lambda x: (x.score, x.fan, x.fu), reverse=True)
# #print(group[0])
