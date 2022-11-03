import json

import parseTenhou
from mahjong.MahjongTransfer import MahjongTransfer
from mahjong.util.MAJING_CONSTANT import SOUTH, EAST, A_RULE, WEST

if __name__ == "__main__":
    teststr = """{"title":["第39期十段位決定戦","日本プロ麻雀連盟公式ルール"],"name":["浜上文吾","荒正義","魚谷侑未","三浦智博"],"rule":{
    "disp":"第39期十段位決定戦4","aka":0},"log":[[[3,0,0],[40300,20500,38800,20400],[25],[],[38,35,33,32,32,28,25,24,21,16,
    15,41,11],[18,11,28,36,45,13,37,47,23,12,29,34],[11,60,21,18,41,45,13,60,32,60,32,29],[38,38,22,21,23,34,26,22,
    24,31,16,13,13],[24,36,11,41,46,27,46,15,18,14,44],[31,21,60,60,60,13,13,46,23,60,60],[31,32,34,34,37,39,27,28,
    29,17,19,12,14],[43,39,18,23,33,26,31,21,27,43,18],[14,12,39,60,"r43",60,60,60,60,60,60],[32,42,11,31,44,35,47,
    17,26,29,37,12,26],[25,35,28,47,33,27,17,42,"4747p47",44,"c272628",39,47,38],[42,44,29,32,31,17,60,60,11,60,12,
    33,"4747k4747"],["和了",[-4000,-4000,-4000,13000],[3,3,3,"満貫4000点∀","嶺上開花(1飜)","役牌 中(1飜)","ドラ(2飜)"]]]]} """

    kyoku = json.loads(teststr)
    parseTenhou.parseKyoku(kyoku['log'], A_RULE)
    # transfer = MahjongTransfer([25, 26, 27, 35, 35, 37, 39, 38], [['k', 47, 47, 47, 47], ['c', 26, 28, 27]], 38)
    # transfer.ronFormat = 'Z'
    # group = transfer.toMahjongGroup()
    # for g in group:
    #     g.setSpecial(EAST, EAST, isRiichi=False, isLingShang=True)
    #     g.setDora([25], [])
    #     g.finalCheck()
    #     print(g)
    #     print("=================")
    #
    # group.sort(key=lambda x: (x.score, x.fan, x.fu), reverse=True)
    # print(group[0])
