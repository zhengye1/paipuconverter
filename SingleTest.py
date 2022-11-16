import json

import parseTenhou
from mahjong.MahjongTransfer import MahjongTransfer
from mahjong.util.MAJING_CONSTANT import SOUTH, EAST, A_RULE, WEST

if __name__ == "__main__":
    teststr = """{"title":["第39期十段位決定戦","日本プロ麻雀連盟公式ルール"],"name":["荒正義","魚谷侑未","近藤久春","浜上文吾"],"rule":{
    "disp":"第39期十段位決定戦6","aka":0},"log":[[[6,1,0],[33900,35000,34700,16400],[11],[],[14,29,29,24,23,22,22,21,37,39,
    17,19,32],[],[],[18,18,14,42,31,33,34,34,38,23,25,26,28],[],[],[27,42,33,13,12,38,35,32,18,35,26,26,27],[28],
    [42],[19,24,26,18,16,45,46,41,44,21,39,29,31],[36],[],["九種九牌"]]]} """

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
