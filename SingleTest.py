import json

import parseTenhou
from mahjong.MahjongTransfer import MahjongTransfer
from mahjong.util.MAJING_CONSTANT import SOUTH, EAST

if __name__ == "__main__":
    teststr = """{"title":["第39期十段位決定戦","日本プロ麻雀連盟公式ルール"],"name":["荒正義","三浦智博","近藤久春","浜上文吾"],"rule":{"disp":"第39期十段位決定戦1","aka":0},"log":[[[0,0,0],[30000,30000,30000,30000],[19],[],[17,47,28,42,45,26,43,32,19,15,16,39,35],[46,15,37,44,13,37,36,14,43,43,24,18,28,33,42],[42,43,19,60,32,39,45,47,46,37,"r60",60,60,60,60],[34,33,23,24,26,11,11,36,27,16,18,19,42],[34,27,21,31,39,23,13,44,14,39,29,38,38,15,22],[19,42,60,60,60,36,60,60,23,60,24,18,23,33,27],[14,15,21,21,28,29,41,44,11,43,37,32,19],[37,24,31,29,25,45,24,18,12,26,11,38,41,22],[19,44,14,15,60,24,60,28,21,45,37,37,32,18],[39,38,35,34,32,28,25,21,47,41,41,16,12],[35,17,18,46,46,44,23,31,25,45,45,13,17,22],[21,28,32,38,39,35,25,23,31,60,60,44,46,18],["和了",[3000,-2000,0,0],[0,1,0,"40符1飜2000点","立直(1飜)"]]]]}
"""

    kyoku = json.loads(teststr)
    parseTenhou.parseKyoku(kyoku['log'])
    transfer = MahjongTransfer([13, 14, 15, 15, 16, 17, 26, 28, 35, 36, 37, 43, 43, 27], [], 27)
    transfer.ronFormat = 'R'
    group = transfer.toMahjongGroup()
    for g in group:
        g.setSpecial(EAST, EAST, isRiichi=True)
        g.setDora([19], [])
        g.finalCheck()
        print(g)
        print("=================")

    group.sort(key=lambda x: (x.score, x.fan, x.fu), reverse=True)
    print(group[0])
