# 面子类型
from mahjong.RuleSet import RuleSet

SHUNZI = 0
KEZI = 1
GANG = 2

# 和牌类型
LIANGMIAN = 0
SHUANGPENG = 1
# 单骑，坎张，边张
SINGLE_WAIT = 2

# YAKU_TYPE
SEVEN_PAIR = 7
KOKUSHI = 13
NORMAL = 0

INNER = 0
FULOU = 1

EAST = 0
SOUTH = 1
WEST = 2
NORTH = 3

OYA_YAKUMAN = 48000
KODOMO_YAKUMAN = 32000

MAN = 1
PIN = 2
SOUZI = 3
JIPAI = 4

HATSU = 46

M_LEAGUE_RULE = RuleSet(25000, 30000, [50, 10, -10, -30], True, True, True, True, True, 2, True, False, True, False,
                        "divided", "top")
SAIKYOSEN_RULE = RuleSet(30000, 30000, [30, 10, -10, -30], False, True, True, True, True, 2, False, False, True, False,
                         "divided", "removed")
A_RULE = RuleSet(30000, 30000, [[12, -1, -3, -8], [8, 4, -4, -8], [8, 3, 1, -12]], False, False, False, False,
                 False, 4, True, False, True, False, "divided", "removed")
