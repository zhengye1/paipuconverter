from mahjong.util.MAJING_CONSTANT import *


class Mianzi:
    def __init__(self, startTile, status, mianziType, aka=0):
        self.startTile = startTile
        self.status = status
        self.mianziType = mianziType
        self.fulou = False
        self.aka = aka
        self.lst = self.toList()

    def toList(self):
        lst = []
        if self.mianziType == SHUNZI:
            lst.append(self.startTile)
            lst.append(self.startTile + 1)
            lst.append(self.startTile + 2)
        elif self.mianziType == KEZI:
            lst = [self.startTile] * 3
        elif self.mianziType == GANG:
            lst = [self.startTile] * 4

        return lst

    def __str__(self):
        baseMessage = "Mianzi(" + str(self.lst) + ") "
        if self.fulou:
            baseMessage = "Open " + baseMessage
        else:
            baseMessage = "Closed " + baseMessage
        return baseMessage
