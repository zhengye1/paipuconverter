import json
import re

from KobalabPaipu import QiPai, QiPaiWrapper, PaiAction, ZimoWrapper, FulouWrapper, KaiGangWrapper, KaiGang, \
    GangWrapper, GangZimoWrapper, DaPaiWrapper
from mahjong.util.MAJING_CONSTANT import EAST, SOUTH, WEST, NORTH

json_str = """{"title":["セガサミーフェニックスNo.1　決定戦","最強戦ルール"],"name":["東城りお","茅森早香","近藤誠一","魚谷侑未"],"rule":{"disp":"セガサミーフェニックスNo.1　決定戦","aka":0},"log":[[[1,0,0],[23000,29000,24000,24000],[26],[35],[39,39,39,35,36,42,28,24,31,31,15,13,18],[12,17,28,32,43,47,11,38,32,38,43,45,45,19,32],[42,15,24,28,28,60,32,60,43,60,60,60,60,"r32",60],[38,34,18,27,42,28,27,18,34,47,37,36,27],[19,41,43,21,23,44,33,47,35,44,29,46,41,21,14,26],[42,60,60,60,19,60,34,60,47,60,60,60,60,"r28",60,60],[21,22,23,24,16,16,17,41,44,25,34,25,29],[38,24,42,16,37,45,12,17,23,25,41,33,35,29,18],[41,29,44,38,60,60,60,34,"r42",60,60,60,60,60,60],[11,12,13,14,14,15,37,22,24,26,27,45,46],[42,22,36,47,13,46,31,19,43,14,11,32,36,22,11],[60,46,45,60,11,24,60,60,60,12,37,46,32,11,60],["和了",[0,-2600,5600,0],[2,1,2,"40符2飜2600点","立直(1飜)","ドラ(1飜)"]]]]}"""

# gameReport1 = json.loads(json_str)
# print(gameReport1['log'])
# # [局数，本场，场供]
# print(f'changfeng', gameReport1['log'][0][0])
# print(f'fenshu', gameReport1['log'][0][1])
# print(f'baopai', gameReport1['log'][0][2])
# print(f'fubaopai', gameReport1['log'][0][3])
# print('------------------------------')
# # 初始手牌
# print(gameReport1['log'][0][4])
# print(gameReport1['log'][0][7])
# print(gameReport1['log'][0][10])
# print(gameReport1['log'][0][13])
# print('------------------------------')
# print(gameReport1['log'][0][5])
# print(gameReport1['log'][0][6])
# print('------------------------------')
# print(gameReport1['log'][0][8])
# print(gameReport1['log'][0][9])
# print('------------------------------')
# print(gameReport1['log'][0][11])
# print(gameReport1['log'][0][12])
# print('------------------------------')
# print(gameReport1['log'][0][14])
# print(gameReport1['log'][0][15])
# print('------------------------------')
# print(gameReport1['log'][0][16])
#
# agariYaku = gameReport1['log'][0][16][2][4:]
# print(agariYaku)
#
# s = agariYaku[0]
# index = s.find('(')
# yaku = s[0:index]
# han = s[index + 1: index + 2]
# print(yaku)
# print(han)
json_str = """{"title":["セガサミーフェニックスNo.1　決定戦","最強戦ルール"],"name":["東城りお","茅森早香","近藤誠一","魚谷侑未"],"rule":{"disp":"セガサミーフェニックスNo.1　決定戦","aka":0},"log":[[[6,0,0],[33700,27100,28100,11100],[38],[],[16,16,15,45,45,12,39,37,33,26,27,41,44],[29,14,24,39,33,29,35,42,13,47,39,21,32,32,35,36,23,13],[41,29,44,12,24,60,16,60,35,60,37,27,33,33,26,35,14,32],[21,23,24,28,44,45,45,31,34,36,37,37,13],[22,41,31,43,43,25,24,15,34,43,47,38,21,19,41,34,"c141315"],[31,60,60,60,60,28,60,25,44,60,37,47,34,34,60,60,19],[46,27,35,19,23,25,47,11,11,14,22,18,28],[38,25,29,37,42,17,11,21,31,27,27,18,33,18,26,17,17,22],[46,47,25,14,35,25,60,"r42",60,60,60,60,60,60,60,60,60,60],[11,12,13,14,18,19,47,25,24,32,32,46,46],[31,26,29,38,35,19,22,44,41,14,36,44,42,28,43,23,36,39],[47,31,60,19,18,60,11,35,46,46,44,60,60,25,26,43,14,22],["流局",[-1500,1500,1500,-1500]]]]} """
gameReport2 = json.loads(json_str)

