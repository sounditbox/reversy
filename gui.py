import time
import functools
from tkinter import Frame, Button, Canvas, IntVar, Radiobutton, Label, TclError

from logic import Board


class ChoosingModePanel:
    def __init__(self, root, switch_mode):
        self.choosing_frame = Frame \
            (root, height=60, width=100, bg='lightblue')
        self.var = IntVar()
        rbutton1 = Radiobutton(self.choosing_frame,
                               text='PvE', variable=self.var, value=1, bg='lightblue')
        rbutton2 = Radiobutton(self.choosing_frame,
                               text='PvP', variable=self.var, value=2, bg='lightblue')
        rbutton3 = Radiobutton(self.choosing_frame,
                               text='EvE', variable=self.var, value=3, bg='lightblue')
        button = Button(self.choosing_frame, text='Ok', bg='lightblue')
        rbutton1.select()
        rbutton1.pack(side='left')
        rbutton2.pack(side='left')
        rbutton3.pack(side='left')
        button.pack(side='left')
        button.bind('<1>', switch_mode)

    def show(self):
        self.choosing_frame.grid()

    def destroy(self):
        self.choosing_frame.destroy()


class ChoosingAIPanel:
    def __init__(self, root, func):
        self.choosing_frame = Frame \
            (root, height=60, width=100, bg='lightblue')
        self.var = IntVar()
        rbutton1 = Radiobutton(self.choosing_frame,
                               text='Easy', variable=self.var, value=1, bg='lightblue')
        rbutton2 = Radiobutton(self.choosing_frame,
                               text='Hard', variable=self.var, value=2, bg='lightblue')
        rbutton3 = Radiobutton(self.choosing_frame,
                               text='Random', variable=self.var, value=3, bg='lightblue')
        button1 = Button(self.choosing_frame, text='Ok', bg='lightblue')
        rbutton1.select()
        rbutton1.pack(side='left')
        rbutton2.pack(side='left')
        rbutton3.pack(side='left')
        button1.pack(side='left')

        button1.bind('<1>', lambda e: func())

    def show(self):
        self.choosing_frame.grid()

    def destroy(self):
        self.choosing_frame.destroy()


class ControlPanel:
    def __init__(self, root, load, exit):
        self.panel_frame = Frame(root, height=60, width=100)

    def create_exit_btn(self, exit):
        self.exit_btn = Button \
            (self.panel_frame, text='Exit', bg='lightblue')
        self.exit_btn.pack(side='right')
        self.exit_btn.bind("<1>", exit)

    def create_restart_btn(self, start):
        # start('start')
        self.restart_btn = Button \
            (self.panel_frame, text='Restart', bg='lightblue')
        self.restart_btn.pack(side='right')
        self.restart_btn.bind("<1>", start)

    def create_load_btn(self, load):
        self.load_btn = Button \
            (self.panel_frame, text='Load', bg='lightblue')
        self.load_btn.pack(side='right')
        self.load_btn.bind("<1>", load)

    def create_save_btn(self, save):
        self.save_btn = Button \
            (self.panel_frame, text='Save', bg='lightblue')
        self.save_btn.pack(side='left')
        self.save_btn.bind("<1>", save)

    def create_unturn_btn(self, unturn):
        self.unturn_btn = Button \
            (self.panel_frame, text='Turn somewhere else', bg='lightblue')
        self.unturn_btn.pack(side='right')
        self.unturn_btn.bind("<1>", unturn)

    def show(self):
        try:
            self.panel_frame.grid()
        except TclError:
            return

    def destroy(self):
        self.panel_frame.destroy()


class TextWindow:
    def __init__(self, root):
        self.text = Label(root, height=3, width=56,
                          text='Welcome to Otello tournament!'
                               '\nChoose the mode:', bg='lightblue')
        self.state = 0

    def show(self):
        self.text.grid()

    def write(self, message):
        if self.state is (2 or 3):
            time.sleep(0.5)
        self.text['text'] = message
        self.state = 1

    def destroy(self):
        self.text.destroy()

    def wrong_cell(self):
        self.write('You can\'t turn this way! Try another cells')
        self.state = 2

    def no_turns(self):
        self.write('You have no turns')
        self.state = 3

    def status(self, status):
        self.write('Blacks: ' + str(status[0]) +
                   '      Whites: ' + str(status[1]))
        self.state = 4


class Field:
    def __init__(self, root):
        self.field = Canvas(root, width=400, height=400)
        self.board = Board()
        self.create_field()
        self.current_coordinates = (-1, -1)
        self.ai = None

    def show(self):
        try:
            self.field.grid()
        except TclError:
            return

    def activate(self, turn, callback):
        for x in range(8):
            for y in range(8):
                self.field.tag_bind('f' + str(x) + str(y), '<1>', turn)
        self.field.bind('<Motion>', functools.partial(callback, param=self))

    def destroy(self):
        self.field.destroy()

    def clear(self):
        self.board.clear()
        self.field.delete('all')
        self.create_field()

    def create_field(self):
        for x in range(8):
            for y in range(8):
                self.field.create_rectangle(x * 50, y * 50, (x + 1) * 50,
                (y + 1) * 50, tag='f' + str(x) + str(y), fill="lightblue")

    def start(self, txt, summarize):
        self.board.start()
        self.update(txt, summarize)

    def update(self, txt, summarize):
        self.field.delete('all')
        self.create_field()
        for i in range(8):
            for j in range(8):
                cell = self.board.board[i][j]
                if cell.cond != 'empty':
                    self.paint_pawn(cell.x, cell.y, cell.cond)
        status = self.board.game_status()
        txt.status(status)

    def paint_pawn(self, x, y, color):
        self.field.create_oval\
            (x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill=color)
