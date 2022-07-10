def ignoreNoneEncode(classDict):
    outputDict = {}
    for key, value in classDict.items:
        if value is not None:
            outputDict[key] = value
    return outputDict


class KobalabPaipu:
    def __init__(self, title, player, qijia, log, defen, rank, point):
        self.title = title
        self.playerr = player
        self.qijia = qijia
        self.log = log
        self.defen = defen
        self.rank = rank
        self.point = point

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class QiPai:
    def __init__(self, zhuangfeng, jushu, changbang, lizhibang, defen, baopai, shoupai):
        self.zhuangfeng = zhuangfeng
        self.jushu = jushu
        self.changbang = changbang
        self.lizhibang = lizhibang
        self.defen = defen
        self.baopai = baopai
        self.shoupai = shoupai

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class QiPaiWrapper:
    def __init__(self, qipai):
        self.qipai = qipai

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class PaiAction:
    def __init__(self, l, p, m):
        self.l = l
        self.p = p
        self.m = m

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class ZimoWrapper:
    def __init__(self, zimo):
        self.zimo = zimo

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class DaPaiWrapper:
    def __init__(self, dapai):
        self.dapai = dapai

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class FulouWrapper:
    def __init__(self, fulou):
        self.fulou = fulou

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class GangWrapper:
    def __init__(self, gang):
        self.gang = gang

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class GangZimoWrapper:
    def __init__(self, gangzimo):
        self.gangzimo = gangzimo

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class Hule:
    def __init__(self, l=None, shoupai=None, baojia=None, fubaopai=None, fu=None, fanshu=None, damanguan=None, defen=None, hupai=None, fenpei=None):
        self.l = l
        self.shoupai = shoupai
        self.baojia = baojia
        self.fubaopai = fubaopai
        self.fu = fu
        self.fanshu = fanshu
        self.damanguan = damanguan
        self.defen = defen
        self.hupai = hupai
        self.fenpei = fenpei

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class HuleWrapper:
    def __init__(self, hule):
        self.hule = hule

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class Pinju:
    def __init__(self, name, shoupai, fenpei):
        self.name = name
        self.shoupai = shoupai
        self.fenpei = fenpei

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class PingjuWrapper:
    def __init__(self, pingju):
        self.pingju = pingju

    def encode(self):
        return ignoreNoneEncode(self.__dict__)


class Yaku:
    def __init__(self, name, han):
        self.name = name
        self.fanshu = han

    def encode(self):
        return ignoreNoneEncode(self.__dict__)