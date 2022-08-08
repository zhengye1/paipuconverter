import re

from mahjong.util.MAJING_CONSTANT import SOUTH, EAST, WEST, NORTH


def checkWReach(mopaiAction, dapaiAction):
    wReachChance = [False] * 4
    # 东家第一打
    eastFirstMopai = str(mopaiAction[EAST][0])
    eastFirstDapai = None
    if len(dapaiAction[EAST]) > 0:
        eastFirstDapai = str(dapaiAction[EAST][0])
        if 'r' in eastFirstDapai:
            wReachChance[EAST][0] = True
        if 'a' in eastFirstDapai:
            return wReachChance  # 庄家暗杠全没了
    else:
        return wReachChance  # 庄家天和

    southFirstMopai = None
    if len(mopaiAction[SOUTH]) > 0:
        southFirstMopai = str(mopaiAction[SOUTH][0])
        if bool(re.search('[cpm]', southFirstMopai)):
            return wReachChance

    westFirstMopai = None
    if len(mopaiAction[WEST]) > 0:
        westFirstMopai = str(mopaiAction[WEST][0])
        if bool(re.search('[pm]', westFirstMopai)) and:
            return wReachChance

    northFirstMopai = None
    if len(mopaiAction[NORTH]) > 0:
        northFirstMopai = str(mopaiAction[NORTH][0])
        if bool(re.search('[pm]', northFirstMopai)):
            return wReachChance

    return wReachChance