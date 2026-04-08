from fltk import *
import numpy as np
import random
    
    
def mastermake() :
    global master,d_master,surroundingMines,d_surroundingMines,maxMines,row,col
    master = np.array([2]*(row*col))
    surroundingMines= np.array([0]*(row*col))
    mines = 0
    
    if maxMines<= row*col :
    
        while mines < maxMines:
            idx = random.randrange(row*col)
    
            if master[idx] != 1 :
                master[idx] = 1
                mines += 1
                
    else :
        fl_message("Too many mines")
        
    
    d_master = master.reshape(row,col)
    d_surroundingMines= surroundingMines.reshape(row,col)
    
    for ir in range(row) :
    
        for ic in range(col) :
    
            if d_master[ir,ic] != 1 :
    
                if radiusChecker(d_master,ir,ic) :
                    d_master[ir,ic] = 0

    makenums()

def makenums() :
    global row,col,surroundingMines,d_surroundingMines
    for l in range(surroundingMines.size) :
        surroundingMines[l] = 0

    for ir in range(row) :

        for ic in range(col) :

            if d_master[ir,ic] == 2 :

                d_surroundingMines[ir,ic] = radiusChecker(d_master,ir,ic,labeling=True)
    
def radiusChecker(lst,ir,ic,clear=False,labeling=False,replacing=False,first=False,numberClearing=False,flago=False) :
    global cleared,row,col,d_master
    fc = True
    c = 0
    il = []
    f = 0
    fl = []
    ml = []
    gl = []

    for rr in range(-1,2) :
    
        for cc in (range(-1,2)) :
    
            if row > ir + rr >= 0 <= ic + cc < col :

                if first :
                    il.append([ir+rr,ic+cc])

                elif replacing :
                    if rr == 0 == cc :
                        None
                    elif lst[ir+rr,ic+cc] != 1 :
                        lst[ir+rr,ic+cc] = 2
    
                elif clear and [ir+rr,ic+cc] not in cleared :
                    cleared.append([ir+rr,ic+cc])
    
                    if lst[ir+rr,ic+cc] == 0 :
    
                        clearall(ir+rr,ic+cc)

                elif not clear :
    
                    if lst[ir+rr,ic+cc] == 1 :
                        c += 1
                        fc = False
                    
                    if numberClearing:
                        if lst[ir+rr,ic+cc].label() == "F" :
                            f += 1

                    elif flago :
                        if lst[ir+rr,ic+cc].label() == "F" :
                            fl.append([ir+rr,ic+cc])
                        if d_master[ir+rr,ic+cc] == 1 :
                            ml.append([ir+rr,ic+cc])
                        elif d_master[ir+rr,ic+cc] != 9 :
                            gl.append([ir+rr,ic+cc])



    if not labeling and not clear and not replacing and not first and not numberClearing and not flago :
        return fc
    elif labeling :
        return c
    elif first :
        return il
    elif numberClearing :
        return f
    elif flago :
        return [fl,ml,gl]
    
def clearall(r=None,c=None,skip=False) :#,wid=None) :
    global master,d_master,row,col,cleared,tiles
    
    if row > r >= 0 <= c < col :
        if skip :
            radiusChecker(d_master,r,c,True)
        elif not skip and d_master[r,c] == 0 :
            radiusChecker(d_master,r,c,True)

    
