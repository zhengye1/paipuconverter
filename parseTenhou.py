import json
import re

from KobalabPaipu import QiPai, QiPaiWrapper, PaiAction, ZimoWrapper, FulouWrapper, KaiGangWrapper, KaiGang, \
    GangWrapper, GangZimoWrapper, DaPaiWrapper, Hule, HuleWrapper, PingjuWrapper, Pingju, KobalabPaipu
from mahjong.MahjongTransfer import MahjongTransfer
from mahjong.util.MAJING_CONSTANT import EAST, SOUTH, WEST, NORTH
from tenhouChiihouCheck import checkTenhouChiiHou
from wReachCheck import checkWReach

SHANGJIA_NOTATION = '-'
DUIJIA_NOTION = '='
XIAJIA_NOTATION = '+'
ruleSet = {}


def setupRuleSet():
    pass


def listHandToKobaStr(hand):
    kobaDict = {'m': [], 'p': [], 's': [], 'z': []}
    for num in hand:
        if type(num) == str and num.isnumeric():
            num = int(num)
        # 天凤用51代表红五，52代表红⑤，53代表红5
        if num > 50:
            shu = 0
            pai = num % 10
        else:
            shu = num % 10
            pai = num // 10
        if pai == 1:
            kobaDict['m'].append(str(shu))
        if pai == 2:
            kobaDict['p'].append(str(shu))
        if pai == 3:
            kobaDict['s'].append(str(shu))
        if pai == 4:
            kobaDict['z'].append(str(shu))
    kobaHand = ''
    for key, value in kobaDict.items():
        if value:
            value.sort()
            kobaHand += (key + ''.join(value))

    return kobaHand


def tenhouNumToPai(tenhouNum, pai=None):
    wordToConvert = tenhouNum
    riichi = ''
    tsumokiri = ''

    if type(tenhouNum) == str and 'r' in tenhouNum:
        wordToConvert = tenhouNum[1:]
        riichi = '*'
        if int(wordToConvert) == 60:
            wordToConvert = pai
            tsumokiri = '_'
    elif tenhouNum == 60:
        wordToConvert = pai
        tsumokiri = '_'

    intFormatWord = int(wordToConvert)
    if 51 <= intFormatWord <= 53:
        pai = intFormatWord % 10
        shu = 0
    else:
        shu = int(wordToConvert) % 10
        pai = int(wordToConvert) // 10
    mian = ''
    if pai == 1:
        mian = 'm'
    if pai == 2:
        mian = 'p'
    if pai == 3:
        mian = 's'
    if pai == 4:
        mian = 'z'

    return mian + str(shu) + tsumokiri + riichi


