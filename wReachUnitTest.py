import unittest
from wReachCheck import checkWReach
from mahjong.util.MAJING_CONSTANT import SOUTH, EAST, WEST, NORTH


class WReachChanceTest(unittest.TestCase):
    def test_eastTianHe(self):
        mopaiAction = [[11], [], [], []]
        dapaiAction = [[], [], [], []]
        self.assertEqual(checkWReach(mopaiAction, dapaiAction), [False, False, False, False])

    def test_southDihe(self):
        mopaiAction = [[11], [12], [], []]
        dapaiAction = [[11], [], [], []]
        self.assertEqual(checkWReach(mopaiAction, dapaiAction), [False, False, False, False])

    def test_westDihe(self):
        mopaiAction = [[11], [12], [13], []]
        dapaiAction = [[11], [12], [], []]
        self.assertEqual(checkWReach(mopaiAction, dapaiAction), [False, False, False, False])

    def test_northDihe(self):
        mopaiAction = [[11], [12], [13], [14]]
        dapaiAction = [[11], [12], [13], []]
        self.assertEqual(checkWReach(mopaiAction, dapaiAction), [False, False, False, False])

    def test_eastNormalWReachAndSouthDihe(self):
        mopaiAction = [[11], [12], [], []]
        dapaiAction = [['r11'], [], [], []]
        self.assertEqual(checkWReach(mopaiAction, dapaiAction), [True, False, False, False])

    def test_eastNormalWReachAndWestDihe(self):
        mopaiAction = [[11], [12], [13], []]
        dapaiAction = [['r11'], [12], [], []]
        self.assertEqual(checkWReach(mopaiAction, dapaiAction), [True, False, False, False])

    def test_eastNormalWReachAndNorthDihe(self):
        mopaiAction = [[11], [12], [13], [14]]
        dapaiAction = [['r11'], [12], [13], []]
        self.assertEqual(checkWReach(mopaiAction, dapaiAction), [True, False, False, False])

    def test_allWReachSuccess(self):
        mopaiAction = [[11], [12], [13], [14]]
        dapaiAction = [['r11'], ['r12'], ['r13'], ['r14']]
        self.assertEqual(checkWReach(mopaiAction, dapaiAction), [True, True, True, True])

    def test_eastAnkan(self):
        mopaiAction = [[11], [12], [13], [14]]
        dapaiAction = [['a11'], ['r12'], ['r13'], ['r14']]
        self.assertEqual(checkWReach(mopaiAction, dapaiAction), [False] * 4)

    def test_southAnkan(self):
        mopaiAction = [[11], [12], [13], [14]]
        dapaiAction = [['r11'], ['a12'], ['r13'], ['r14']]
        self.assertEqual(checkWReach(mopaiAction, dapaiAction), [True, False, False, False])

    def test_westAnkan(self):
        mopaiAction = [[11], [12], [13], [14]]
        dapaiAction = [['r11'], ['r12'], ['a13'], ['r14']]
        self.assertEqual(checkWReach(mopaiAction, dapaiAction), [True, True, False, False])

    def test_northAnkan(self):
        mopaiAction = [[11], [12], [13], [14]]
        dapaiAction = [['r11'], ['r12'], ['r13'], ['a14']]
        self.assertEqual(checkWReach(mopaiAction, dapaiAction), [True, True, True, False])


if __name__ == "__main__":
    unittest.main()
