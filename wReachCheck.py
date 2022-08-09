import re

from mahjong.util.MAJING_CONSTANT import SOUTH, EAST, WEST, NORTH


def checkWReach(mopaiAction, dapaiAction):
    wReachChance = [False] * 4
    # 东家第一打
    eastFirstMopai = str(mopaiAction[EAST][0])
    if len(dapaiAction[EAST]) > 0:
        eastFirstDapai = str(dapaiAction[EAST][0])
        if 'r' in eastFirstDapai:
            wReachChance[EAST] = True
            if eastFirstDapai == 'r60':
                eastFirstDapai = eastFirstMopai
        if 'a' in eastFirstDapai:
            return wReachChance  # 庄家暗杠全没了
    else:
        return wReachChance  # 庄家天和

    southFirstMopai = None
    if len(mopaiAction[SOUTH]) > 0:
        southFirstMopai = str(mopaiAction[SOUTH][0])
        if bool(re.search('[cpm]', southFirstMopai)) and eastFirstDapai in southFirstMopai:  # 庄家打的，南家副露
            return wReachChance

    westFirstMopai = None
    if len(mopaiAction[WEST]) > 0:
        westFirstMopai = str(mopaiAction[WEST][0])
        if bool(re.search('[pm]', westFirstMopai)) and eastFirstDapai in westFirstMopai:
            return wReachChance

    northFirstMopai = None
    if len(mopaiAction[NORTH]) > 0:
        northFirstMopai = str(mopaiAction[NORTH][0])
        if bool(re.search('[pm]', northFirstMopai)) and eastFirstDapai in northFirstMopai:
            return wReachChance

    # 那就轮到南家了
    if len(dapaiAction[SOUTH]) > 0:
        southFirstDapai = str(dapaiAction[SOUTH][0])
        if 'r' in southFirstDapai:
            wReachChance[SOUTH] = True
            if southFirstDapai == 'r60':
                southFirstDapai = southFirstMopai
        if 'a' in southFirstDapai:
            return wReachChance
    else:
        return wReachChance

    if westFirstMopai:
        if bool(re.search('[cpm]', westFirstMopai)) and southFirstDapai in westFirstMopai:  # 南家打的
            return wReachChance

    if northFirstMopai:
        if bool(re.search('[pm]', northFirstMopai)) and southFirstDapai in northFirstMopai:
            return wReachChance

    eastSecondMopai = None
    if len(mopaiAction[EAST]) > 1:
        eastSecondMopai = str(mopaiAction[EAST][1])
        if bool(re.search('[pm]', eastSecondMopai)) and southFirstDapai in eastSecondMopai:
            return wReachChance

    # 西家
    if len(dapaiAction[WEST]) > 0:
        westFirstDapai = str(dapaiAction[WEST][0])
        if 'r' in westFirstDapai:
            wReachChance[WEST] = True
            if westFirstDapai == 'r60':
                westFirstDapai = westFirstMopai
        if 'a' in westFirstDapai:
            return wReachChance
    else:
        return wReachChance

    if northFirstMopai:
        if bool(re.search('[cpm]', northFirstMopai)) and westFirstDapai in northFirstMopai:
            return wReachChance

    if eastSecondMopai:
        if bool(re.search('[pm]', eastSecondMopai)) and westFirstDapai in eastSecondMopai:
            return wReachChance

    if len(mopaiAction[SOUTH]) > 1:
        southSecondMopai = str(mopaiAction[SOUTH][1])
        if bool(re.search('[pm]', southSecondMopai)) and westFirstDapai in southSecondMopai:
            return wReachChance

    # 北家
    if len(dapaiAction[NORTH]) > 0:
        northFirstDapai = str(dapaiAction[NORTH][0])
        if 'r' in northFirstDapai:
            wReachChance[NORTH] = True
        if 'a' in northFirstDapai:
            return wReachChance
    else:
        return wReachChance

    return wReachChance