json_str = """{"title":["",""],"name":["Aさん","Bさん","私","Dさん"],"rule":{"disp":"般南喰赤","aka":1},"log":[[[4,0,0],[29300,34700,16500,19500],[26,42,17,42,13],[],[11,13,14,17,21,25,34,36,36,43,45,46,47],[33,31,14,41,43,46,43,17,25,25,34,27,26,43],[43,21,46,47,45,60,41,25,60,60,31,60,11,60],[13,15,16,18,52,26,28,35,44,44,45,47,47],[21,"47p4747","4444p44",36,36,16,35,22,53,32,26,33,"c275226",39,32],[60,35,28,60,60,45,60,60,60,60,13,60,26,60,60],[12,19,23,24,28,32,35,37,37,39,39,41,44],[39,15,31,12,44,12,27,31,41,42,41,28,"3737p37","31p3131",21,"m39393939",31,12,37,46],[41,44,19,15,28,44,60,23,24,41,60,60,42,35,60,0,"31k313131","121212a12","3737k3737",60],[13,14,17,19,21,23,28,32,33,38,38,46,47],[29,29,16,24,22,51,23,45,19,27,37,22,24,42,18],[47,46,19,29,21,28,29,60,60,60,60,60,60,60,23],["和了",[0,-32000,32000,0],[2,1,2,"役満32000点","四槓子(役満)"]]]]}"""
tenhouReport = json.loads(json_str)

SHANGJIA_NOTATION = '-'
DUIJIA_NOTION = '='
XIAJIA_NOTATION = '+'


def listHandToKobaStr(hand):
    kobaDict = {'m': [], 'p': [], 's': [], 'z': []}
    for num in hand:
        if type(num) == str and num.isnumeric():
            num = int(num)

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
        if pai == int(wordToConvert):
            tsumokiri = '_'
    elif tenhouNum == 60:
        wordToConvert = pai
        tsumokiri = '_'

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
            kobaFulou = kobaFulou[0:2] + SHANGJIA_NOTATION + kobaFulou[2:]
        elif pIndex == 2:
            kobaFulou = kobaFulou[0:3] + DUIJIA_NOTION + kobaFulou[3:]
        elif pIndex == 4:
            kobaFulou = kobaFulou[0:4] + XIAJIA_NOTATION + kobaFulou[4:]
        fulouDict['kobaStr'] = kobaFulou
        fulouDict['fulouType'] = 'p'
        fulouDict['fulouPai'] = int(tenhouPai[pIndex + 1:pIndex + 3])
        return fulouDict

    # 加杠
    if 'k' in tenhouPai:
        kIndex = tenhouPai.index('k')
        fulouDict['showHand'] = [int(tenhouPai[kIndex + 1:kIndex + 3])] * 3
        kobaFulou = listHandToKobaStr([tenhouPai[kIndex + 1:kIndex + 3]] * 4)
        if kIndex == 0:
            kobaFulou = kobaFulou[0:2] + SHANGJIA_NOTATION + kobaFulou[2:]
        elif kIndex == 2:
            kobaFulou = kobaFulou[0:3] + DUIJIA_NOTION + kobaFulou[3:]
        elif kIndex == 4:
            kobaFulou = kobaFulou[0:4] + XIAJIA_NOTATION + kobaFulou[4:]
        fulouDict['kobaStr'] = kobaFulou
        fulouDict['fulouType'] = 'k'
        fulouDict['fulouPai'] = int(tenhouPai[kIndex + 1:kIndex + 3])
        return fulouDict

    if 'm' in tenhouPai:
        kIndex = tenhouPai.index('m')
        fulouDict['showHand'] = [int(tenhouPai[kIndex + 1:kIndex + 3])] * 3
        kobaFulou = listHandToKobaStr([tenhouPai[kIndex + 1:kIndex + 3]] * 4)
        if kIndex == 0:
            kobaFulou = kobaFulou[0:2] + SHANGJIA_NOTATION + kobaFulou[2:]
        elif kIndex == 2:
            kobaFulou = kobaFulou[0:3] + DUIJIA_NOTION + kobaFulou[3:]
        elif kIndex == 4:
            kobaFulou = kobaFulou[0:4] + XIAJIA_NOTATION + kobaFulou[4:]
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


