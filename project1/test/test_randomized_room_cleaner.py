import unittest
import pacman


class TestRandomizedRoomCleaner(unittest.TestCase):
    layouts = [
        'rectangularRoomWithObstacles-1',
        'rectangularRoom-1',
        'rectangularRoom-2',
    ]

    num_games = 5

    @staticmethod
    def generate_test(layout):
        def test(self):
            array_args = ['-p', 'RandomizedRoomCleaner',
                          '-l', layout,
                          '-q',
                          '-n', str(TestRandomizedRoomCleaner.num_games),
                          '--frameTime', '0',
                          '--timeout', '4']
            args = pacman.readCommand(array_args)
            games = pacman.runGames(**args)
            wins = [game.state.isWin() for game in games].count(True)
            scores = [game.state.getScore() for game in games]
            self.assertTrue(wins == TestRandomizedRoomCleaner.num_games, "Pacman did not win all games!")
            self.assertTrue(sum(scores) / float(len(scores)) > 0, "Average score not positive!")

        return test

    @staticmethod
    def setup_tests():
        for test in TestRandomizedRoomCleaner.layouts:
            test_name = 'test_%s' % test
            func = TestRandomizedRoomCleaner.generate_test(test)
            setattr(TestRandomizedRoomCleaner, test_name, func)


TestRandomizedRoomCleaner.setup_tests()
if __name__ == '__main__':
    unittest.main()
