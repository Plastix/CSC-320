import unittest
import pacman


class TestRectangularRoomCleaner(unittest.TestCase):
    layouts = [
        ['rectangularRoom-1'],
        ['rectangularRoom-2'],
        ['rectangularRoom-3'],
        ['rectangularRoom-4'],
        ['rectangularRoom-5'],
        ['rectangularRoom-6'],
        ['rectangularRoom-7']
    ]

    @staticmethod
    def generate_test(layout):
        def test(self):
            args = pacman.readCommand(['-p', 'RectangularRoomCleaner',
                                       '-l', layout,
                                       '-q',
                                       '--frameTime', '0',
                                       '--timeout', '1'])
            games = pacman.runGames(**args)
            self.assertTrue(games[0].state.isWin())

        return test

    @staticmethod
    def setup_tests():
        for test in TestRectangularRoomCleaner.layouts:
            test_name = 'test_%s' % test[0]
            func = TestRectangularRoomCleaner.generate_test(test[0])
            setattr(TestRectangularRoomCleaner, test_name, func)


TestRectangularRoomCleaner.setup_tests()
if __name__ == '__main__':
    unittest.main()