def terminateCondition(mopaiIndex, mopaiLength, dapaiIndex, dapaiLength):
    terminateDict = {'terminate': False, 'terminateBy': ""}
    print(f'T:{[mopaiIndex[0], mopaiLength[0], dapaiIndex[0], dapaiLength[0]]}')
    print(f'N:{[mopaiIndex[1], mopaiLength[1], dapaiIndex[1], dapaiLength[1]]}')
    print(f'X:{[mopaiIndex[2], mopaiLength[2], dapaiIndex[2], dapaiLength[2]]}')
    print(f'B:{[mopaiIndex[3], mopaiLength[3], dapaiIndex[3], dapaiLength[3]]}')
    eastRCheck = (
            all(v == mopaiLength[0] for v in [mopaiIndex[0], mopaiLength[0]]) and
            all(v == dapaiLength[0] for v in [dapaiIndex[0], dapaiLength[0]]))
    southRCheck = (all(v == mopaiLength[1] for v in [mopaiIndex[1], mopaiLength[1]]) and
                   all(v == dapaiLength[1] for v in [dapaiIndex[1], dapaiLength[1]]))
    westRCheck = (all(v == mopaiLength[2] for v in [mopaiIndex[2], mopaiLength[2]]) and
                  all(v == dapaiLength[2] for v in [dapaiIndex[2], dapaiLength[2]]))
    northRCheck = (all(v == mopaiLength[3] for v in [mopaiIndex[3], mopaiLength[3]]) and
                   all(v == dapaiLength[3] for v in [dapaiIndex[3], dapaiLength[3]]))

    terminateByRonOrRyukyoku = eastRCheck and southRCheck and westRCheck and northRCheck

    if terminateByRonOrRyukyoku:
        terminateDict['terminate'] = True
        terminateDict['terminateBy'] = 'R'  # R for ron or ryukyoku
        return terminateDict

    # for zimo, it will guarantee have one player the index for mopai is 1 more then the dapai
    eastZimoCheck = (
            all(v == mopaiLength[0] for v in [mopaiIndex[0], mopaiLength[0]]) and
            all(v == dapaiLength[0] for v in [dapaiIndex[0], dapaiLength[0]]) and
            mopaiIndex[0] - dapaiIndex[0] == 1)
    southZimoCheck = (all(v == mopaiLength[1] for v in [mopaiIndex[1], mopaiLength[1]]) and
                      all(v == dapaiLength[1] for v in [dapaiIndex[1], dapaiLength[1]]) and
                      mopaiIndex[1] - dapaiIndex[1] == 1)
    westZimoCheck = (all(v == mopaiLength[2] for v in [mopaiIndex[2], mopaiLength[2]]) and
                     all(v == dapaiLength[2] for v in [dapaiIndex[2], dapaiLength[2]]) and
                     mopaiIndex[2] - dapaiIndex[2] == 1)
    northZimoCheck = (all(v == mopaiLength[3] for v in [mopaiIndex[3], mopaiLength[3]]) and
                      all(v == dapaiLength[3] for v in [dapaiIndex[3], dapaiLength[3]]) and
                      mopaiIndex[3] - dapaiIndex[3] == 1)
    terminateByZimo = eastZimoCheck or southZimoCheck or westZimoCheck or northZimoCheck
    if terminateByZimo:
        terminateDict['terminate'] = True
        terminateDict['terminateBy'] = 'Z'
        return terminateDict

    return terminateDict


