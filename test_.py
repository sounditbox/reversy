import unittest
from logic import *


class Test(unittest.TestCase):
    def assertBoardsEqual(self, board, string_vision):
        string_vision = string_vision.replace(' ', '')
        string_vision = string_vision.replace('\n', '')

        for x in range(8):
            for y in range(8):
                board_color = board[x][y].cond
                string_color = string_vision[0]
                if string_color == 'w':
                    string_color = 'white'
                elif string_color == 'b':
                    string_color = 'black'
                elif string_color == '.':
                    string_color = 'empty'
                string_vision = string_vision[1:]
                self.assertEqual(board_color, string_color)

    def test_cell(self):
        c = Cell(0, 0, 'empty')
        self.assertEqual(c.x, 0)
        self.assertEqual(c.y, 0)
        self.assertEqual(c.cond, 'empty')

    def test_empty_board(self):
        b = Board()
        for i in range(7):
            for j in range(7):
                self.assertEqual(b.board[i][j].cond, 'empty')
        self.assertEqual(b.color, 'black')
        self.assertEqual(b.turn_number, 0)
        self.assertEqual(b.mode, 'pve')

    def test_start_board(self):
        expected = """
                    ........
                    ........
                    ........
                    ...bw...
                    ...wb...
                    ........
                    ........
                    ........
                    """
        b = Board()
        b.start()
        self.assertBoardsEqual(b.board,expected)
        start_turns = b.possible_turns('white')
        self.assertEqual(len(start_turns), 4)

    def test_start_can_turn(self):
        b = Board()
        b.start()
        self.assertTrue(b.can_turn('white'))
        self.assertTrue(b.can_turn('black'))

    def test_can_turn_on_coord(self):
        b = Board()
        b.start()
        self.assertTrue(b.can_turn(b.color, 3, 5))
        self.assertTrue(b.can_turn(b.color, 4, 2))
        self.assertTrue(b.can_turn(b.color, 2, 4))
        self.assertTrue(b.can_turn(b.color, 5, 3))
        self.assertFalse(b.can_turn(b.color, 7, 7))
        self.assertFalse(b.can_turn(b.color, 1, 1))


    def test_empty_game_status(self):
        b = Board()
        self.assertEqual(b.game_status(), (0, 0))

    def test_start_game_status(self):
        b = Board()
        b.start()
        self.assertEqual(b.game_status(), (2, 2))

    def test_first_line(self):
        b = Board()
        b.start()
        b.turn(3, 5)
        expected = '''
                    ........
                    ........
                    ........
                    ...bbb..
                    ...wb...
                    ........
                    ........
                    ........
                    '''
        self.assertBoardsEqual(b.board,expected)

    def test_blacks_win(self):
        b = Board()
        b.start()
        b.turn(3, 5)
        b.color = 'black'
        b.turn(5, 2)
        whites_count = b.game_status()[1]
        self.assertEqual(whites_count, 0)
        expected = '''
                    ........
                    ........
                    ........
                    ...bbb..
                    ...bb...
                    ..b.....
                    ........
                    ........
                    '''
        self.assertBoardsEqual(b.board,expected)


    def test_whites_win(self):
        b = Board()
        b.start()
        b.color = 'white'
        b.turn(3, 2)
        b.color = 'white'
        b.turn(4, 5)
        blacks_count = b.game_status()[0]
        self.assertEqual(blacks_count, 0)

    def test_domain(self):
        self.assertTrue(in_domain(2, 5))
        self.assertTrue(in_domain(7, 7))
        self.assertFalse(in_domain(8, 8))
        self.assertFalse(in_domain(-5, 3))

    def test_clearing(self):
        b = Board()
        b.start()
        b.clear()
        test_board = b.to_wb_vision()
        for x in range(8):
            for y in range(8):
                self.assertEqual(test_board[x][y], '.')


if __name__ == "__main__":
    unittest.main()
