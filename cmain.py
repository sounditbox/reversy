#!/usr/bin/python
from tkinter import Tk, TclError
import gui
import argparse

from ai import random_level_ai, hard_level_ai, easy_level_ai
from logic import Board_saver, Board_loader


def eve_mode():
    txt.write('Welcome to Reversi tournament!\n Mode: EvE')
    field.start(txt, summarize)
    field.show()
    con_pan.show()
    field.update(txt, summarize)

    while field.board.can_turn('black') and \
            field.board.can_turn('white') and field.board.turn_number >= 0:
        try:
            field.update(txt, summarize)
        except TclError:
            return
        root.update()
        root.after(500, _ai.make_turn(field.board))

    summarize(field.board.game_status())


def pvx_mode(message):
    if field.board.mode == 'pvp':
        if message == 'no turn':
            field.board.color = 'white' \
                if field.board.turn_number % 2 == 0 else 'black'
    else:
        field.update(txt, summarize)
        root.update()
        root.after(500, _ai.make_turn(field.board))


def callback(event, param):
    x, y = int(repr(getattr(event, 'x'))) // 50, \
           int(repr(getattr(event, 'y'))) // 50
    if field.current_coordinates != (x, y) and \
            field.board.can_turn(field.board.color, x, y):
        field.current_coordinates = (x, y)
        field.board.turn(x, y)
        status = field.board.game_status()
        txt.text['text'] = 'If you\'ll turn on {} {} then:' \
                           '\n Player 1(Blacks): {}      ' \
                           'Possible Player 2(Whites): {}'.format(x, y, status[0], status[1])
        field.board.unturn()


def show_field_and_control_panel():
    field.show()
    con_pan.show()
    start('start')
    txt.text['text'] = ''


def save(event):
    if field.board.mode == 'pvp':
        Board_saver.save_pvp(field.board)
    elif field.board.mode == 'pve':
        Board_saver.save_pve(field.board)
    else:
        Board_saver.save_eve(field.board)


def load(event):
    if field.board.mode == 'pvp':
        field.board = Board_loader.load_pvp()
    elif field.board.mode == 'pve':
        field.board = Board_loader.load_pve()
    else:
        field.board = Board_loader.load_eve()
    field.update(txt, summarize)



def start(event):
    field.clear()
    field.start(txt, summarize)
    field.activate(turn, callback)
    if field.board.mode == 'eve':
        eve_mode()


def exit(event):
    root.destroy()


def unturn(event):
    field.board.unturn()
    _ai.make_turn(field.board)
    field.update(txt, summarize)


def summarize(status):
    if status[0] > status[1]:
        txt.write('Game over.\nPlayer 1 win!')
    elif status[0] == status[1]:
        txt.write('Game over.\nDraw!')
    else:
        txt.write('Game over.\nPlayer 2 win!')
    txt.text['text'] += '\nPlayer 1(Blacks): {}  Player 2(Whites): {}'.format(*status)


def turn(event):
    x, y = int(repr(getattr(event, 'x'))) // 50, \
           int(repr(getattr(event, 'y'))) // 50
    color = field.board.color
    if field.board.can_turn(color, x, y):
        field.board.turn(x, y)
        root.update()
        pvx_mode('next turn')
    elif field.board.can_turn(color):
        txt.wrong_cell()
        txt.text.update()
    else:
        txt.no_turns()
        txt.text.update()
        pvx_mode('no turn')
    txt.text.update()
    if not field.board.can_turn('black') \
            and not field.board.can_turn('white'):
        summarize(field.board.game_status())
    field.update(txt, summarize)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', default='pve', choices=['pve', 'pvp', 'eve'], required=True)
    parser.add_argument('-l', '--level', default='easy', choices=['easy', 'hard', 'random'])
    args = parser.parse_args()
    root = Tk()
    root.resizable(width=False, height=False)
    txt = gui.TextWindow(root)
    txt.write('Welcome to Otello tournament!')
    txt.show()
    field = gui.Field(root)
    field.board.mode = args.mode
    con_pan = gui.ControlPanel(root, load, exit)
    _ai = None

    if args.level is not None:
        if args.level == 'easy':
            _ai = easy_level_ai()
        elif args.level == 'hard':
            _ai = hard_level_ai()
        else:
            _ai = random_level_ai()

    con_pan.create_save_btn(save)
    con_pan.create_load_btn(load)
    con_pan.create_restart_btn(start)
    start('start')
    field.show()
    con_pan.show()
    root.mainloop()
