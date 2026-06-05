from fltk import *
import random
import pickle


# FINE I'LL FOLLOW THE STUPID STYLE GUIDE, GOD!

class Minesweeper(Fl_Window) :

    def __init__(self) :
        self.make_game(9, 9, 64, 10, 0, "Minesweeper")
        super().__init__(self.width, self.height, self.title)
        self.make_leaderboard()

    def make_game(self, rows, columns, size, mines, difficulty, title) :
        self.difficulty = difficulty
        self.row = rows
        self.col = columns
        self.area = rows*columns
        self.proximity = (-columns-1, -columns, -columns+1, -1, 1, columns-1, columns, columns+1)
        self.size = size
        self.max_mines = mines
        self.bombs = []
        self.flags = []
        self.chunk = []
        self.first_click = True
        self.attributes = (rows, columns, size, mines, difficulty, title)

        self.master = [2 for i in range(self.area)]
        self.hints = [0 for i in range(self.area)]

        self.place_mines()
        self.assign_clear()
        self.assign_numbers()

        self.width = size*columns
        self.height = size*rows + 32
        self.title = title

    def make_leaderboard(self) :
        self.leaderboard = Fl_Window(320, 512)
        self.leaderboard.begin()
        tabnames = ("Beginner", "Intermediate", "Expert", "Custom")
        self.records_browser = Fl_Tabs(16, 16, 288, 480)
        self.tabs = []
        self.display = []

        try :
            with open("msrecords.pickle", "rb") as f :
                records = pickle.load(f)
        except :
            records = [[], [], [], []]

        for i in range(4) :
            self.tabs.append(Fl_Group(16, 48, 208, 480, tabnames[i]))
            self.display.append(Fl_Browser(32, 64, 256, 416))
            self.display[i].textfont(FL_HELVETICA)
            self.display[i].textsize(28)
            self.update_records(records[i], i)
            self.tabs[i].end()

        self.records_browser.end()
        self.leaderboard.set_modal()
        self.leaderboard.color(43)
        self.leaderboard.end()

    def custom_game(self) :
        pass

    def place_mines(self) :
        m = 0
        while m < self.max_mines :
            i = random.randrange(len(self.master))
            if self.master[i] == 2 :
                self.master[i] = 1
                self.bombs.append(i)
                m += 1

    def assign_clear(self) :
        for i in range(self.area) :
            if self.radius(i, 0) is False :
                self.master[i] = 0

    def assign_numbers(self) :
        for i in range(self.area) :
            self.hints[i] = self.radius(i, 1)

    def radius(self, i, purpose) :
        temp_prox = list(self.proximity)
        if self.master[i] == 1 and purpose not in (-1, 3, 4, 5) :
            return 0

        if i % self.col == 0 :
            for p in (5, 3, 0) :
                temp_prox.pop(p)
        elif i in range(self.col-1, self.area, self.col) :
            for p in (7, 4, 2) :
                temp_prox.pop(p)

        output = None
        if purpose in (0, 4) :
            output = False
        elif purpose == 1 :
            output = 0
        elif purpose in (-1, 3, 5, 6) :
            output = []

        for d in temp_prox :
            if i+d not in range(self.area) :
                continue
            if purpose == -1 :
                output.append(i+d)
            elif purpose == 6 :
                if i+d in self.flags :
                    output.append(i+d)

            if self.master[i+d] == 1 :
                if purpose in (0, 4) :
                    output = True
                elif purpose == 1 :
                    output += 1
                elif purpose == 3 :
                    output.append(i+d)

            elif self.master[i+d] == 0 :
                if purpose == 5 :
                    output.append(i+d)

            if purpose == 2 :
                if i+d not in self.chunk and self.master[i+d] in (0, 2) :
                    self.chunk.append(i+d)

                    if self.master[i+d] == 0 :
                        self.chunk_clear(i+d)

        return output

    def chunk_clear(self, i) :
        self.radius(i, 2)

    def replace_empty(self, i) :
        empty_indexes = self.radius(i, 5)
        for i in empty_indexes :
            self.master[i] = 2

    def label_boxes(self, w) :
        if self.hints[w] != 0 :
            self.boxes[w].label(str(self.hints[w]))
        self.boxes[w].labelsize(self.size//2 + self.size//4)
        self.boxes[w].labelfont(FL_SCREEN_BOLD)
        self.boxes[w].hide()
        self.color_numbers(w)

    def make_board(self, size, reset=False) :
        self.resetable_widgets = Fl_Group(0, 32, size*self.col, size*self.row)

        self.tiles = []
        self.boxes = []
        self.around = []

        for y in range(self.row) :
            for x in range(self.col) :
                self.tiles.append(Fl_Button(size*x, size*y + 32, size, size))
                self.boxes.append(Fl_Box(size*x, size*y + 32, size, size))
                self.around.append(Fl_Button(size*x, size*y + 32, size, size))

        for w in range(self.area) :
            self.tiles[w].callback(self.sweep)
            self.tiles[w].labelsize(size//2 + size//4)
            self.tiles[w].labelfont(FL_ZAPF_DINGBATS)
            self.label_boxes(w)
            self.around[w].callback(self.radius_sweep)
            self.around[w].deactivate()
            self.around[w].box(FL_NO_BOX)

        self.resetable_widgets.end()
        if reset is True :
            return

        self.restart = Fl_Menu_Bar(0, 0, self.width - 192, 32)
        self.restart.add("New", FL_CTRL | ord("r"), self.reset_game, 0)
        self.restart.add("Difficulty/Easy", 0, self.reset_game, (9, 9, 64, 10, 0, "Minesweeper"))
        self.restart.add("Difficulty/Intermediate", 0, self.reset_game, (16, 16, 32, 40, 1, "Minesweeper"))
        self.restart.add("Difficulty/Expert", 0, self.reset_game, (16, 30, 32, 99, 2, "Minesweeper"))
        self.restart.add("Records", 0, self.show_records)
        self.restart.box(FL_BORDER_BOX)
        self.restart.textfont(FL_HELVETICA_BOLD)

        self.mine_count = Fl_Box(self.restart.w(), 0, 64, 32)
        self.overly_complicated_mine_count_function()
        self.mine_count.labelsize(18)
        self.mine_count.labelfont(FL_HELVETICA_BOLD)
        self.mine_count.box(FL_BORDER_BOX)

        self.spacer = Fl_Box(self.restart.w() + self.mine_count.w(), 0, 64, 32)
        self.spacer.box(FL_BORDER_BOX)

        self.timer = Fl_Box(self.restart.w() + self.mine_count.w()*2, 0, 64, 32)
        self.timer.label("00:00")
        self.timer.labelsize(18)
        self.timer.labelfont(FL_HELVETICA_BOLD)
        self.timer.box(FL_BORDER_BOX)

    def color_numbers(self, w) :
        match self.hints[w] :
            case 1 :
                self.boxes[w].labelcolor(FL_BLUE)
            case 2 :
                self.boxes[w].labelcolor(61)
            case 3 :
                self.boxes[w].labelcolor(FL_RED)
            case 4 :
                self.boxes[w].labelcolor(136)
            case 5 :
                self.boxes[w].labelcolor(81)
            case 6 :
                self.boxes[w].labelcolor(140)
            case 7 :
                self.boxes[w].labelcolor(0)
            case 8 :
                self.boxes[w].labelcolor(42)

    def hide_tiles(self, i) :
        if self.tiles[i].label() == "F" :
            return
        self.tiles[i].deactivate()
        self.tiles[i].color(43)
        self.tiles[i].box(FL_BORDER_BOX)
        self.master[i] = 9

        if self.boxes[i].label() is not None :
            self.boxes[i].show()
            self.around[i].activate()

    def flagging(self, i) :
        if self.tiles[i].label() == "F" :
            self.tiles[i].label(None)
            self.flags.remove(i)
            self.overly_complicated_mine_count_function()
            return
        self.tiles[i].label("F")
        self.flags.append(i)
        self.overly_complicated_mine_count_function()

    def overly_complicated_mine_count_function(self) :
        new_label = self.max_mines - len(self.flags)
        if new_label >= 0 :
            if new_label > 99 :
                self.mine_count.label(" ".join(str(new_label)))
            elif new_label > 9 :
                self.mine_count.label("0 " + " ".join(str(new_label)))
            else :
                self.mine_count.label("0 0 " + str(new_label))
        else :
            if -100 < new_label < -9 :
                self.mine_count.label(" ".join(str(new_label)))
            elif new_label > -100 :
                self.mine_count.label("- 0 " + " ".join(str(abs(new_label))))

    def spawn_protection(self, i) :
        bomb_indexes = []
        adjacent = self.radius(i, -1)
        adjacent.append(i)

        if self.master[i] == 1 :
            bomb_indexes.append(i)
        if self.radius(i, 4) is True :
            bomb_indexes.extend(self.radius(i, 3))

        x = 0
        while x < len(bomb_indexes) :
            new_place = random.randrange(self.area)
            if self.master[new_place] != 1 and new_place not in adjacent :
                self.master[bomb_indexes[x]] = 2
                self.bombs[self.bombs.index(bomb_indexes[x])] = new_place
                self.master[new_place] = 1
                self.replace_empty(new_place)
                x += 1

        self.assign_clear()
        self.assign_numbers()
        for w in range(self.area) :
            self.boxes[w].label(None)
            self.label_boxes(w)

    def game_timer(self, elapsed) :
        elapsed += 1
        self.elapsed = elapsed
        self.timer.label("%02d:%02d" % (self.convert_seconds(elapsed))) # https://stackoverflow.com/questions/134934/display-number-with-leading-zeros
        if elapsed < 3600 :
            Fl.repeat_timeout(1.0, self.game_timer, elapsed)

    def convert_seconds(self, s) :
        minutes = s // 60
        seconds = s % 60
        return minutes, seconds

    def win_lose(self, status) :
        self.show_mines(status)
        Fl.remove_timeout(self.game_timer)
        for i in range(self.area) :
            self.tiles[i].when(FL_WHEN_NEVER)
            self.around[i].when(FL_WHEN_NEVER)
        if status == 0 :
            self.mine_count.label("BOZO")
            fl_message("feels bad man")
        elif status == 1 :
            self.mine_count.label("0 0 0")
            self.save_score(self.elapsed, self.difficulty)
            fl_message(f"do it again i wasn't looking  {self.timer.label()}")

    def save_score(self, new_score, difficulty) :
        try :
            with open("msrecords.pickle", "rb") as f :
                records = pickle.load(f)
        except :
            records = [[], [], [], []]

        dif_records = records[difficulty]

        if len(dif_records) < 10 :
            dif_records.append(new_score)
        elif new_score < dif_records[-1] :
            dif_records[-1] = new_score
        else :
            return

        dif_records.sort()

        self.update_records(dif_records, difficulty)

        with open("msrecords.pickle", "wb") as f :
            pickle.dump(records, f)
            print(records)

    def show_records(self, wid) :
        self.leaderboard.show()

    def update_records(self, dif_records, i) :
        self.display[i].clear()
        for r in dif_records :
            self.display[i].add("             %02d : %02d" % (self.convert_seconds(r)))

    def show_mines(self, game_status) :
        unflagged_mines = self.bombs[:]
        if game_status == 0 :
            for i in range(len(self.flags)) :
                if self.flags[i] in self.bombs :
                    unflagged_mines.remove(self.flags[i])
                    continue
                self.tiles[self.flags[i]].color(171)
                self.tiles[self.flags[i]].down_color(171)

            for i in range(len(unflagged_mines)) :
                self.tiles[unflagged_mines[i]].label("Y")
                self.tiles[unflagged_mines[i]].color(171)
                self.tiles[unflagged_mines[i]].down_color(171)
        elif game_status == 1 :
            for i in range(self.area) :
                if self.master[i] == 1 :
                    self.tiles[i].label("F")

        self.redraw()

    def radius_sweep(self, wid) :
        if Fl.event_button() != 1 :
            return
        center = self.around.index(wid)
        adjacent = self.radius(center, -1)
        adjacent_values = [self.master[x] for x in adjacent]
        adjacent_bombs = [adjacent[x] for x in range(len(adjacent)) if adjacent_values[x] == 1]
        adjacent_flags = self.radius(center, 6)
        bomb_count = len(adjacent_bombs)
        flag_count = len(adjacent_flags)

        if flag_count > bomb_count or flag_count == 0 or flag_count < bomb_count :
            return

        if adjacent_flags != adjacent_bombs :
            self.win_lose(0)
            return

        for i in range(len(adjacent)) :
            if adjacent_values[i] == 2 :
                self.hide_tiles(adjacent[i])

        if 0 in adjacent_values :
            new_center = adjacent[adjacent_values.index(0)]
            self.sweep(self.tiles[new_center])
            return

        if {0,2}.isdisjoint(self.master) is True :
            self.win_lose(1)

    def sweep(self, wid) :
        center = self.tiles.index(wid)
        if Fl.event_button() == 3 :
            self.flagging(center)
            return
        if self.tiles[center].label() == "F" :
            return

        if self.first_click is True :
            Fl.add_timeout(1.0, self.game_timer, 0)
            if self.master[center] != 0 :
                self.spawn_protection(center)
            self.first_click = False

        match self.master[center] :
            case 1 :
                self.win_lose(0)

            case 0 :
                self.chunk.append(center)
                self.chunk_clear(center)
                for i in range(self.area) :
                    if i in self.chunk :
                        self.hide_tiles(i)
                self.chunk = []

            case 2 :
                self.hide_tiles(center)

        if {0, 2}.isdisjoint(self.master) is True : # https://stackoverflow.com/questions/47608858/if-multiple-elements-are-not-in-a-list-then
            self.win_lose(1)

    def reset_game(self, wid, attributes) :
        if attributes == 0 :
            attributes = self.attributes[:]
        else :
            self.attributes = attributes[:]

        rows, columns, size, mines, difficulty, title = attributes
        Fl.remove_timeout(self.game_timer)
        self.make_game(rows, columns, size, mines, difficulty, title)
        self.timer.label("00:00")
        self.overly_complicated_mine_count_function()
        self.resetable_widgets.clear()
        self.begin()
        self.resize(self.x(), self.y(), self.width, self.height)
        self.restart.resize(0, 0, self.width - 192, 32)
        self.mine_count.resize(self.restart.w(), 0, 64, 32)
        self.spacer.resize(self.mine_count.x() + 64, 0, 64, 32)
        self.timer.resize(self.spacer.x() + 64, 0, 64, 32)
        self.make_board(self.size, True)
        self.end()


if __name__ == "__main__" :
    sweeper = Minesweeper()
    sweeper.begin()
    sweeper.make_board(sweeper.size)
    sweeper.end()
    sweeper.show()

    for i in range(sweeper.row) :
        print(sweeper.master[i*sweeper.row:i*sweeper.row+sweeper.col])

    Fl.visible_focus(0)
    Fl.run()
