from fltk import *
import random
import numpy as np

class Game(Fl_Window) :
    # enemyname : (moves, direction, updates, type, size)
    enemies = {
        "shooter" : ("g", 0, (-1, -2, 1, 2), 2, (1.1)),
        "bomber" : ("g", 1, (-1, 1), 4, (1, 1)),
        "cannon" : ("g", 0, (-1, -2, 1, 2), 4, (2, 2)),
        "bullet" : ("b", 1, (-1, -2, 1, 2), 1, (1, 1)),
        "firework" : ("b", 1, (-2, 2), 2, (2, 1)),
        "spike" : ("s", 0, (-1, -2, 1, 2), 1, (0, 1)),
        "mine" : ("s", 0, (0), 2, (0, 2))
    }
    enemy_names = tuple(enemies.keys())
    directions = (-1, -2, 1, 2)

    def __init__(self) :
        self.ROW = 15
        self.COL = 15
        self.AREA = 225
        self.SIZE = 48
        self.STEPS = 25
        self.ENEMIES = 10
        self.proximity = (-self.COL-1, -self.COL, -self.COL+1, -1, 1, self.COL-1, self.COL, self.COL+1)
        self.first_click = True
        self.all_hazards = []
        super().__init__(self.SIZE*self.COL, self.SIZE*self.ROW + 32, "QueBot")

        self.begin()
        resetable_widgets = Fl_Group(0, 32, self.w(), self.w())
        self.make_board(self.ROW, self.COL, self.SIZE)
        resetable_widgets.end()
        self.start = Fl_Button(0, 0, 48, 32, "S")
        self.start.callback(lambda w: Fl.add_timeout(0.0, self.playout, (0,(0,))))
        self.end()

    def make_board(self, row, col, size) :
        self.tiles = np.array([Fl_Button]*self.AREA)
        self.row_col = []
        i = 0
        for y in range(row) :
            for x in range(col) :
                self.tiles[i] = Fl_Button(size*x, size*y + 32, size, size)
                self.tiles[i].callback(self.qlick, i)
                self.tiles[i].color(96)
                self.tiles[i].labelfont(FL_ZAPF_DINGBATS)
#                self.tiles[i].labelcolor(168)
                self.tiles[i].labelsize(32)
                self.tiles[i].box(FL_FLAT_BOX)
                self.row_col.append((y, x))
                i += 1
        self.d_tiles = self.tiles.reshape(row, col)

    def place_enemy(self, attributes, i) :
        etype, moves, directions, speed, sizes = attributes
        spot = self.row_col[i]
        hazard = []
        hazards = []

        if etype == "s" :
            boinks = []
            if 2 not in sizes :
                while True :
                    vr = 1
                    boink = list(spot)
                    try :
                        direction = directions[random.randrange(len(directions))]
                        vertical = direction % 2 == 0

                        if vertical is True :
                            vr = 2

                        boink[vr-1] += direction//vr

                        dih = self.row_col.index(tuple(boink))
                        break
                    except :
                        pass
            else :
                boink = []
                for d in range(len(Game.directions)) :
                    vertical = Game.directions[d] % 2 == 0
                    if vertical is True :
                        vr = 2
                        boink.extend([spot[0] + Game.directions[d]//2, spot[1]])
                    else :
                        boink.extend([spot[0], spot[1] + Game.directions[d]])
        
            for s in range(0, len(boink), 2) :
                try :
                    boinks.append(self.row_col.index(tuple(boink[s:s+2])))
                except :
                    pass

            for x in range(1, self.STEPS+1) :
                if x % (speed*2) == 0 :
                    hazard = (i, *boinks)
                else :
                    hazard = (i,)
            
                for all_h in self.all_hazards :
                    for h in all_h :
                        if not set(hazard).isdisjoint((*h, self.player_position, *self.surrounding_player)) :
                            return 0
            
                hazards.append(hazard)

        else :
            while True :
                vr = 1
                boink = list(spot)
                try :
                    direction = directions[random.randrange(len(directions))]
                    vertical = direction % 2 == 0

                    if vertical is True :
                        vr = 2

                    boink[vr-1] += direction//vr
                    dih = self.row_col.index(tuple(boink))
                    break
                except :
                    pass

            if etype == "b" :
                for x in range(self.STEPS) :
                    boinks.extend(boink)
                    if vertical is True :
                        if tuple([boinks[0] + direction//vr, boinks[1]]) in self.row_col :
                    else :
                        if tuple([boinks[0], boinks[1] + direction]) in self.row_col :

                # boinks will be a list of lists, each of them is going to have the path of one bullet, the loop will somehow get all these bullet's paths together for each frame

        self.tiles[i].label("|")
        self.all_hazards.append(hazards)
        return 1

    def playout(self, data) :
        i, prev_hazards = data
        prev_hazards = list(prev_hazards)

        for p in prev_hazards :
            self.tiles[p].color(96)
        prev_hazards = []

        for f in self.all_hazards[i] :
            prev_hazards.append(f)
            self.tiles[f].color(128)

        self.redraw()

        if i < self.STEPS-1 :
            Fl.repeat_timeout(0.5, self.playout, (i+1, prev_hazards))

    def make_puzzle(self, i) :
        self.player_position = i
        self.surrounding_player = tuple([x+i for x in self.proximity])
        unpacked_hazards = []
#        self.tiles[i].labelcolor(175)
        self.tiles[i].labelcolor(7)
        self.tiles[i].label("s")
        enemies_placed = 0
        while enemies_placed < self.ENEMIES :
            placement = random.randrange(self.AREA)
            name = Game.enemy_names[random.choice([5,6])]
            enemies_placed += self.place_enemy(Game.enemies[name], placement)
        for h in range(self.STEPS) :
            u_hazards = []
            for hh in range(self.ENEMIES) :
                for hhh in self.all_hazards[hh][h] :
                    u_hazards.append(hhh)

            unpacked_hazards.append(tuple(set(u_hazards)))
        self.all_hazards = unpacked_hazards

    def qlick(self, wid, i) :
        if self.first_click is True :
            self.make_puzzle(i)
            self.first_click = False
            return
        

quebot = Game()
quebot.show()

Fl.visible_focus(0)
Fl.run()