def makeboard() :
    global tiles,d_tiles,row,col,surroundingMines,d_surroundingMines,boxes,d_boxes,size,areaClear,d_areaClear
    tiles = np.array([])
    boxes = np.array([])
    areaClear = np.array([])

    for y in range(row) :
    
        for x in range(col) :
            tiles = np.append(tiles,Fl_Button(size*x,size*y + 32,size,size))
            areaClear = np.append(areaClear,Fl_Button(size*x,size*y + 32,size,size))
            boxes = np.append(boxes,Fl_Box(size*x,size*y + 32,size,size))
            
            

    for but in range(tiles.size) :
        tiles[but].callback(sweep)
        boxes[but].hide()
        areaClear[but].box(FL_NO_BOX)
        areaClear[but].deactivate()
        areaClear[but].callback(sweep)
        
        if surroundingMines[but] != 0 :
            boxes[but].label(str(surroundingMines[but]))
            boxes[but].labelfont(FL_HELVETICA_BOLD)
            boxes[but].labelsize(size//2 + size//4)
            colornums(boxes,surroundingMines,but)
        
    d_tiles = tiles.reshape(row,col)
    d_boxes = boxes.reshape(row,col)
    d_areaClear = areaClear.reshape(row,col)
    
def surroundingMinesChecker() :
    global surroundingMines,d_surroundingMines,boxes
    for but in range(surroundingMines.size) :
        boxes[but].label(None)
        
        if surroundingMines[but] != 0 :
            boxes[but].label(str(surroundingMines[but]))
            boxes[but].labelfont(FL_HELVETICA_BOLD)
            boxes[but].labelsize(size//2 + size//4)
            colornums(boxes,surroundingMines,but)

def firstClick(center,max=False) :
    global row,col,master,d_master
    ir = center[0]
    ic = center[1]
    il = radiusChecker(d_master,ir,ic,first=True)
    rep = True

    if d_master[ir,ic] == 1 :
        while rep :
            ridx = random.randrange(row)
            cidx = random.randrange(col)
            if d_master[ridx,cidx] != 1 and [ridx,cidx] not in il :
                rep = False
                d_master[ridx,cidx] = 1
                radiusChecker(d_master,ridx,cidx,replacing=True)

    if not max :
        d_master[ir,ic] = 0

        for rr in range(-1,2) :
        
            for cc in (range(-1,2)) :
                rep = True

                if row > ir + rr >= 0 <= ic + cc < col :
                    
                    if d_master[ir+rr,ic+cc] == 1 :

                        if radiusChecker(d_master,ir+rr,ic+cc) :
                            d_master[ir+rr,ic+cc] = 0
                        else :
                            d_master[ir+rr,ic+cc] = 2

                        while rep :
                            ridx = random.randrange(row)
                            cidx = random.randrange(col)
                            if d_master[ridx,cidx] != 1 and [ridx,cidx] not in il :
                                rep = False
                                d_master[ridx,cidx] = 1
                                radiusChecker(d_master,ridx,cidx,replacing=True)

    else :
        d_master[ir,ic] = 2

def colornums(boxes,surroundingMines,but) :
    match surroundingMines[but] :
        case 1 :
            boxes[but].labelcolor(FL_BLUE)
        case 2 :
            boxes[but].labelcolor(61)
        case 3 :
            boxes[but].labelcolor(FL_RED)
        case 4 :
            boxes[but].labelcolor(136)
        case 5 :
            boxes[but].labelcolor(81)
        case 6 :
            boxes[but].labelcolor(140)
        case 7 :
            boxes[but].labelcolor(0)
        case 8 :
            boxes[but].labelcolor(42)

def sweep(wid) :
    global master,d_master,cleared,tiles,d_tiles,click,won,maxMines,num,d_surroundingMines,boxes,flagCount,areaClear,d_areaClear
    if wid in tiles :
        center = [np.where(d_tiles==wid)[0][0],np.where(d_tiles==wid)[1][0],np.where(tiles==wid)[0][0]]
    else :
        center = [np.where(d_areaClear==wid)[0][0],np.where(d_areaClear==wid)[1][0],np.where(areaClear==wid)[0][0]]
    
    match Fl.event_button() :
        case 1 :
            if wid.label() != "F" :
                if click == 0 and 2 in master :
                    Fl.add_timeout(1.0,timerclock)
                    if maxMines<= (row*col - 9) :
                        firstClick(center)
                    else :
                        firstClick(center,True)
                    for ir in range(row) :
    
                        for ic in range(col) :
                    
                            if d_master[ir,ic] != 1 :
                    
                                if radiusChecker(d_master,ir,ic) :
                                    d_master[ir,ic] = 0
                    makenums()
                    surroundingMinesChecker()
                    click = 1

                idx = center[2]
                r = center[0]
                c = center[1]

                if wid.label() == None :

                    if wid in tiles :

                        if master[idx] == 1 :
                            timerclock(True)
                            fl_message("The cow's booteh")
                            
                        elif master[idx] == 0 :
                            clearall(r,c)#,wid)

                        elif master[idx] == 2 :
                            master[idx] = 9
                            tiles[idx].color(45)
                            tiles[idx].deactivate()
                            boxes[idx].show()
                            if boxes[idx].label() != None :
                                areaClear[idx].activate()

                    elif wid in areaClear :
                        around = surroundingMines[idx]
                        
                        if around == radiusChecker(d_tiles,r,c,numberClearing=True) :
                            mighty = radiusChecker(d_tiles,r,c,flago=True)

                            if mighty[0] == mighty[1] :

                                if len(mighty) == 3 :

                                    for i in range(len(mighty[2])) :
                                        if d_master[mighty[2][i][0],mighty[2][i][1]] == 0 :
                                            center = [mighty[2][i][0],mighty[2][i][1]]

                                    if len(center) == 2 :
                                        clearall(center[0],center[1],True)#,wid)

                                    for i in range(len(mighty[2])) :

                                        if d_master[mighty[2][i][0],mighty[2][i][1]] != 9 :
                                            d_master[mighty[2][i][0],mighty[2][i][1]] = 9
                                            d_tiles[mighty[2][i][0],mighty[2][i][1]].color(45)
                                            d_tiles[mighty[2][i][0],mighty[2][i][1]].deactivate()
                                            d_boxes[mighty[2][i][0],mighty[2][i][1]].show()
                                            if d_boxes[mighty[2][i][0],mighty[2][i][1]].label() != None :
                                                d_areaClear[mighty[2][i][0],mighty[2][i][1]].activate()
                            else :
                                timerclock(True)
                                fl_message("The cow's botteh")

                    elif 2 not in master :
                        fl_message("Mines"*maxMines)

                    for i in range(len(cleared)) :
                        
                        if d_tiles[cleared[i][0],cleared[i][1]].label() == None :
                            d_master[cleared[i][0],cleared[i][1]] = 9
                            d_tiles[cleared[i][0],cleared[i][1]].color(45)
                            d_tiles[cleared[i][0],cleared[i][1]].deactivate()
                            d_boxes[cleared[i][0],cleared[i][1]].show()
                            if d_boxes[cleared[i][0],cleared[i][1]].label() != None :
                                d_areaClear[cleared[i][0],cleared[i][1]].activate()
                        
                    cleared = []

                    if 0 not in master and 2 not in master :
                        timerclock(True)
                        mrem.label(f"{maxMines} / {maxMines}")
                        fl_message("You da man")
                        won = True
        
        case 3 :
            if wid in tiles :
                if wid.label() == "F" :
                    flagCount -= 1
                    wid.label(None)
                else :
                    flagCount += 1
                    wid.label("F")
                    wid.labelcolor(168)
                    wid.labelfont(FL_HELVETICA_BOLD)
                    wid.labelsize(size//2 + size//4)
                mrem.label(f"{flagCount} / {maxMines}")

def timerclock(stop=False) :
    global timer,seconds
    if stop or seconds >= 999 :
        Fl.remove_timeout(timerclock)
        return
    seconds += 1
    if seconds > 99 :
        timer.label(f"{seconds}")
    elif seconds > 9 :
        timer.label(f"0{seconds}")
    else :
        timer.label(f"00{seconds}")
    Fl.repeat_timeout(1.0,timerclock)

def allGlobalVariables(sch=1) :
    global cleared,size,row,col,maxMines,mines,click,won,deadson,surroundingMines,gamemode,flagCount,seconds
    surroundingMines = np.array([])
    cleared = []
    match sch :
        case 1 :
            size = 64
            row = 9
            col = 9
            maxMines = 10
        case 2 :
            size = 40
            row = 16
            col = 16
            maxMines = 40
        case 3 :
            size = 40
            row = 16
            col = 30
            maxMines = 99
    gamemode = sch
    mines = []
    mastermake()
    click = 0
    flagCount = 0
    won = False
    seconds = 0

def reset() :
    global tiles,boxes,areaClear,timer
    for but in range(tiles.size) :
        Fl.delete_widget(tiles[but])
        Fl.delete_widget(boxes[but])
        Fl.delete_widget(areaClear[but])
    Fl.remove_timeout(timerclock)
    timer.label("000")

def game(wid,sch=1) :
    global size,maxMines,row,col,sweeper,gamemode
    if sch == 0 :
        sch = gamemode
    reset()
    allGlobalVariables(sch)
    sweeper.begin()
    sweeper.resize(0,0,size*col,size*row + 32)
    mode.resize(0,0,sweeper.w(),32)
    mrem.resize(sweeper.w(),0,(size*2)+size//2 + size//4,28)
    mrem.label(f"0 / {maxMines}")
    timer.label("000")
    makeboard()
    
    sweeper.end()

allGlobalVariables()

sweeper = Fl_Window(size*col,size*row + 32,"Minesweeper")
sweeper.begin()

mode = Fl_Menu_Bar(0,0,sweeper.w(),32)
mode.add("New",FL_CTRL | ord("r"),game,0)
mode.add("Difficulty/Beginner",0,game,1)
mode.add("Difficulty/Intermediate",0,game,2)
mode.add("Difficulty/Expert",0,game,3)

mrem = Fl_Box(sweeper.w(),0,(size*2)+size//2 + size//4,28)
mrem.label(f"0 / {maxMines}")
mrem.labelsize(32)
mrem.align(FL_ALIGN_LEFT)

timer = Fl_Box(size + size//8,0,(size*2)+size//2 + size//4,28)
timer.label("000")
timer.labelsize(32)
timer.align(FL_ALIGN_CENTER)

makeboard()

sweeper.end()
sweeper.show()

Fl.visible_focus(0)
Fl.run()
