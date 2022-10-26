import json

import parseTenhou
from mahjong.MahjongTransfer import MahjongTransfer
from mahjong.util.MAJING_CONSTANT import SOUTH, EAST

if __name__ == "__main__":
    # teststr = """{"title":["インターネット麻雀日本選手権2022","4月6日"],"name":["ぺん","魚谷侑未","ひかまゆのん","山舗徹"],"rule":{"aka":0},
    # "log":[[[1,1,0],[24100,45700,25100,25100],[],[],[12,15,15,16,17,34,37,38,24,27,27,42,47],[25,16,45,24,45,19,21,
    # 13,43,38,33],[47,12,60,34,60,60,24,21,60,42,38],[13,17,18,32,33,35,39,21,22,26,29,42,45],[35,22,37,43,41,15,32,
    # 38,44,44,17,18],[42,39,45,60,60,26,60,35,35,21,15,32],[11,12,16,35,36,25,28,29,41,41,42,46,46],[13,"4141p41",46,
    # 32,19,36,39,15,31,21,32,38,26],[25,16,42,60,60,35,60,60,60,60,60,60,60],[11,12,12,14,18,36,24,25,25,27,29,41,44],
    # [37,35,47,22,31,14,31,46,43,13,14,23,27],[41,44,60,11,60,18,60,60,22,43,12,25,27],["和了",[0,0,5500,-5500],[2,3,2,
    # "40符3飜5200点","自風 東(1飜)","役牌 發(1飜)","ドラ(1飜)"]]]]} """
    #
    # kyoku = json.loads(teststr)
    # parseTenhou.parseKyoku(kyoku['log'])
    transfer = MahjongTransfer([16, 17, 18, 24, 24, 26, 28, 36, 37, 38, 45, 45, 45, 27], [], 27)
    transfer.ronFormat = 'R'
    group = transfer.toMahjongGroup()
    for g in group:
        g.setSpecial(SOUTH, EAST, isRiichi=False)
        g.setDora([10], [])
        g.finalCheck()
        print(g)
        print("=================")

    group.sort(key=lambda x: (x.score, x.fan, x.fu), reverse=True)
    print(group[0])