def fulou(tenhouPai):
    fulouDict = {}
    # for chi
    if 'c' in tenhouPai:
        fulouDict['showHand'] = [int(tenhouPai[3:5]), int(tenhouPai[5:7])]
        kobaFulou = listHandToKobaStr([tenhouPai[1:3], tenhouPai[3:5], tenhouPai[5:7]])
        kobaFulou = kobaFulou.replace(tenhouPai[1:3][1], tenhouPai[1:3][1] + SHANGJIA_NOTATION)
        fulouDict['kobaStr'] = kobaFulou
        fulouDict['fulouType'] = 'c'
        fulouDict['fulouPai'] = int(tenhouPai[1:3])
        return fulouDict

    if 'p' in tenhouPai:
        pIndex = tenhouPai.index('p')
        fulouDict['showHand'] = [int(tenhouPai[pIndex + 1:pIndex + 3])] * 2
        kobaFulou = listHandToKobaStr([tenhouPai[pIndex + 1:pIndex + 3]] * 3)
        if pIndex == 0:
            kobaFulou = kobaFulou + SHANGJIA_NOTATION
        elif pIndex == 2:
            kobaFulou = kobaFulou + DUIJIA_NOTION
        elif pIndex == 4:
            kobaFulou = kobaFulou + XIAJIA_NOTATION
        fulouDict['kobaStr'] = kobaFulou
        fulouDict['fulouType'] = 'p'
        fulouDict['fulouPai'] = int(tenhouPai[pIndex + 1:pIndex + 3])
        return fulouDict

    # 加杠
    if 'k' in tenhouPai:
        kIndex = tenhouPai.index('k')
        fulouDict['showHand'] = [int(tenhouPai[kIndex + 1:kIndex + 3])] * 3
        kobaFulou = listHandToKobaStr([tenhouPai[kIndex + 1:kIndex + 3]] * 3)
        if kIndex == 0:
            kobaFulou = kobaFulou + SHANGJIA_NOTATION + kobaFulou[1]
        elif kIndex == 2:
            kobaFulou = kobaFulou + DUIJIA_NOTION + kobaFulou[1]
        elif kIndex == 4:
            kobaFulou = kobaFulou + XIAJIA_NOTATION + kobaFulou[1]
        fulouDict['kobaStr'] = kobaFulou
        fulouDict['fulouType'] = 'k'
        fulouDict['fulouPai'] = int(tenhouPai[kIndex + 1:kIndex + 3])
        return fulouDict

    if 'm' in tenhouPai:
        kIndex = tenhouPai.index('m')
        fulouDict['showHand'] = [int(tenhouPai[kIndex + 1:kIndex + 3])] * 3
        kobaFulou = listHandToKobaStr([tenhouPai[kIndex + 1:kIndex + 3]] * 4)
        if kIndex == 0:
            kobaFulou = kobaFulou + SHANGJIA_NOTATION
        elif kIndex == 2:
            kobaFulou = kobaFulou + DUIJIA_NOTION
        elif kIndex == 4:
            kobaFulou = kobaFulou + XIAJIA_NOTATION
        fulouDict['kobaStr'] = kobaFulou
        fulouDict['fulouType'] = 'm'
        fulouDict['fulouPai'] = int(tenhouPai[kIndex + 1:kIndex + 3])
        return fulouDict

    if 'a' in tenhouPai:
        aIndex = tenhouPai.index('a')
        fulouDict['showHand'] = [int(tenhouPai[aIndex + 1:aIndex + 3])] * 4
        kobaFulou = listHandToKobaStr([tenhouPai[aIndex + 1:aIndex + 3]] * 4)
        fulouDict['kobaStr'] = kobaFulou
        fulouDict['fulouType'] = 'a'
        fulouDict['fulouPai'] = int(tenhouPai[aIndex + 1:aIndex + 3])
        return fulouDict


def indexCheck(mopaiAction, dapaiAction, mopaiLength, dapaiLength, player):
    return len(mopaiAction[player]) == len(dapaiAction[player]) == 0 and mopaiLength[player] - dapaiLength[player] == 1


def terminateCondition(mopaiAction, mopaiLength, dapaiAction, dapaiLength):
    terminateDict = {'terminate': False, 'terminateBy': ""}
    eastZimoCheck = indexCheck(mopaiAction, dapaiAction, mopaiLength, dapaiLength, EAST)
    southZimoCheck = indexCheck(mopaiAction, dapaiAction, mopaiLength, dapaiLength, SOUTH)
    westZimoCheck = indexCheck(mopaiAction, dapaiAction, mopaiLength, dapaiLength, WEST)
    northZimoCheck = indexCheck(mopaiAction, dapaiAction, mopaiLength, dapaiLength, NORTH)

    terminateByZimo = eastZimoCheck or southZimoCheck or westZimoCheck or northZimoCheck
    if terminateByZimo:
        terminateDict['terminate'] = True
        terminateDict['terminateBy'] = 'Z'
        return terminateDict

    terminateByRonOrRyukyoku = \
        len(mopaiAction[EAST]) == len(mopaiAction[SOUTH]) == len(mopaiAction[WEST]) == len(mopaiAction[NORTH]) \
        == len(dapaiAction[EAST]) == len(dapaiAction[SOUTH]) == len(dapaiAction[WEST]) == len(dapaiAction[NORTH]) == 0

    if terminateByRonOrRyukyoku:
        terminateDict['terminate'] = True
        terminateDict['terminateBy'] = 'R'  # R for ron or ryukyoku
        return terminateDict

    return terminateDict


