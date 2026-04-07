from fltk import *
import numpy as np
import random
    
    
def mastermake() :
    global master,dmaster,nums,dnums,maxmines,row,col
    master = np.array([2]*(row*col))
    nums = np.array([0]*(row*col))
    mines = 0
    
    if maxmines <= row*col :
    
        while mines < maxmines :
            idx = random.randrange(row*col)
    
            if master[idx] != 1 :
                master[idx] = 1
                mines += 1
                
    else :
        fl_message("Too many mines")
        
    
    dmaster = master.reshape(row,col)
    dnums = nums.reshape(row,col)
    
    for ir in range(row) :
    
        for ic in range(col) :
    
            if dmaster[ir,ic] != 1 :
    
                if radius(dmaster,ir,ic) :
                    dmaster[ir,ic] = 0

    makenums()

def makenums() :
    global row,col,nums,dnums
    for l in range(nums.size) :
        nums[l] = 0

    for ir in range(row) :

        for ic in range(col) :

            if dmaster[ir,ic] == 2 :

                dnums[ir,ic] = radius(dmaster,ir,ic,labeling=True)
    
def radius(lst,ir,ic,clear=False,labeling=False,replacing=False,first=False,numclear=False,flago=False) :
    global clrd,row,col,dmaster
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
    
                elif clear and [ir+rr,ic+cc] not in clrd :
                    clrd.append([ir+rr,ic+cc])
    
                    if lst[ir+rr,ic+cc] == 0 :
    
                        clearall(ir+rr,ic+cc)

                elif not clear :
    
                    if lst[ir+rr,ic+cc] == 1 :
                        c += 1
                        fc = False
                    
                    if numclear :
                        if lst[ir+rr,ic+cc].label() == "F" :
                            f += 1

                    elif flago :
                        if lst[ir+rr,ic+cc].label() == "F" :
                            fl.append([ir+rr,ic+cc])
                        if dmaster[ir+rr,ic+cc] == 1 :
                            ml.append([ir+rr,ic+cc])
                        elif dmaster[ir+rr,ic+cc] != 9 :
                            gl.append([ir+rr,ic+cc])



    if not labeling and not clear and not replacing and not first and not numclear and not flago :
        return fc
    elif labeling :
        return c
    elif first :
        return il
    elif numclear :
        return f
    elif flago :
        return [fl,ml,gl]
    
def clearall(r=None,c=None,skip=False) :#,wid=None) :
    global master,dmaster,row,col,clrd,tiles
    
    if row > r >= 0 <= c < col :
        if skip :
            radius(dmaster,r,c,True)
        elif not skip and dmaster[r,c] == 0 :
            radius(dmaster,r,c,True)

    
