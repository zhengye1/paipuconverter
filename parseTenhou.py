import json
import re

json_str = """{"title":["セガサミーフェニックスNo.1　決定戦","最強戦ルール"],"name":["東城りお","茅森早香","近藤誠一","魚谷侑未"],"rule":{"disp":"セガサミーフェニックスNo.1　決定戦","aka":0},"log":[[[1,0,0],[23000,29000,24000,24000],[26],[35],[39,39,39,35,36,42,28,24,31,31,15,13,18],[12,17,28,32,43,47,11,38,32,38,43,45,45,19,32],[42,15,24,28,28,60,32,60,43,60,60,60,60,"r32",60],[38,34,18,27,42,28,27,18,34,47,37,36,27],[19,41,43,21,23,44,33,47,35,44,29,46,41,21,14,26],[42,60,60,60,19,60,34,60,47,60,60,60,60,"r28",60,60],[21,22,23,24,16,16,17,41,44,25,34,25,29],[38,24,42,16,37,45,12,17,23,25,41,33,35,29,18],[41,29,44,38,60,60,60,34,"r42",60,60,60,60,60,60],[11,12,13,14,14,15,37,22,24,26,27,45,46],[42,22,36,47,13,46,31,19,43,14,11,32,36,22,11],[60,46,45,60,11,24,60,60,60,12,37,46,32,11,60],["和了",[0,-2600,5600,0],[2,1,2,"40符2飜2600点","立直(1飜)","ドラ(1飜)"]]]]}"""

gameReport1 = json.loads(json_str)
print (f'changfeng', gameReport1['log'][0][0])
print (f'fenshu', gameReport1['log'][0][1])
print (f'baopai', gameReport1['log'][0][2])
print (f'fubaopai', gameReport1['log'][0][3])
print ('------------------------------')
print (gameReport1['log'][0][4])
print (gameReport1['log'][0][7])
print (gameReport1['log'][0][10])
print (gameReport1['log'][0][13])
print ('------------------------------')
print (gameReport1['log'][0][5])
print (gameReport1['log'][0][6])
print ('------------------------------')
print (gameReport1['log'][0][8])
print (gameReport1['log'][0][9])
print ('------------------------------')
print (gameReport1['log'][0][11])
print (gameReport1['log'][0][12])
print ('------------------------------')
print (gameReport1['log'][0][14])
print (gameReport1['log'][0][15])
print ('------------------------------')
print (gameReport1['log'][0][16])

paiAction=gameReport1['log'][0][8][4]
if type(paiAction) == str and 'c' in paiAction:
    print('Chi action')
elif type(paiAction) == str and 'p' in paiAction:
    print('Pong Action')
    
agariYaku = gameReport1['log'][0][16][2][4:]   
print(agariYaku)

s = agariYaku[0]
index = s.find('(')
yaku = s[0:index]
han = s[index + 1: index + 2]
print(yaku)
print(han)
