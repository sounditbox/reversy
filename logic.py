import copy
import pickle


class Cell:
    def __init__(self, x, y, condition='empty'):
        self.cond = condition
        self.x = x
        self.y = y


class Board:
    def __init__(self):
        self.board = [[None] * 8 for i in range(8)]
        for i in range(8):
            for j in range(8):
                self.board[i][j] = Cell(i, j)
        self.color = 'black'
        self.turn_number = 0
        self.mode = 'pve'
        self.previous_state = [[None] * 8 for i in range(8)]
        self.preprevious_state = [[None] * 8 for i in range(8)]
        self.prepreprevious_state = [[None] * 8 for i in range(8)]

    def get_ordered_turn_list(board):
        res = []
        for x in range(8):
            for y in range(8):
                if board.can_turn(board.color, x, y):
                    prev = board.current_color_count()
                    board.turn(x, y)
                    curr = board.current_color_count()
                    count = curr - prev
                    board.unturn()
                    res.append(((x, y), count))
        res.sort(key=lambda x: x[1])
        return list(map(lambda x: x[0], res))

    def start(self):
        self.color = 'black'
        self.board[3][3].cond = 'black'
        self.board[3][4].cond = 'white'
        self.board[4][3].cond = 'white'
        self.board[4][4].cond = 'black'
        self.previous_state = [[None] * 8 for i in range(8)]
        self.preprevious_state = [[None] * 8 for i in range(8)]
        self.prepreprevious_state = [[None] * 8 for i in range(8)]

    def clear(self):
        for column in self.board:
            for cell in column:
                cell.cond = 'empty'

    def change_color(self):
        self.color = 'white' if self.color == 'black' else 'black'
        self.turn_number += 1

    def enemy_neighbors(self, cell):
        enemy_color = 'black' if cell.cond == 'white' else 'white'
        res = []
        neighborhood = self.neighbors(cell)
        for cell in neighborhood:
            if cell.cond == enemy_color:
                res.append(cell)
        return res

    def neighbors(self, cell):
        neighborhood = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if in_domain(cell.x + i, cell.y + j) and (i != 0 or j != 0):
                    neighborhood.append(self.board[cell.x + i][cell.y + j])
        return neighborhood

    def line(self, start_cell, dx, dy):
        current_cell = self.board[start_cell.x][start_cell.y]
        line_color = current_cell.cond
        line = [current_cell]
        while in_domain(current_cell.x + dx, current_cell.y + dy):
            current_cell = self.board[current_cell.x + dx][current_cell.y + dy]
            if current_cell.cond == line_color:
                line.append(current_cell)
            elif current_cell.cond == 'empty':
                line.append(current_cell)
                line.reverse()
                return line
            else:
                break
        return None

    def possible_turns(self, color):
        allied_cells = []
        for column in self.board:
            for cell in column:
                if cell.cond == None:
                    return
                if cell.cond == color:
                    allied_cells.append(cell)

        turns = []
        for cell in allied_cells:
            for enemy_cell in self.enemy_neighbors(cell):
                dx, dy = enemy_cell.x - cell.x, enemy_cell.y - cell.y
                new_line = self.line(enemy_cell, dx, dy)
                if new_line is not None:
                    turns.append(new_line)
        return turns

    def turn(self, x, y):
        self.prepreprevious_state = copy.deepcopy(self.preprevious_state)
        self.preprevious_state = copy.deepcopy(self.previous_state)
        self.previous_state = copy.deepcopy(self.board)
        self.turn_states(x, y, self.color)
        self.color = 'white' if self.turn_number % 2 == 0 else 'black'
        self.turn_number += 1

    def unturn(self):
        if self.turn_number > 0:
            self.board = copy.deepcopy(self.previous_state)
            self.previous_state = copy.deepcopy(self.preprevious_state)
            self.preprevious_state = copy.deepcopy(self.prepreprevious_state)
            self.prepreprevious_state = [[None] * 8 for i in range(8)]
            self.turn_number -= 1
            self.color = 'white' if self.turn_number % 2 == 1 else 'black'

    def turn_states(self, x, y, color):  # упростить color, если возможно
        lines = self.possible_turns(color)
        for line in lines:
            if (x, y) == (line[0].x, line[0].y):
                for cell in line:
                    self.board[cell.x][cell.y].cond = color

    def can_turn(self, color, *coords):
        lines = self.possible_turns(color)
        if len(coords) == 0:
            return len(lines) != 0
        else:
            for line in lines:
                if coords == (line[0].x, line[0].y):
                    return True
            return False

    def game_status(self):
        black = 0
        white = 0
        for column in self.board:
            for cell in column:
                if cell.cond == 'white':
                    white += 1
                elif cell.cond == 'black':
                    black += 1
        return black, white

    def current_color_count(self):
        count = 0
        for column in self.board:
            for cell in column:
                if cell.cond == self.color:
                    count += 1
        return count

    def to_wb_vision(self):
        res = [[None] * 8 for i in range(8)]
        for x in range(8):
            for y in range(8):
                curr = self.board[x][y].cond
                if curr == 'black':
                    curr = 'b'
                elif curr == 'white':
                    curr = 'w'
                else:
                    curr = '.'
                res[x][y] = curr
        return res


class Board_loader:
    @staticmethod
    def load_pvp():
        with open('pvp.pickle', 'rb') as f:
            board = pickle.load(f)
            return board
    @staticmethod
    def load_pve():
        with open('pve.pickle', 'rb') as f:
            board = pickle.load(f)
            return board
    @staticmethod
    def load_eve():
        with open('eve.pickle', 'rb') as f:
            board = pickle.load(f)
            return board


class Board_saver:

    @staticmethod
    def save_pvp(board):
        with open('pvp.pickle', 'wb') as f:
            pickle.dump(board, f)

    @staticmethod
    def save_pve(board):
        with open('pve.pickle', 'wb') as f:
            pickle.dump(board, f)

    @staticmethod
    def save_eve(board):
        with open('eve.pickle', 'wb') as f:
            pickle.dump(board, f)


def in_domain(x, y):
    return 0 <= x < 8 and 0 <= y < 8
