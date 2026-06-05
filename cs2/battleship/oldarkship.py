from fltk import *
import socket, sys

def make_master(row, col, size) :
    pl = [0 for x in range(row*col)]
    el = [0 for x in range(row*col)]

def make_board(row, col, size) :
    pt = []
    et = []
    offset = size*col + size//4
    
    i = 0
    for y in range(row) :
        for x in range(col) :
            pt.append(Fl_Button(size*x, size*y, size, size))
            et.append(Fl_Button(size*x + offset, size*y, size, size))
            
            pt[i].callback(click, (i, 0))
            et[i].callback(click, (i, 1))
            pt[i].image(images["blank"])
            et[i].image(images["blank"])
            i += 1

    return pt, et

def click(wid, data) :
    global phase, placed
    i, use = data
    if use == 1 and phase == "deploy" :
        placed += 1
        deploy_ship(i, phase, placed)

def deploy_ship(i, placed) :
    global phase

    if placed >= 5 :
        phase = "ready"
        return

    if my_board[i] != 1 :
        my_board[i] = 1
        my_tiles[i].image(images["ship"])

ROW = 5
COL = 5
SIZE = 64
phase = "deploy"
placed = 0

images = { "blank" : Fl_PNG_Image("./blank.png").copy(SIZE, SIZE),
           "ship"  : Fl_PNG_Image("./ship.png").copy(SIZE, SIZE),
           "miss"  : Fl_PNG_Image("./miss.png").copy(SIZE, SIZE),
           "hit"   : Fl_PNG_Image("./hit.png").copy(SIZE, SIZE) }

battleship = Fl_Window(SIZE*COL*2 + SIZE//4, SIZE*ROW + SIZE//2, "Nabvle Baddttle")
battleship.begin()
battleship.color(20)

my_tiles, em_tiles = make_board(ROW, COL, SIZE)

battleship.end()
battleship.show()

Fl.visible_focus(0)
Fl.run()
