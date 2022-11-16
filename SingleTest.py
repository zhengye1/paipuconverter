import json

import parseTenhou
from mahjong.MahjongTransfer import MahjongTransfer
from mahjong.util.MAJING_CONSTANT import SOUTH, EAST, A_RULE, WEST

if __name__ == "__main__":
    teststr = """{"title":["第39期十段位決定戦","日本プロ麻雀連盟公式ルール"],"name":["荒正義","魚谷侑未","近藤久春","浜上文吾"],"rule":{
    "disp":"第39期十段位決定戦6","aka":0},"log":[[[1,0,0],[28500,32100,29700,29700],[47],[],[16,16,46,42,15,14,27,38,22,36,
    23,11,19],[13,45,25,21,45,45,22,15,23,27,34,15,23,46,35,38,39],[42,19,46,11,38,36,60,15,60,60,60,15,60,60,60,60,
    60],[27,24,19,13,21,43,32,44,33,35,14,29,13],[37,17,45,41,42,26,31,35,18,21,27,47,44,16,41,33,18,29],[21,44,43,
    29,60,24,41,37,13,60,60,60,60,19,60,35,35,31],[47,17,21,26,43,41,26,25,38,36,12,33,32],[32,14,22,24,16,32,37,36,
    28,41,17,47,31,19,38,12,29,28],[21,43,60,47,41,14,12,60,33,60,60,60,60,60,60,60,60,26],[43,19,18,14,12,11,34,31,
    28,24,23,22,39],[42,25,24,35,31,17,46,43,36,12,39,37,11,39,28,37,44],[39,42,31,11,60,28,60,14,12,60,60,60,60,60,
    60,60,60],["和了",[0,0,-1300,1300],[3,2,3,"40符1飜1300点","河底撈魚(1飜)"]]]]} """

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
