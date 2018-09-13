from ai import easy_level_ai, hard_level_ai, random_level_ai, base_ai
from gui import TextWindow, Field, ChoosingAIPanel, ControlPanel, ChoosingModePanel
from logic import Board_saver, Board_loader
from tkinter import Tk, TclError


def eve_mode():
    txt.write('Welcome to Reversi tournament!\n Mode: EvE')
    field.board.start()
    field.ai = random_level_ai
    while field.board.can_turn('black') and \
            field.board.can_turn('white') and field.board.turn_number >= 0:
        try:
            field.update(txt, summarize)
            root.update()
            root.after(500, field.ai.make_turn(base_ai,field.board))
        except TclError:
            return

    summarize(field.board.game_status())


def pvx_mode(message):
    if field.board.mode == 'pvp':
        if message == 'no turn':
            field.board.color = 'white' \
                if field.board.turn_number % 2 == 0 else 'black'
    else:
        field.update(txt, summarize)
        root.update()
        var = ch_ai.var.get()
        if var == 1:
            field.ai = easy_level_ai
        elif var == 2:
            field.ai = hard_level_ai

        elif var == 3:
            field.ai = random_level_ai
        else:
            field.ai = base_ai
        root.after(500, field.ai.make_turn(base_ai,field.board))


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
    if ch_ai != None:
        ch_ai.destroy()


def switch_mode(event):
    var = ch_pan.var.get()
    if var != 0:
        ch_pan.destroy()
        if var == 1:
            ch_ai.show()
            txt.text['text'] = 'Welcome to Otello tournament!\nChoose the AI level:'
            # con_pan.create_unturn_btn(unturn)
        elif var == 2:
            field.show()
            field.board.mode = 'pvp'
            field.activate(turn,callback)
            field.start(txt,summarize)
            con_pan.show()
        else:
            field.show()
            field.board.mode = 'eve'
            con_pan.restart_btn['text'] = 'Restart'
            con_pan.show()
            #con_pan.exit_btn.destroy()
            eve_mode()


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
    field.board.color = 'black'
    field.start(txt, summarize)
    if field.board.mode == 'eve':
        eve_mode()
    field.activate(turn, callback)


def exit(event):
    root.destroy()


def unturn(event):
    field.board.unturn()
    field.ai.make_turn(field.board)
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
    root = Tk()
    root.resizable(width=False, height=False)
    txt = TextWindow(root)
    txt.show()
    field = Field(root)
    ch_ai = ChoosingAIPanel(root, show_field_and_control_panel)
    con_pan = ControlPanel(root, load, exit)

    con_pan.create_save_btn(save)
    con_pan.create_load_btn(load)
    con_pan.create_restart_btn(start)
    ch_pan = ChoosingModePanel(root, switch_mode)
    ch_pan.show()
    root.mainloop()