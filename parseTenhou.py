import json

from KobalabPaipu import QiPai, QiPaiWrapper, PaiAction, ZimoWrapper

json_str = """{"title":["セガサミーフェニックスNo.1　決定戦","最強戦ルール"],"name":["東城りお","茅森早香","近藤誠一","魚谷侑未"],"rule":{"disp":"セガサミーフェニックスNo.1　決定戦","aka":0},"log":[[[1,0,0],[23000,29000,24000,24000],[26],[35],[39,39,39,35,36,42,28,24,31,31,15,13,18],[12,17,28,32,43,47,11,38,32,38,43,45,45,19,32],[42,15,24,28,28,60,32,60,43,60,60,60,60,"r32",60],[38,34,18,27,42,28,27,18,34,47,37,36,27],[19,41,43,21,23,44,33,47,35,44,29,46,41,21,14,26],[42,60,60,60,19,60,34,60,47,60,60,60,60,"r28",60,60],[21,22,23,24,16,16,17,41,44,25,34,25,29],[38,24,42,16,37,45,12,17,23,25,41,33,35,29,18],[41,29,44,38,60,60,60,34,"r42",60,60,60,60,60,60],[11,12,13,14,14,15,37,22,24,26,27,45,46],[42,22,36,47,13,46,31,19,43,14,11,32,36,22,11],[60,46,45,60,11,24,60,60,60,12,37,46,32,11,60],["和了",[0,-2600,5600,0],[2,1,2,"40符2飜2600点","立直(1飜)","ドラ(1飜)"]]]]}"""

gameReport1 = json.loads(json_str)
print(gameReport1['log'])
# [局数，本场，场供]
print(f'changfeng', gameReport1['log'][0][0])
print(f'fenshu', gameReport1['log'][0][1])
print(f'baopai', gameReport1['log'][0][2])
print(f'fubaopai', gameReport1['log'][0][3])
print('------------------------------')
# 初始手牌
print(gameReport1['log'][0][4])
print(gameReport1['log'][0][7])
print(gameReport1['log'][0][10])
print(gameReport1['log'][0][13])
print('------------------------------')
print(gameReport1['log'][0][5])
print(gameReport1['log'][0][6])
print('------------------------------')
print(gameReport1['log'][0][8])
print(gameReport1['log'][0][9])
print('------------------------------')
print(gameReport1['log'][0][11])
print(gameReport1['log'][0][12])
print('------------------------------')
print(gameReport1['log'][0][14])
print(gameReport1['log'][0][15])
print('------------------------------')
print(gameReport1['log'][0][16])

agariYaku = gameReport1['log'][0][16][2][4:]
print(agariYaku)

s = agariYaku[0]
index = s.find('(')
yaku = s[0:index]
han = s[index + 1: index + 2]
print(yaku)
print(han)

SHANGJIA_NOTATION = '-'
DUIJIA_NOTION = '='
XIAJIA_NOTATION = '+'


def listHandToKobaStr(hand):
    kobaDict = {'m': [], 'p': [], 's': [], 'z': []}
    for num in hand:
        if (num.isnumeric()):
            num = int(num)
        else:
            return ''
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
        if (pai == int(wordToConvert)):
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
        fulouDict['showHand'] = [tenhouPai[3:5], tenhouPai[5:7]]
        kobaFulou = listHandToKobaStr([tenhouPai[1:3], tenhouPai[3:5], tenhouPai[5:7]])
        kobaFulou = kobaFulou[0:2] + SHANGJIA_NOTATION + kobaFulou[2:]
        fulouDict['kobaStr'] = kobaFulou
        return fulouDict

    if 'p' in tenhouPai:
        pIndex = tenhouPai.index('p')
        fulouDict['showHand'] = [tenhouPai[pIndex + 1:pIndex + 3]] * 2
        kobaFulou = listHandToKobaStr([tenhouPai[pIndex + 1:pIndex + 3]] * 3)
        if pIndex == 0:
            kobaFulou = kobaFulou[0:2] + SHANGJIA_NOTATION + kobaFulou[2:]
        elif pIndex == 2:
            kobaFulou = kobaFulou[0:3] + DUIJIA_NOTION + kobaFulou[3:]
        elif pIndex == 4:
            kobaFulou = kobaFulou[0:4] + XIAJIA_NOTATION + kobaFulou[4:]
        fulouDict['kobaStr'] = kobaFulou
        return fulouDict

    if 'k' in tenhouPai:
        kIndex = tenhouPai.index('k')
        fulouDict['showHand'] = [tenhouPai[kIndex + 1:kIndex + 3]] * 3
        kobaFulou = listHandToKobaStr([tenhouPai[kIndex + 1:kIndex + 3]] * 4)
        if kIndex == 0:
            kobaFulou = kobaFulou[0:2] + SHANGJIA_NOTATION + kobaFulou[2:]
        elif kIndex == 2:
            kobaFulou = kobaFulou[0:3] + DUIJIA_NOTION + kobaFulou[3:]
        elif kIndex == 4:
            kobaFulou = kobaFulou[0:4] + XIAJIA_NOTATION + kobaFulou[4:]
        fulouDict['kobaStr'] = kobaFulou
        return fulouDict

    if 'a' in tenhouPai:
        aIndex = tenhouPai.index('a')
        fulouDict['showHand'] = [tenhouPai[aIndex + 1:aIndex + 3]] * 4
        kobaFulou = listHandToKobaStr([tenhouPai[aIndex + 1:aIndex + 3]] * 4)
        fulouDict['kobaStr'] = kobaFulou
        return fulouDict


