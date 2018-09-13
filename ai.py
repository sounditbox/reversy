import random


class base_ai:
    def get_turn_number(self, board=None):
        return 0

    def make_turn(self, board):
        possible_turns = board.get_ordered_turn_list()
        if len(possible_turns) == 0:
            board.change_color()
        else:
            board.turn(possible_turns[self.get_turn_number(board)][0],
                       possible_turns[self.get_turn_number(board)][1])


class easy_level_ai(base_ai):
    def get_turn_number(self, board=None):
        return 0


class hard_level_ai(base_ai):
    def get_turn_number(self, board=None):
        return -1


class random_level_ai(base_ai):
    def get_turn_number(self, board=None):
        possible_turns = board.get_ordered_turn_list()
        return random.randint(0, len(possible_turns) - 1)
