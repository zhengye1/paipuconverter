from mahjong.util.MAJING_CONSTANT import SOUTH, EAST, WEST, NORTH


def checkTenhouChiiHou(mopaiAction, dapaiAction):
    tenhouChiiHouChance = [False] * 4
    # 可能天和
    if len(dapaiAction[EAST]) == 0 and len(mopaiAction[EAST]) == 1:
        tenhouChiiHouChance[EAST] = True
        return tenhouChiiHouChance

    # 摸牌lst大于1说明过了一巡没人胡牌
    if len(mopaiAction[EAST]) > 1 or len(mopaiAction[SOUTH]) > 1 or len(mopaiAction[WEST]) > 1 or len(
            mopaiAction[NORTH]) > 1:
        return tenhouChiiHouChance

    # 要确保东家打出来的没有人吃碰
    eastFirstDapai = str(dapaiAction[EAST][0])

    southFirstMopai = None
    if len(mopaiAction[SOUTH]) > 0:
        southFirstMopai = mopaiAction[SOUTH][0]
        if type(southFirstMopai) == str and eastFirstDapai in southFirstMopai:
            return tenhouChiiHouChance

    westFirstMopai = None
    if len(mopaiAction[WEST]) > 0:
        westFirstMopai = mopaiAction[WEST][0]
        if type(westFirstMopai) == str and eastFirstDapai in westFirstMopai:
            return tenhouChiiHouChance

    northFirstMopai = None
    if len(mopaiAction[NORTH]) > 0:
        northFirstMopai = mopaiAction[NORTH][0]
        if type(northFirstMopai) == str and eastFirstDapai in northFirstMopai:
            return tenhouChiiHouChance

    # 南家肯定有摸牌，因为上面的第一打没人吃碰
    if len(dapaiAction[SOUTH]) == 0:
        tenhouChiiHouChance[SOUTH] = True
        return tenhouChiiHouChance

    # 南家打的牌，只需要看是不是第一打被西家北家碰掉
    southFirstDapai = str(dapaiAction[SOUTH][0])
    if westFirstMopai:
        if type(westFirstMopai) == str and southFirstDapai in westFirstMopai:
            return tenhouChiiHouChance

    if northFirstMopai:
        if type(northFirstMopai) == str and southFirstDapai in northFirstMopai:
            return tenhouChiiHouChance

    if len(dapaiAction[WEST]) == 0:
        tenhouChiiHouChance[WEST] = True
        return tenhouChiiHouChance

    # 西家打的牌就看北家碰不碰了
    westFirstDapai = str(dapaiAction[WEST][0])
    if northFirstMopai:
        if type(northFirstMopai) == str and westFirstDapai in northFirstMopai:
            return tenhouChiiHouChance

    if len(dapaiAction[NORTH]) == 0:
        tenhouChiiHouChance[NORTH] = True
        return tenhouChiiHouChance
    return tenhouChiiHouChance