def buildHands(zimoHand, fulouHand, agariPai=None):
    if agariPai:
        handStr = listHandToKobaStr(zimoHand) + tenhouNumToPai(agariPai)
    else:
        handStr = listHandToKobaStr(zimoHand)
    if len(fulouHand) != 0:
        handStr = handStr + ',' + ','.join(fulouHand)

        print(f'fulou hand {fulouHand} final hand string {handStr}')
    return handStr


def resetYifa(riichiYifa, player=-1):
    if player >= 0:
        if riichiYifa[player] == 'RI':
            riichiYifa[player] = 'R'
    else:
        for i, rI in enumerate(riichiYifa):
            if 'RI' in rI:
                riichiYifa[i] = 'R'
            else:
                riichiYifa[i] = ''


riichiYifa = ['', '', '', '']  # 检查立直一发的


def resetRiichiYifa():
    riichiYifa = ['', '', '', '']


def parseKyoku(kyokuReport, ruleSet=None):
    # return Qipai object
    ju = kyokuReport[0][0][0]
    changfeng = ju // 4
    jushu = ju % 4  # 0 for east, 1 for south, 2 for west, 3 for north
    changbang = kyokuReport[0][0][1]
    lizhibang = kyokuReport[0][0][2]

    # defen is current point start from east, south, west, north
    defen = kyokuReport[0][1]
    defen = defen[jushu:] + defen[0:jushu]

    baopaiIndex = 0
    baopaiLst = kyokuReport[0][2]
    baopai = baopaiLst[baopaiIndex]
    fubaopaiLst = kyokuReport[0][3]
    fubaopaiIndex = 0

    if len(fubaopaiLst) != 0:
        fubaopai = fubaopaiLst[fubaopaiIndex]
    else:
        fubaopai = None

    # 4,7,10,13 is the open hand
    indexSequence = [4, 7, 10, 13]

    eastIndex = indexSequence[jushu % 4]
    southIndex = indexSequence[(jushu + 1) % 4]
    westIndex = indexSequence[(jushu + 2) % 4]
    northIndex = indexSequence[(jushu + 3) % 4]

    eastStartHand = kyokuReport[0][eastIndex]
    southStartHand = kyokuReport[0][southIndex]
    westStardHand = kyokuReport[0][westIndex]
    northStartHand = kyokuReport[0][northIndex]

    # use for keep track final hand
    tenhouShoupai = [[h for h in eastStartHand], [h for h in southStartHand], [h for h in westStardHand],
                     [h for h in northStartHand]]

    # for kobolab shoupai
    shoupai = [listHandToKobaStr(eastStartHand), listHandToKobaStr(southStartHand), listHandToKobaStr(westStardHand),
               listHandToKobaStr(northStartHand)]

    qipai = QiPai(changfeng, jushu, changbang, lizhibang, defen, tenhouNumToPai(baopai), shoupai)
    qiPaiWrapper = QiPaiWrapper(qipai)

    eastMoPai = kyokuReport[0][eastIndex + 1]
    eastDaPai = kyokuReport[0][eastIndex + 2]
    southMoPai = kyokuReport[0][southIndex + 1]
    southDaPai = kyokuReport[0][southIndex + 2]
    westMoPai = kyokuReport[0][westIndex + 1]
    westDaPai = kyokuReport[0][westIndex + 2]
    northMoPai = kyokuReport[0][northIndex + 1]
    northDaPai = kyokuReport[0][northIndex + 2]
    mopaiAction = [[mp for mp in eastMoPai], [mp for mp in southMoPai], [mp for mp in westMoPai],
                   [mp for mp in northMoPai]]
    dapaiAction = [[dp for dp in eastDaPai], [dp for dp in southDaPai], [dp for dp in westDaPai],
                   [dp for dp in northDaPai]]

    # keep track the fulou
    fulouHand = [[], [], [], []]
    kobaFulouHand = [[], [], [], []]

    mopaiLength = [len(eastMoPai), len(southMoPai), len(westMoPai), len(northMoPai)]
    dapaiLength = [len(eastDaPai), len(southDaPai), len(westDaPai), len(northDaPai)]

    currentPlayerIndex = EAST

    gameStep = [qiPaiWrapper]

    action = 'M'  # M for mopai, 'P' for dapai
    previous = 'D'

    kangExists = False  # 检查岭上开花
    isLingShang = False
    isHaidi = False
    isHedi = False
    isQiangGang = False

    if ruleSet and not ruleSet.yifa:
        RIICHI_YIFA = 'R'
    else:
        RIICHI_YIFA = 'RI'

    remainTile = 70
    tenhouChiiHouCheck = checkTenhouChiiHou(mopaiAction, dapaiAction)
    wReachChanceCheck = checkWReach(mopaiAction, dapaiAction)
    resetRiichiYifa()
    while True:
        if action == 'M':
            mopai = mopaiAction[currentPlayerIndex].pop(0)
            terminateDict = terminateCondition(mopaiAction, mopaiLength, dapaiAction, dapaiLength)
            if terminateDict['terminate']:
                if terminateDict['terminateBy'] == 'Z':
                    agariPai = mopai
                    if kangExists:
                        kangExists = False
                        isLingShang = True
                        if previous == 'D':  # 从暗杠来的
                            baopaiIndex += 1
                            kaigang = KaiGangWrapper(KaiGang(tenhouNumToPai(baopaiLst[baopaiIndex])))
                            gameStep.append(kaigang)
                            gangzimo = GangZimoWrapper(PaiAction(currentPlayerIndex, p=tenhouNumToPai(mopai)))
                            gameStep.append(gangzimo)
                            tenhouShoupai[currentPlayerIndex].append(mopai)
                            remainTile -= 1
                    if remainTile == 0 and not isLingShang:
                        isHaidi = True
                    kobaMopai = tenhouNumToPai(mopai)
                    zimo = ZimoWrapper(PaiAction(currentPlayerIndex, p=kobaMopai))
                    gameStep.append(zimo)
                    break

            else:
                resetYifa(riichiYifa, currentPlayerIndex)
                if kangExists and previous == 'D':
                    resetYifa(riichiYifa)
                    kangExists = False
                    baopaiIndex += 1
                    if ruleSet and ruleSet.kanAri:
                        kaigang = KaiGangWrapper(KaiGang(tenhouNumToPai(baopaiLst[baopaiIndex])))
                        gameStep.append(kaigang)
                    gangzimo = GangZimoWrapper(PaiAction(currentPlayerIndex, p=tenhouNumToPai(mopai)))
                    gameStep.append(gangzimo)
                    tenhouShoupai[currentPlayerIndex].append(mopai)
                    remainTile -= 1
                    action = 'D'
                    previous = 'M'

                # 大明杠
                elif type(mopai) == str and ('m' in mopai or 'p' in mopai or 'c' in mopai):
                    resetYifa(riichiYifa)
                    chiPengKang = True
                    junme = -1
                    fulouDict = fulou(mopai)
                    lst = []
                    for tile in fulouDict['showHand']:
                        if tile % 10 == 0:  # 遇到红五了
                            tenhouShoupai[currentPlayerIndex].remove(50 + tile // 10)
                        else:
                            tenhouShoupai[currentPlayerIndex].remove(tile)
                        lst.append(int(tile))
                    lst.insert(0, fulouDict['fulouType'])
                    lst.append(fulouDict['fulouPai'])
                    fulouHand[currentPlayerIndex].append(lst)
                    kobaFulouHand[currentPlayerIndex].append(fulouDict['kobaStr'])
                    kobaFulou = FulouWrapper(PaiAction(currentPlayerIndex, m=fulouDict['kobaStr']))
                    gameStep.append(kobaFulou)
                    if 'm' in mopai:
                        dapaiAction[currentPlayerIndex].pop(0)  # 因为是0 所以要挪一过去
                        kangExists = True
                    else:
                        action = 'D'
                        previous = 'M'

                else:
                    tenhouShoupai[currentPlayerIndex].append(mopai)
                    kobaMopai = tenhouNumToPai(mopai)
                    zimo = ZimoWrapper(PaiAction(currentPlayerIndex, p=kobaMopai))
                    gameStep.append(zimo)
                    action = 'D'
                    previous = 'M'
                    remainTile -= 1
        else:
            dapai = dapaiAction[currentPlayerIndex].pop(0)
            if type(dapai) == str and 'a' in dapai:
                resetYifa(riichiYifa)
                chiPengKang = True
                junme = -1
                fulouDict = fulou(dapai)
                lst = []
                for tile in fulouDict['showHand']:
                    if tile % 10 == 0:  # 遇到红五了
                        tenhouShoupai[currentPlayerIndex].remove(50 + tile // 10)
                    else:
                        tenhouShoupai[currentPlayerIndex].remove(tile)
                    lst.append(tile)
                lst.insert(0, fulouDict['fulouType'])
                fulouHand[currentPlayerIndex].append(lst)
                kobaFulouHand[currentPlayerIndex].append(fulouDict['kobaStr'])
                gang = GangWrapper(PaiAction(currentPlayerIndex, m=fulouDict['kobaStr']))
                gameStep.append(gang)
                kangExists = True
                action = 'M'
                previous = 'D'

            elif type(dapai) == str and 'k' in dapai:
                chiPengKang = True
                junme = -1
                print(f'fulou dict{fulouDict}')
                kobaFulouHand[currentPlayerIndex].remove(fulouDict['kobaStr'])
                fulouDict = fulou(dapai)
                pLst = ['p'] + fulouDict['showHand']  # 加杠必定在已经被碰掉的情况
                index = fulouHand[currentPlayerIndex].index(pLst)
                fulouHand[currentPlayerIndex][index][0] = 'k'
                fulouHand[currentPlayerIndex][index].append(fulouDict['fulouPai'])
                gang = GangWrapper(PaiAction(currentPlayerIndex, m=fulouDict['kobaStr']))
                gameStep.append(gang)
                tenhouShoupai[currentPlayerIndex].remove(fulouDict['fulouPai'])
                kobaFulouHand[currentPlayerIndex].append(fulouDict['kobaStr'])
                if terminateCondition(mopaiAction, mopaiLength, dapaiAction, dapaiLength)['terminate']:
                    isQiangGang = True
                    agariPai = dapai
                    break
                resetYifa(riichiYifa)
                kangExists = True
                action = 'M'
                previous = 'D'

            else:
                if dapai == 'r60' or dapai == 60:
                    kobaPai = tenhouNumToPai(dapai, mopai)
                    if type(dapai) == str and 'r' in dapai:
                        riichiYifa[currentPlayerIndex] = RIICHI_YIFA
                    dapai = mopai  # 因为是摸切
                    tenhouShoupai[currentPlayerIndex].remove(mopai)

                elif type(dapai) == str and 'r' in dapai:
                    kobaPai = tenhouNumToPai(dapai)
                    riichiYifa[currentPlayerIndex] = RIICHI_YIFA
                    tenhouShoupai[currentPlayerIndex].remove(int(dapai[1:]))
                else:
                    kobaPai = tenhouNumToPai(dapai)
                    tenhouShoupai[currentPlayerIndex].remove(dapai)
                kobaDapai = DaPaiWrapper(PaiAction(currentPlayerIndex, p=kobaPai))
                gameStep.append(kobaDapai)
                action = 'M'
                previous = 'D'
                terminateDict = terminateCondition(mopaiAction, mopaiLength, dapaiAction, dapaiLength)
                # 打出去的要是结束如果没牌暂且算上是河底
                if terminateDict['terminate'] and terminateDict['terminateBy'] == 'R':
                    agariPai = mopai if dapai == 'r60' or dapai == 60 else dapai
                    agariPai = int(dapai[1:]) if type(dapai) == str and 'r' in dapai else dapai  # 燕返
                    if remainTile == 0:
                        isHedi = True
                    break
                else:
                    if type(dapai) == str and 'r' in dapai:
                        riichiYifa[currentPlayerIndex] = RIICHI_YIFA
                    shangjia = (currentPlayerIndex + 3) % 4
                    duijia = (currentPlayerIndex + 2) % 4
                    xiajia = (currentPlayerIndex + 1) % 4
                    if len(mopaiAction[duijia]) != 0 and bool(re.search('[pm]', str(mopaiAction[duijia][0]))) \
                            and str(dapai) in mopaiAction[duijia][0]:
                        junme = -1
                        currentPlayerIndex = duijia
                    elif len(mopaiAction[shangjia]) != 0 and bool(re.search('[pm]', str(mopaiAction[shangjia][0]))) \
                            and str(dapai) in mopaiAction[shangjia][0]:
                        junme = -1
                        currentPlayerIndex = shangjia
                    else:
                        if len(mopaiAction[xiajia]) != 0 and bool(re.search('[pm]', str(mopaiAction[xiajia][0]))) \
                                and str(dapai) in mopaiAction[xiajia][0]:
                            junme = -1
                        currentPlayerIndex = xiajia

    gameResult = kyokuReport[0][16]
    print(f'{"东" if changfeng == 0 else "南"}{jushu + 1}局 {changbang}本场')
    if '和了' in gameResult[0]:
        print(f'RonOrZimo')
        for index in range(1, len(gameResult[1:])):
            fenpei = gameResult[index]
            print(f'before {fenpei}')
            fenpei = fenpei[jushu:] + fenpei[0:jushu]
            print(fenpei)
            fuFan = gameResult[index + 1][3]
            print(f'index + 1 {gameResult[index + 1]}')
            if terminateDict['terminateBy'] == 'Z':
                # find the correct zimo place
                agariShoupai = buildHands(tenhouShoupai[currentPlayerIndex], kobaFulouHand[currentPlayerIndex],
                                          agariPai)
                agariPlayer = currentPlayerIndex
                ronFormat = 'Z'
                print(agariShoupai)

            else:
                agariPlayer = (gameResult[index + 1][0] - ju) % 4
                houjyuPlayer = (gameResult[index + 1][1] - ju) % 4

                agariShoupai = buildHands(tenhouShoupai[agariPlayer], kobaFulouHand[agariPlayer], agariPai)
                print(
                    f'jushu {jushu} Ron by {agariPlayer} <- {houjyuPlayer} with hand {agariShoupai} and agaripai {agariPai}')
                ronFormat = 'R'
            finalInner = [h if h // 10 != 5 else (h % 10 * 10) for h in tenhouShoupai[agariPlayer]]
            finalInner.append(agariPai)
            transfer = MahjongTransfer(finalInner, fulouHand[agariPlayer], agariPai)
            transfer.ronFormat = ronFormat
            group = transfer.toMahjongGroup()
            if len(group) == 0:
                print(f'Tenhou shoupai {tenhouShoupai[agariPlayer]} and fulou hand: {fulouHand[agariPlayer]}')
                print(f'baopai {baopaiLst} ura {fubaopaiLst}')
                print(f'final innner {finalInner} fulouhand {fulouHand[agariPlayer]}')
                break
            for g in group:
                g.setSpecial(agariPlayer, changfeng,
                             tianhe=agariPlayer == EAST and tenhouChiiHouCheck[agariPlayer],
                             dihe=agariPlayer != EAST and tenhouChiiHouCheck[agariPlayer],
                             isLingShang=isLingShang, isQiangGang=isQiangGang,
                             isRiichi=('R' in riichiYifa[agariPlayer] and not wReachChanceCheck[agariPlayer]),
                             isWReach=('R' in riichiYifa[agariPlayer] and wReachChanceCheck[agariPlayer]),
                             isYifa=('RI' in riichiYifa[agariPlayer]),
                             isHedi=isHedi, isHaidi=isHaidi)
                g.setDora(baopaiLst, fubaopaiLst)
                g.finalCheck()

            group.sort(key=lambda x: (x.score, x.fan, x.fu), reverse=True)

            agariGroup = group[0]
            baojia = houjyuPlayer if ronFormat == 'R' else None
            fubaopai = None if len(fubaopaiLst) == 0 else [tenhouNumToPai(tile) for tile in fubaopaiLst]
            fu = agariGroup.fu if len(agariGroup.yakumans) == 0 else None
            fan = agariGroup.fan if len(agariGroup.yakumans) == 0 else None
            defen = agariGroup.score
            damanguan = 1 if len(agariGroup.yakumans) > 0 else None
            hupai = [yakuman for yakuman in agariGroup.yakumans] if len(agariGroup.yakumans) > 0 \
                else [yaku for yaku in agariGroup.yakus]
            hule = Hule(l=agariPlayer, shoupai=agariShoupai, baojia=baojia,
                        fubaopai=fubaopai,
                        fu=fu, fanshu=fan, damanguan=damanguan,
                        defen=defen, hupai=hupai, fenpei=fenpei)
            huleWrapper = HuleWrapper(hule)
            gameStep.append(huleWrapper)
    else:
        status = ''
        print(f'Ryukyoku')
        print(f'riichi yifa{riichiYifa}')
        if len(gameResult) == 1:
            # 全员听牌或者没听
            status = gameResult[0]
            fenpei = [0, 0, 0, 0]
        else:
            fenpei = gameResult[1]
            fenpei = fenpei[jushu:] + fenpei[0:jushu]
        print(f'流局分数分配{fenpei}')
        shoupai = []
        for i, fenshu in enumerate(fenpei):
            if fenshu > 0 or status == '全員聴牌':
                shoupai.append(buildHands(tenhouShoupai[i], kobaFulouHand[i]))
            else:
                shoupai.append('')
        pinju = PingjuWrapper(Pingju(name='流局', shoupai=shoupai, fenpei=fenpei))
        gameStep.append(pinju)

        print(
            f'东家 {tenhouShoupai[EAST]} fulou: {fulouHand[EAST]} convert to koba: {buildHands(tenhouShoupai[EAST], kobaFulouHand[EAST])}')
        print(
            f'南家 {tenhouShoupai[SOUTH]} fulou:{fulouHand[SOUTH]} convert to koba:{buildHands(tenhouShoupai[SOUTH], kobaFulouHand[SOUTH])}')
        print(
            f'西家 {tenhouShoupai[WEST]} fulou:{fulouHand[WEST]} convert to koba:{buildHands(tenhouShoupai[WEST], kobaFulouHand[WEST])}')
        print(
            f'北家 {tenhouShoupai[NORTH]} fulou:{fulouHand[NORTH]} convert to koba:{buildHands(tenhouShoupai[NORTH], kobaFulouHand[NORTH])}')
    print("========================")
    kyokuReport = json.dumps(gameStep,
                             default=lambda l: dict(
                                 (key, value) for key, value in l.encode().items() if value is not None),
                             ensure_ascii=False)
    print(f'kyokuReport: {kyokuReport}')
    return gameStep


def parseHanchan(tenhouLine, ruleSet=None):
    title = ''
    player = ''
    qijia = ''
    log = []
    defen = []
    rank = []
    point = [0, 0, 0, 0]
    for i, kyokuStr in enumerate(tenhouLine):
        kyoku = json.loads(kyokuStr)
        # 半庄开始
        if i == 0:
            title = kyoku['title'][0]
            player = kyoku['name']
            qijia = EAST
        log.append(parseKyoku(kyoku['log'], ruleSet))
        if i == len(tenhouLine) - 1:
            initialKyokuPoint = kyoku['log'][0][1]
            tenshuChange = kyoku['log'][0][16][1]
            print(f'all last initial:{initialKyokuPoint} and tenshu change: {tenshuChange}')
            defen = [initialKyokuPoint[i] + tenshuChange[i] for i in range(4)]
            riichiYifaOriginal = riichiYifa[1:] + [riichiYifa[0]]
            print(f'riichiyifa{riichiYifaOriginal}')
            defen = [defen[i] - 1000 if 'R' in riichiYifaOriginal[i] else defen[i] for i in range(4)]

            rank = [0] * len(defen)
            for i, x in enumerate(sorted(range(len(defen)), key=lambda y: defen[y], reverse=True)):
                rank[x] = i + 1
            print(f'final defen {defen} and rank{rank}')
            point = ruleSet.calculatePoint(defen, rank)

        print("=======================")
    kobaPaipu = KobalabPaipu(title, player, qijia, log, defen, rank, point)
    kobaReport = json.dumps(kobaPaipu,
                            default=lambda l: dict(
                                (key, value) for key, value in l.encode().items() if value is not None),
                            ensure_ascii=False)

    print(f"Should be all OK to write: {kobaReport}")
    return kobaReport
