#!/usr/bin/env python2
from pow import (
    gbp_basic,
    hash_nonce,
    hash_xi,
    zcash_person,
)
from pyblake2 import blake2b
import unittest

ZCASH_TEST_VECTORS = [
    (96, 5, b'block header', 0, []),
    (96, 5, b'block header', 1, []),
    (96, 5, b'block header', 2, [
  [3389, 110764, 37520, 58346, 4112, 61459, 47776, 84587, 11643, 34988, 36560, 98422, 36242, 47864, 76737, 80053, 3422, 74285, 77922, 101376, 58602, 104312, 64513, 89638, 10240, 76326, 27584, 36949, 43637, 75295, 56666, 91601],
    ]),
    (96, 5, b'block header', 10, [
  [787, 20674, 53516, 73404, 4022, 110690, 35427, 58606, 22749, 129878, 34185, 112292, 56949, 100033, 100182, 115894, 13225, 23627, 94405, 114446, 14243, 118738, 36358, 79934, 49517, 78196, 85137, 85376, 57430, 77040, 102235, 114826],
  [2656, 33964, 2683, 87167, 19223, 113046, 67505, 101388, 12585, 77102, 18807, 117333, 70932, 106281, 85381, 118430, 6664, 12926, 6868, 33372, 15227, 128690, 89250, 96792, 14322, 23199, 32286, 57355, 54637, 130050, 70335, 99067],
  [4207, 21880, 85981, 113070, 16301, 41187, 88537, 103201, 6295, 86241, 21605, 56786, 28030, 80680, 52120, 79774, 7875, 56055, 25882, 112870, 9719, 40271, 35223, 50883, 27959, 92599, 70158, 106739, 31838, 117463, 69735, 83367],
  [9637, 51478, 44285, 93559, 76796, 108515, 123998, 124708, 17379, 29371, 21401, 48583, 62725, 80279, 109465, 111074, 16793, 128680, 42090, 42327, 34750, 101600, 64379, 84300, 48256, 49313, 82752, 87659, 67566, 117002, 78981, 122103],
    ]),
    (96, 5, b'block header', 11, [
  [1638, 116919, 4749, 45156, 58749, 103900, 92294, 109359, 16076, 89395, 21938, 121398, 18847, 43685, 53116, 114427, 7067, 69901, 23179, 73689, 33890, 103453, 66168, 129978, 57522, 115912, 81791, 123826, 76090, 96629, 120289, 123662],
  [2957, 38313, 18116, 83967, 10458, 51007, 13244, 61860, 16311, 113118, 76034, 90819, 43134, 61561, 68365, 93667, 7626, 86183, 62381, 109415, 90075, 114836, 93702, 131024, 19175, 124662, 20036, 34896, 33427, 60491, 103672, 107450],
    ]),

    (96, 5, b'Equihash is an asymmetric PoW based on the Generalised Birthday problem.', 0, []),
    (96, 5, b'Equihash is an asymmetric PoW based on the Generalised Birthday problem.', 1, [
  [2154, 87055, 7922, 12920, 45189, 49783, 122795, 124296, 2432, 48178, 48280, 67880, 3912, 62307, 10987, 93891, 19673, 24483, 33984, 91500, 38171, 85505, 94625, 106140, 31530, 60861, 59391, 117337, 68078, 129665, 126764, 128278],
  [3521, 83631, 86264, 106366, 62729, 102245, 74046, 114174, 45281, 59655, 45686, 60328, 71798, 123267, 83891, 121660, 12375, 83210, 94890, 120434, 35140, 109028, 65151, 89820, 18962, 24744, 55758, 116061, 63695, 125324, 98242, 125805],
    ]),
    (96, 5, b'Equihash is an asymmetric PoW based on the Generalised Birthday problem.', 2, [
  [6310, 126030, 19266, 92728, 22993, 43617, 59500, 110969, 8633, 95173, 11769, 69347, 21455, 114538, 67360, 77234, 7538, 84336, 27001, 79803, 33408, 111870, 42328, 48938, 19045, 48081, 55314, 86688, 24992, 93296, 68568, 106618],
    ]),
    (96, 5, b'Equihash is an asymmetric PoW based on the Generalised Birthday problem.', 10, [
  [6768, 10445, 80746, 128923, 28583, 50486, 47353, 58892, 35052, 45980, 61445, 103307, 67117, 94090, 78715, 109244, 20795, 102820, 31354, 91894, 50174, 126488, 77522, 80142, 28219, 74825, 66159, 73984, 60786, 121859, 70144, 120379],
  [7865, 119271, 33055, 103984, 19519, 65954, 36562, 123493, 10038, 60327, 10645, 98001, 10748, 108967, 73961, 99283, 20538, 21631, 41159, 81213, 71041, 74642, 97906, 107612, 47736, 74711, 75451, 117319, 53428, 73882, 73362, 125084],
    ]),
    (96, 5, b'Equihash is an asymmetric PoW based on the Generalised Birthday problem.', 11, [
  [637, 78032, 97478, 118268, 16058, 44395, 19029, 39150, 1566, 66582, 4084, 107252, 59619, 116281, 67957, 128728, 30916, 69051, 90422, 102716, 51905, 66753, 60509, 78066, 38568, 119630, 75839, 113134, 54356, 70996, 63085, 83048],
  [4130, 71826, 46248, 50447, 4281, 129092, 23122, 103196, 9305, 34797, 111094, 127775, 82662, 120386, 109738, 124765, 24770, 125174, 83477, 102473, 45209, 79062, 84764, 125929, 31689, 95554, 66614, 127658, 31756, 55684, 53670, 53776],
    ]),
    (96, 5, b'Test case with 3+-way collision in the final round.', 0x0000000000000000000000000000000000000000000000000000000000002af3, [
  [1093, 45982, 37399, 89200, 29813, 113936, 40951, 64027, 4370, 122807, 82736, 119086, 21530, 60168, 65163, 68120, 2310, 94346, 22675, 61162, 19193, 54507, 38352, 94322, 5341, 65047, 48071, 120787, 32561, 129305, 62593, 93497],
  [6411, 91796, 58827, 93129, 6705, 74430, 91891, 124391, 32765, 128544, 51395, 74269, 55980, 89012, 58573, 75543, 7902, 22572, 27944, 66370, 61755, 76417, 68687, 90417, 31576, 105479, 117582, 130960, 52751, 53260, 71636, 118134],
  [6411, 91796, 58827, 93129, 6705, 74430, 91891, 124391, 32765, 128544, 51395, 74269, 55980, 89012, 58573, 75543, 7902, 22572, 61755, 76417, 27944, 66370, 68687, 90417, 31576, 105479, 117582, 130960, 52751, 53260, 71636, 118134],
  [6411, 91796, 58827, 93129, 6705, 74430, 91891, 124391, 32765, 128544, 51395, 74269, 55980, 89012, 58573, 75543, 7902, 22572, 68687, 90417, 27944, 66370, 61755, 76417, 31576, 105479, 117582, 130960, 52751, 53260, 71636, 118134],
  [11541, 106147, 29075, 118360, 53060, 62499, 109856, 118745, 14581, 56663, 114595, 121986, 35542, 72577, 88428, 116033, 11996, 55170, 16966, 94150, 16116, 81559, 34889, 112430, 37304, 104803, 92442, 119354, 46613, 72741, 50259, 89047],
    ]),
]


class EquihashSolverTestCase(unittest.TestCase):
    def __init__(self, n, k, I, nonce, solns):
        super(EquihashSolverTestCase, self).__init__('testBasicSolver')
        self.n = n
        self.k = k
        self.I = I
        self.nonce = nonce
        self.solns = solns

    def shortDescription(self):
        return '%d,%d: "%s" | %d' % (self.n, self.k, self.I, self.nonce)

    def testBasicSolver(self):
        digest = blake2b(digest_size=(512/self.n)*self.n/8, person=zcash_person(self.n, self.k))
        digest.update(self.I)
        hash_nonce(digest, self.nonce)
        ret = gbp_basic(digest, self.n, self.k)
        self.assertEqual(sorted(ret), self.solns)

def test_vectors():
    suite = unittest.TestSuite()
    for tv in ZCASH_TEST_VECTORS:
        suite.addTest(EquihashSolverTestCase(*tv))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_vectors())
