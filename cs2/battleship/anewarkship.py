from fltk import *
import socket, sys


class Battleship(Fl_Window) :

    def __init__(self, socketdata, tile_size=64, label="Navel Batel") :
        # self.SIZE = tile_size
        self.ROW = 5
        self.COL = 5
        width = tile_size*(self.COL*2 + 1)
        height = tile_size*(self.ROW + 1)
        super().__init__(width, height, label)
        self.status, self.host, self.port = socketdata
        self.images = { "ship" : Fl_PNG_Image("./ship.png").copy(tile_size, tile_size),
                        "hit"  : Fl_PNG_Image("./hit.png").copy(tile_size, tile_size),
                        "miss" : Fl_PNG_Image("./miss.png").copy(tile_size, tile_size),
                        "blank": Fl_PNG_Image("./blank.png").copy(tile_size, tile_size) }

        self.begin()

        self.my_ocean, self.em_ocean = self.make_tiles(tile_size, self.ROW, self.COL)
        self.buttons_onoff((self.my_ocean, self.em_ocean), 0)
        self.connect = Fl_Button(tile_size*(self.COL*2 - 1), tile_size*self.ROW, tile_size*2, tile_size, "Connect")
        self.connect.callback(self.connect_game, socketdata)
        self.resizable(self)

        self.end()

        self.ships = []
        self.attacks = []
        self.hits = 0
        self.damage = 0

    def make_tiles(self, size, row, col) :
        me = []
        you = []
        offset = size*(col + 1)
        i = 0
        for y in range(row) :
            for x in range(col) :
                me.append(Fl_Button(size*x, size*y, size, size))
                you.append(Fl_Button(size*x + offset, size*y, size, size))

                me[i].image(self.images["blank"])
                you[i].image(self.images["blank"])
                me[i].callback(self.deploy_ship, i)
                you[i].callback(self.attack, i)

                i += 1

        return me, you

    def buttons_onoff(self, tilesets, onoff) :
        for tiles in tilesets :
            if onoff == 0 :
                for wid in tiles :
                    wid.when(FL_WHEN_NEVER)
            elif onoff == 1 :
                for wid in tiles :
                    wid.when(FL_WHEN_RELEASE)
    
    def game_end(self, hits, damage) :
        if hits >= 5 :
            return 1
        elif damage >= 5 :
            return 0
        else :
            return -1

    def deploy_ship(self, wid, i) :
        if i not in self.ships :
            self.ships.append(i)
            wid.image(self.images["ship"])
        Fl.check()

        if len(self.ships) == 5 :
            self.buttons_onoff((self.my_ocean,), 0)
            self.conn.sendall(bytes([0]))
            self.conn.recv(1024)
            if self.status == "server" :
                self.buttons_onoff((self.em_ocean,), 1)
            elif self.status == "client" :
                self.hold(self.status)

    def attack(self, wid, i) :
        if i in self.attacks :
            return
        self.buttons_onoff((self.em_ocean,), 0)

        self.attacks.append(i)
        self.conn.sendall(bytes([i]))
        is_hit = self.conn.recv(1024)[0]

        if is_hit == 1 :
            wid.image(self.images["hit"])
            self.hits += 1
        elif is_hit == 0 :
            wid.image(self.images["miss"])
        Fl.check()

        is_game_over = self.game_end(self.hits, self.damage)
        if is_game_over != -1 and self.status == "server" :
            self.conn.close()
        if is_game_over == 1 :
            fl_message("You win!")
            return
        elif is_game_over == 0 :
            fl_message("You lose!")
            return

        self.hold(self.status)
    
    def hold(self, status) :
        missile = self.conn.recv(1024)[0]
        
        is_hit = 1 if missile in self.ships else 0
        
        if is_hit == 1 :
            self.ships.remove(missile)
            self.my_ocean[missile].image(self.images["hit"])
            self.damage += 1
        else :
            self.my_ocean[missile].image(self.images["miss"])
        self.my_ocean[missile].redraw()
        Fl.check()
        
        self.conn.sendall(bytes([is_hit]))
        
        is_game_over = self.game_end(self.hits, self.damage)
        if is_game_over == 0 :
            fl_message("You lose!")
            return
        
        self.buttons_onoff((self.em_ocean,), 1)

    def connect_game(self, wid, socketdata) :
        status, host, port = socketdata

        if status == "server" :
            wid.label("Connecting...")
            Fl.check()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind( (host, port) )
            sock.listen(1)
            self.conn = sock.accept()[0]

        elif status == "client" :
            try :
                self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.conn.connect( (host, port) )
            except :
                fl_message("Host server not found")
                return
        
        wid.label("Connected")
        wid.when(FL_WHEN_NEVER)
        Fl.check()

        self.buttons_onoff((self.my_ocean,), 1)


if __name__ == "__main__" :
    if len(sys.argv) >= 3 :
        status = sys.argv[1]
        host = sys.argv[2]
        port = int(sys.argv[3])
    else :
        status = input("status ('server' or 'client'): ").lower()
        host = input("host ip: ")
        port = int(input("port: "))

    if status in ("server", "client") :
        game = Battleship((status, host, port))
        game.show()
        Fl.visible_focus(0)
        Fl.run()
    else :
        print("Error: status must be in 'server', 'client'")