def buildHands(zimoHand, fulouHand, agariPai=None):
    if agariPai:
        handStr = listHandToKobaStr(zimoHand) + tenhouNumToPai(agariPai)
    else:
        handStr = listHandToKobaStr(zimoHand)
    if fulouHand:
        handStr = handStr + ',' + ','.join(fulouHand)

    return handStr


def getFuFan(fuFan):
    fu = ''
    fan = ''
    defen = ''
    if '符' in fuFan:
        fu = int(fuFan[0:fuFan.index('符')])
        fan = int(fuFan[fuFan.index('符') + 1:fuFan.index('飜')])
        defen = fuFan[fuFan.index('飜') + 1:fuFan.index('点')]
    else:
        pointIndex = re.search(r"\d", fuFan)
        defen = fuFan[pointIndex.start():fuFan.index('点')]

    if '∀' in fuFan:
        defen = int(defen) * 3
    elif '-' in fuFan:
        lowPay = defen[0:defen.index('-')]
        highPay = defen[defen.index('-') + 1:]
        defen = int(lowPay) * 2 + int(highPay)

    return {'fu': fu, 'fan': fan, 'defen': int(defen)}


def parseKyoku(kyokuReport):
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
    mopaiAction = [eastMoPai, southMoPai, westMoPai, northMoPai]
    dapaiAction = [eastDaPai, southDaPai, westDaPai, northDaPai]

    # keep track the fulou
    fulouHand = [[], [], [], []]
    kobaFulouHand = [[], [], [], []]

    mopaiIndex = [0, 0, 0, 0]
    mopaiLength = [len(eastMoPai), len(southMoPai), len(westMoPai), len(northMoPai)]
    dapaiIndex = [0, 0, 0, 0]
    dapaiLength = [len(eastDaPai), len(southDaPai), len(westDaPai), len(northDaPai)]

    print(f'initial: {mopaiLength} | {dapaiLength}')
    print(f'initial list : {mopaiAction} |{dapaiAction}')
    currentPlayerIndex = EAST
    gameStart = False
    mopai = ''
    dapai = ''
    gameStep = [qiPaiWrapper]
    terminateDict = {}
    agariPai = ''
    action = 'M'  # M for mopai, 'P' for dapai
    previous = 'D'

    isTianhe = False
    isDihe = False
    chiPengKang = False  # 检查地和用的
    kangExists = False  # 检查岭上开花
    isLingShang = False
    isHaidi = False
    isHedi = False
    remainTile = 70

    while True:
        if action == 'M':
            print(f'current player {currentPlayerIndex} after dapai {tenhouShoupai[currentPlayerIndex]}')
            print(f'mopaiIndex {mopaiIndex[currentPlayerIndex]}')
            print(f'mopaiAction {mopaiAction[currentPlayerIndex]}')
            mopai = mopaiAction[currentPlayerIndex][mopaiIndex[currentPlayerIndex]]
            print(f"current player {currentPlayerIndex} mopai: {mopai}")
            mopaiIndex[currentPlayerIndex] += 1
            terminateDict = terminateCondition(mopaiIndex, mopaiLength, dapaiIndex, dapaiLength)
            if terminateDict['terminate']:
                if terminateDict['terminateBy'] == 'Z':
                    agariPai = mopai
                    if currentPlayerIndex == EAST and mopaiIndex[currentPlayerIndex] == 1:
                        isTianhe = True
                        break
                    elif currentPlayerIndex != EAST and mopaiIndex[currentPlayerIndex] == 1 and not chiPengKang:
                        isDihe = True
                        break
                    else:
                        if kangExists:
                            kangExists = False
                            isLingShang = True
                            if previous == 'D':  # 从暗杠来的
                                baopaiIndex += 1
                                kaigang = KaiGangWrapper(KaiGang(baopaiLst[baopaiIndex]))
                                gameStep.append(kaigang)
                                gangzimo = GangZimoWrapper(PaiAction(currentPlayerIndex, p=mopai))
                                gameStep.append(gangzimo)
                                remainTile -= 1
                        if remainTile == 0 and not isLingShang:
                            isHaidi = True
                        break
            else:
                if kangExists and previous == 'D':
                    kangExists = False
                    baopaiIndex += 1
                    kaigang = KaiGangWrapper(KaiGang(baopaiLst[baopaiIndex]))
                    gameStep.append(kaigang)
                    gangzimo = GangZimoWrapper(PaiAction(currentPlayerIndex, p=mopai))
                    gameStep.append(gangzimo)
                    remainTile -= 1
                    action = 'D'
                    previous = 'M'

                # 大明杠
                elif type(mopai) == str and ('m' in mopai or 'p' in mopai or 'c' in mopai):
                    fulouDict = fulou(mopai)
                    lst = []
                    for tile in fulouDict['showHand']:
                        tenhouShoupai[currentPlayerIndex].remove(int(tile))
                        lst.append(int(tile))
                    lst.insert(0, fulouDict['fulouType'])
                    lst.append(fulouDict['fulouPai'])
                    fulouHand[currentPlayerIndex].append(lst)
                    kobaFulouHand[currentPlayerIndex].append(fulouDict['kobaStr'])
                    kobaFulou = FulouWrapper(PaiAction(currentPlayerIndex, m=fulouDict['kobaStr']))
                    gameStep.append(kobaFulou)
                    if 'm' in mopai:
                        # 杠dora即开
                        baopaiIndex += 1
                        kaigang = KaiGangWrapper(KaiGang(baopaiLst[baopaiIndex]))
                        gameStep.append(kaigang)
                        dapaiIndex[currentPlayerIndex] += 1  # 因为是0 所以要挪一过去
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
            print(f'current player {currentPlayerIndex} after mopai {tenhouShoupai[currentPlayerIndex]}')
            dapai = dapaiAction[currentPlayerIndex][dapaiIndex[currentPlayerIndex]]
            dapaiIndex[currentPlayerIndex] += 1
            print(f"current player {currentPlayerIndex} dapai: {dapai}")
            if type(dapai) == str and 'a' in dapai:
                fulouDict = fulou(dapai)
                lst = []
                for tile in fulouDict['showHand']:
                    tenhouShoupai[currentPlayerIndex].remove(tile)
                    lst.append(tile)
                lst.insert(0, fulouDict['fulouType'])
                lst.append(fulouDict['fulouPai'])
                fulouHand[currentPlayerIndex].append(lst)
                kobaFulouHand[currentPlayerIndex].append(fulouDict['kobaStr'])
                gang = GangWrapper(PaiAction(currentPlayerIndex, m=fulouDict['kobaStr']))
                gameStep.append(gang)
                kangExists = True
                action = 'M'
                previous = 'D'

            elif type(dapai) == str and 'k' in dapai:
                fulouDict = fulou(dapai)
                pLst = ['p'] + fulouDict['showHand']  # 加杠必定纯在已经被碰掉的情况
                index = fulouHand[currentPlayerIndex].index(pLst)
                fulouHand[currentPlayerIndex][index][0] = 'k'
                fulouHand[currentPlayerIndex][index].append(fulouDict['fulouPai'])
                gang = GangWrapper(PaiAction(currentPlayerIndex, m=fulouDict['kobaStr']))
                gameStep.append(gang)
                kangExists = True
                dapaiIndex[currentPlayerIndex] += 1
                action = 'M'
                previous = 'D'

            else:
                if dapai == 'r60' or dapai == 60:
                    kobaPai = tenhouNumToPai(dapai, mopai)
                    dapai = mopai # 因为是摸切
                    tenhouShoupai[currentPlayerIndex].remove(mopai)
                elif type(dapai) == str and 'r' in dapai:
                    kobaPai = tenhouNumToPai(dapai)
                    tenhouShoupai[currentPlayerIndex].remove(int(dapai[1:]))
                else:
                    kobaPai = tenhouNumToPai(dapai)
                    tenhouShoupai[currentPlayerIndex].remove(dapai)
                kobaDapai = DaPaiWrapper(PaiAction(currentPlayerIndex, p=kobaPai))
                gameStep.append(kobaDapai)

                action = 'M'
                previous = 'D'
                terminateDict = terminateCondition(mopaiIndex, mopaiLength, dapaiIndex, dapaiLength)
                print(f'terminate? {terminateDict}')
                # 打出去的要是结束如果没牌暂且算上是河底
                if terminateDict['terminate'] and terminateDict['terminateBy'] == 'R':
                    agariPai = mopai if dapai == 'r60' or dapai == 60 else dapai
                    if remainTile == 0:
                        isHedi = True
                    break
                else:
                    duijia = (currentPlayerIndex + 2) % 4
                    xiajia = (currentPlayerIndex + 1) % 4
                    shangjia = (currentPlayerIndex + 3) % 4
                    if mopaiIndex[duijia] < mopaiLength[duijia] and bool(
                            re.search('[pm]', str(mopaiAction[duijia][mopaiIndex[duijia]]))) and \
                            str(dapai) in mopaiAction[duijia][mopaiIndex[duijia]]:
                        currentPlayerIndex = duijia
                    elif mopaiIndex[shangjia] < mopaiLength[shangjia] and bool(
                            re.search('[pm]', str(mopaiAction[shangjia][mopaiIndex[shangjia]]))) and \
                            str(dapai) in mopaiAction[shangjia][mopaiIndex[shangjia]]:
                        currentPlayerIndex = shangjia
                    else:
                        currentPlayerIndex = xiajia

    gameResult = kyokuReport[0][16]
    if '和了' in gameResult[0]:
        print(f'RonOrZimo')
        for index in range(1, len(gameResult[1:])):
            fenpei = gameResult[index]
            fenpei = fenpei[jushu:] + fenpei[0:jushu]
            print(fenpei)
            fuFan = gameResult[index + 1][3]
            if '符' in fuFan:
                fu = fuFan[0:fuFan.index('符')]
                fan = fuFan[fuFan.index('符') + 1:fuFan.index('飜')]
                defen = fuFan[fuFan.index('飜') + 1:fuFan.index('点')]

            if terminateDict['terminateBy'] == 'Z':
                # find the correct zimo place
                zimoPlayer = (gameResult[index + 1][0] - 1) % 4
                zimoShoupai = buildHands(tenhouShoupai[zimoPlayer], fulouHand[zimoPlayer], agariPai)
                print(zimoShoupai)

    else:
        print(f'Ryukyoku')
        print(
            f'东家 {tenhouShoupai[EAST]} fulou: {fulouHand[EAST]} convert to koba: {buildHands(tenhouShoupai[EAST], kobaFulouHand[EAST])}')
        print(
            f'南家 {tenhouShoupai[SOUTH]} fulou:{fulouHand[SOUTH]} convert to koba:{buildHands(tenhouShoupai[SOUTH], kobaFulouHand[SOUTH])}')
        print(
            f'西家 {tenhouShoupai[WEST]} fulou:{fulouHand[WEST]} convert to koba:{buildHands(tenhouShoupai[WEST], kobaFulouHand[WEST])}')
        print(
            f'北家 {tenhouShoupai[NORTH]} fulou:{fulouHand[NORTH]} convert to koba:{buildHands(tenhouShoupai[NORTH], kobaFulouHand[NORTH])}')
    print(
        json.dumps(gameStep,
                   default=lambda l: dict((key, value) for key, value in l.encode().items() if value is not None),
                   ensure_ascii=False))


# parseKyoku(gameReport1['log'])
# parseKyoku(gameReport2['log'])
parseKyoku(tenhouReport['log'])