def terminateCondition(mopaiIndex, mopaiLength, dapaiIndex, dapaiLength):
    terminateDict = {"terminate": False, "terminateBy": ""}
    terminateByRonOrRyukyoku = (
            all(v == mopaiLength[0] for v in [mopaiIndex[0], mopaiLength[0], dapaiIndex[0], dapaiLength[0]]) and
            all(v == mopaiLength[1] for v in [mopaiIndex[1], mopaiLength[1], dapaiIndex[1], dapaiLength[1]]) and
            all(v == mopaiLength[2] for v in [mopaiIndex[2], mopaiLength[2], dapaiIndex[2], dapaiLength[2]]) and
            all(v == mopaiLength[3] for v in [mopaiIndex[3], mopaiLength[3], dapaiIndex[3], dapaiLength[3]]))

    if terminateByRonOrRyukyoku:
        terminateDict['terminate'] = True
        terminateDict['terminateBy'] = 'R'  # R for ron or ryukyoku
        return terminateDict

    # for zimo, it will guarantee have one player the index for mopai is 1 more then the dapai
    terminateByZimo = (
                              all(v == mopaiLength[0] for v in [mopaiIndex[0], mopaiLength]) and
                              all(v == dapaiLength[0] for v in [dapaiIndex[0], dapaiLength]) and
                              mopaiIndex[0] - dapaiIndex[0] == 1) or \
                      (all(v == mopaiLength[1] for v in [mopaiIndex[1], mopaiLength]) and
                       all(v == dapaiLength[1] for v in [dapaiIndex[1], dapaiLength]) and
                       mopaiIndex[1] - dapaiIndex[1] == 1) or \
                      (all(v == mopaiLength[2] for v in [mopaiIndex[2], mopaiLength]) and
                       all(v == dapaiLength[2] for v in [dapaiIndex[2], dapaiLength]) and
                       mopaiIndex[2] - dapaiIndex[2] == 1) or \
                      (all(v == mopaiLength[3] for v in [mopaiIndex[3], mopaiLength]) and
                       all(v == dapaiLength[3] for v in [dapaiIndex[3], dapaiLength]) and
                       mopaiIndex[3] - dapaiIndex[3] == 1)
    if terminateByZimo:
        terminateDict['terminate'] = True
        terminateDict['terminateBy'] = 'Z'


def parseKyoku(kyokuReport):
    # return Qipai object
    ju = kyokuReport[0][0][0]
    changfeng = ju / 4
    jushu = ju % 4  # 0 for east, 1 for south, 2 for west, 3 for north
    changbang = kyokuReport[0][0][1]
    lizhibang = kyokuReport[0][0][2]

    # defen is current point start from east, south, west, north
    defen = kyokuReport[0][1]
    defen = defen[jushu:] + defen[0:jushu]

    baopai = kyokuReport[0][2]

    if len(kyokuReport[0][3]) != 0:
        fubaopai = kyokuReport[0][3]
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

    qipai = QiPai(changfeng, jushu, changbang, lizhibang, defen, baopai, fubaopai, shoupai)
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

    mopaiIndex = [0, 0, 0, 0]
    mopaiLength = [len(eastMoPai), len(southMoPai), len(westMoPai), len(northMoPai)]
    dapaiIndex = [0, 0, 0, 0]
    dapaiLength = [len(eastDaPai), len(southDaPai), len(westDaPai), len(northDaPai)]

    currentPlayerIndex = 0
    gameStart = False
    mopai = ''
    dapai = ''
    gameStep = [qiPaiWrapper]

    while not terminateCondition(mopaiIndex, mopaiLength, dapaiIndex, dapaiLength)['terminate']:
        # mopai
        mopai = mopaiAction[currentPlayerIndex][mopaiIndex[currentPlayerIndex]]

        mopaiIndex[currentPlayerIndex] += 1
        terminateDict = terminateCondition(mopaiIndex,mopaiLength,dapaiIndex,dapaiLength)
        isTerminate = terminateDict['terminate']
        # if is zimo
        if isTerminate and terminateDict['terminateBy'] == 'Z':
            zimo = ZimoWrapper(PaiAction(currentPlayerIndex, tenhouNumToPai(mopai)))
            gameStep.append(zimo)

        # dpai
        # other play chi pon kang?
        # currentPlayerIndex swtich to that player
        # otherwise currentPlayerIndex switch add 1