def makeboard() :
    global tiles,dtiles,row,col,nums,dnums,boxes,dboxes,size,numcl,dnumcl
    tiles = np.array([])
    boxes = np.array([])
    numcl = np.array([])

    for y in range(row) :
    
        for x in range(col) :
            tiles = np.append(tiles,Fl_Button(size*x,size*y + 32,size,size))
            numcl = np.append(numcl,Fl_Button(size*x,size*y + 32,size,size))
            boxes = np.append(boxes,Fl_Box(size*x,size*y + 32,size,size))
            
            

    for but in range(tiles.size) :
        tiles[but].callback(sweep)
        boxes[but].hide()
        numcl[but].box(FL_NO_BOX)
        numcl[but].deactivate()
        numcl[but].callback(sweep)
        
        if nums[but] != 0 :
            boxes[but].label(str(nums[but]))
            boxes[but].labelfont(FL_HELVETICA_BOLD)
            boxes[but].labelsize(size//2 + size//4)
            colornums(boxes,nums,but)
        
    dtiles = tiles.reshape(row,col)
    dboxes = boxes.reshape(row,col)
    dnumcl = numcl.reshape(row,col)
    
def surmines() :
    global nums,dnums,boxes
    for but in range(nums.size) :
        boxes[but].label(None)
        
        if nums[but] != 0 :
            boxes[but].label(str(nums[but]))
            boxes[but].labelfont(FL_HELVETICA_BOLD)
            boxes[but].labelsize(size//2 + size//4)
            colornums(boxes,nums,but)

def firstclick(center,max=False) :
    global row,col,master,dmaster
    ir = center[0]
    ic = center[1]
    il = radius(dmaster,ir,ic,first=True)
    rep = True

    if dmaster[ir,ic] == 1 :
        while rep :
            ridx = random.randrange(row)
            cidx = random.randrange(col)
            if dmaster[ridx,cidx] != 1 and [ridx,cidx] not in il :
                rep = False
                dmaster[ridx,cidx] = 1
                radius(dmaster,ridx,cidx,replacing=True)

    if not max :
        dmaster[ir,ic] = 0

        for rr in range(-1,2) :
        
            for cc in (range(-1,2)) :
                rep = True

                if row > ir + rr >= 0 <= ic + cc < col :
                    
                    if dmaster[ir+rr,ic+cc] == 1 :

                        if radius(dmaster,ir+rr,ic+cc) :
                            dmaster[ir+rr,ic+cc] = 0
                        else :
                            dmaster[ir+rr,ic+cc] = 2

                        while rep :
                            ridx = random.randrange(row)
                            cidx = random.randrange(col)
                            if dmaster[ridx,cidx] != 1 and [ridx,cidx] not in il :
                                rep = False
                                dmaster[ridx,cidx] = 1
                                radius(dmaster,ridx,cidx,replacing=True)

    else :
        dmaster[ir,ic] = 2

def colornums(boxes,nums,but) :
    match nums[but] :
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
    global master,dmaster,clrd,tiles,dtiles,click,won,maxmines,num,dnums,boxes,amt,numcl,dnumcl
    if wid in tiles :
        center = [np.where(dtiles==wid)[0][0],np.where(dtiles==wid)[1][0],np.where(tiles==wid)[0][0]]
    else :
        center = [np.where(dnumcl==wid)[0][0],np.where(dnumcl==wid)[1][0],np.where(numcl==wid)[0][0]]
    
    match Fl.event_button() :
        case 1 :
            if wid.label() != "F" :
                if click == 0 and 2 in master :
                    Fl.add_timeout(1.0,timerclock)
                    if maxmines <= (row*col - 9) :
                        firstclick(center)
                    else :
                        firstclick(center,True)
                    for ir in range(row) :
    
                        for ic in range(col) :
                    
                            if dmaster[ir,ic] != 1 :
                    
                                if radius(dmaster,ir,ic) :
                                    dmaster[ir,ic] = 0
                    makenums()
                    surmines()
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
                                numcl[idx].activate()

                    elif wid in numcl :
                        around = nums[idx]
                        
                        if around == radius(dtiles,r,c,numclear=True) :
                            mighty = radius(dtiles,r,c,flago=True)

                            if mighty[0] == mighty[1] :

                                if len(mighty) == 3 :

                                    for i in range(len(mighty[2])) :
                                        if dmaster[mighty[2][i][0],mighty[2][i][1]] == 0 :
                                            center = [mighty[2][i][0],mighty[2][i][1]]

                                    if len(center) == 2 :
                                        clearall(center[0],center[1],True)#,wid)

                                    for i in range(len(mighty[2])) :

                                        if dmaster[mighty[2][i][0],mighty[2][i][1]] != 9 :
                                            dmaster[mighty[2][i][0],mighty[2][i][1]] = 9
                                            dtiles[mighty[2][i][0],mighty[2][i][1]].color(45)
                                            dtiles[mighty[2][i][0],mighty[2][i][1]].deactivate()
                                            dboxes[mighty[2][i][0],mighty[2][i][1]].show()
                                            if dboxes[mighty[2][i][0],mighty[2][i][1]].label() != None :
                                                dnumcl[mighty[2][i][0],mighty[2][i][1]].activate()
                            else :
                                timerclock(True)
                                fl_message("The cow's botteh")

                    elif 2 not in master :
                        fl_message("Mines"*maxmines)

                    for i in range(len(clrd)) :
                        
                        if dtiles[clrd[i][0],clrd[i][1]].label() == None :
                            dmaster[clrd[i][0],clrd[i][1]] = 9
                            dtiles[clrd[i][0],clrd[i][1]].color(45)
                            dtiles[clrd[i][0],clrd[i][1]].deactivate()
                            dboxes[clrd[i][0],clrd[i][1]].show()
                            if dboxes[clrd[i][0],clrd[i][1]].label() != None :
                                dnumcl[clrd[i][0],clrd[i][1]].activate()
                        
                    clrd = []

                    if 0 not in master and 2 not in master :
                        timerclock(True)
                        mrem.label(f"{maxmines} / {maxmines}")
                        fl_message("You da man")
                        won = True
        
        case 3 :
            if wid in tiles :
                if wid.label() == "F" :
                    amt -= 1
                    wid.label(None)
                else :
                    amt += 1
                    wid.label("F")
                    wid.labelcolor(168)
                    wid.labelfont(FL_HELVETICA_BOLD)
                    wid.labelsize(size//2 + size//4)
                mrem.label(f"{amt} / {maxmines}")

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

def vari(sch=1) :
    global clrd,size,row,col,maxmines,mines,click,won,deadson,nums,gamemode,amt,seconds
    nums = np.array([])
    clrd = []
    match sch :
        case 1 :
            size = 64
            row = 9
            col = 9
            maxmines = 10
        case 2 :
            size = 40
            row = 16
            col = 16
            maxmines = 40
        case 3 :
            size = 40
            row = 16
            col = 30
            maxmines = 99
    gamemode = sch
    mines = []
    mastermake()
    click = 0
    amt = 0
    won = False
    seconds = 0

def reset() :
    global tiles,boxes,numcl,timer
    for but in range(tiles.size) :
        Fl.delete_widget(tiles[but])
        Fl.delete_widget(boxes[but])
        Fl.delete_widget(numcl[but])
    Fl.remove_timeout(timerclock)
    timer.label("000")

def game(wid,sch=1) :
    global size,maxmines,row,col,sweeper,gamemode
    if sch == 0 :
        sch = gamemode
    reset()
    vari(sch)
    sweeper.begin()
    sweeper.resize(0,0,size*col,size*row + 32)
    mode.resize(0,0,sweeper.w(),32)
    mrem.resize(sweeper.w(),0,(size*2)+size//2 + size//4,30)
    mrem.label(f"0 / {maxmines}")
    timer.label("000")
    makeboard()
    
    sweeper.end()

vari()

sweeper = Fl_Window(size*col,size*row + 32,"Minesweeper")
sweeper.begin()

mode = Fl_Menu_Bar(0,0,sweeper.w(),32)
mode.add("New",FL_CTRL | ord("r"),game,0)
mode.add("Difficulty/Beginner",0,game,1)
mode.add("Difficulty/Intermediate",0,game,2)
mode.add("Difficulty/Expert",0,game,3)

mrem = Fl_Box(sweeper.w(),0,(size*2)+size//2 + size//4,30)
mrem.label(f"0 / {maxmines}")
mrem.labelsize(32)
mrem.align(FL_ALIGN_LEFT)

timer = Fl_Box(size + size//8,0,(size*2)+size//2 + size//4,30)
timer.label("000")
timer.labelsize(32)
timer.align(FL_ALIGN_CENTER)

makeboard()

sweeper.end()
sweeper.show()

Fl.visible_focus(0)
Fl.run()
