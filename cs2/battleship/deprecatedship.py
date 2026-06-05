from fltk import *
import socket, sys
import numpy as np
def make_boards(row, col, size) :
    pt = np.array([Fl_Button]*AREA)
    et = np.array([Fl_Button]*AREA)
    ids = []
    offset = size*row + size//4
    i = 0
    for y in range(row) :
        for x in range(col) :
            pt[i] = Fl_Button(size*x, size*y + size, size, size)
            et[i] = Fl_Button(size*x + offset, size*y + size, size, size)
            ids.append((y, x))

            pt[i].box(FL_BORDER_BOX)
            et[i].box(FL_BORDER_BOX)
            pt[i].color(138)
            et[i].color(138)
            pt[i].callback(click, (i, 0))
            et[i].callback(click, (i, 1))

            i += 1

    d_pt = pt.reshape(row, col)
    d_et = et.reshape(row, col)
    return pt, d_pt, et, d_et, ids

def click(wid, data) :
    global direction, ship_size

    if Fl.event_button() == 3 :
        direction = 1 if direction == 0 else 0
        direction_display.label(direction_symbols[direction])
        return

    i, function = data
    if function == 0 and gamephase == "deploy" :
        deploy_ship(wid, i)
        if ship_size > 4 :
            gamephase = "battle"

    elif function == 1 and gamephase == "battle" :
        send_missile(wid, i)

def deploy_ship(wid, i, drc) :
    global ship_size
    rowcol = list(index[i])
    j = 1
    for x in range(ship_size) :
        rowcol[drc] += x
        if rowcol in index

def send_missile(wid, i) :
    print(indexes[i])

ROW = 10
COL = 10
SIZE = 48
AREA = ROW*COL
gamephase = "deploy"
ship_size = 1
ships = []
direction = 1
direction_symbols = (">", "^")

battleship = Fl_Window(SIZE*ROW*2 + SIZE//8, SIZE*COL + SIZE*2, "Nable Baddle")
battleship.begin()
battleship.color(47)

my_tiles, d_my_tiles, em_tiles, d_em_tiles, indexes = make_boards(ROW, COL, SIZE)

direction_display = Fl_Box(0, battleship.h() - SIZE, SIZE, SIZE, ">")
direction_display.box(FL_FLAT_BOX)
direction_display.labelsize(32)

size_display = Fl_Box(SIZE, battleship.h() - SIZE, SIZE, SIZE, "1")

battleship.end()
battleship.show()

Fl.visible_focus(0)
Fl.run()
