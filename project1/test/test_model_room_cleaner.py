import unittest
import pacman


class TestModelRoomCleaner(unittest.TestCase):
    layouts = [
        'rectangularRoom-1',
        'rectangularRoom-2',
        'rectangularRoom-3',
        'rectangularRoomWithObstacles-1',
        'mediumSearch',
        'mediumSafeSearch',
    ]

    @staticmethod
    def generate_test(layout):
        def test(self):
            args = pacman.readCommand(['-p', 'ModelBasedRoomCleaner',
                                       '-l', layout,
                                       '-q',
                                       '--frameTime', '0',
                                       '--timeout', '1'])
            games = pacman.runGames(**args)
            self.assertTrue(games[0].state.isWin())

        return test

    @staticmethod
    def setup_tests():
        for test in TestModelRoomCleaner.layouts:
            test_name = 'test_%s' % test
            func = TestModelRoomCleaner.generate_test(test)
            setattr(TestModelRoomCleaner, test_name, func)


TestModelRoomCleaner.setup_tests()
if __name__ == '__main__':
    unittest.main()
