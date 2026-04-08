from fltk import *
import random
import time
import pickle

class Blinken(Fl_Window) :
    masterSequence = []
    userSequence = []
    sequenceStarted = False
    gameDifficulty = 0
    patternAdditions = 1
    allChosenButtons = []
    skipOptions = False

    def __init__(self,width,height,title) :
        super().__init__(width,height,title)

        self.begin()
        self.color(fl_rgb_color(33,32,33))

        self.buttonBackground = Fl_Box(height//8,height//6,width - (height//8)*2,height - (height//8)*2)
        self.buttonBackground.box(FL_FLAT_BOX)
        self.buttonBackground.color(FL_BLACK)
        self.buttonBackground.labelsize(height//8)
        self.buttonBackground.labelcolor(7)
        
        self.buttonYellow = Fl_Button(height//8,
                                      height//6,
                                      self.buttonBackground.w()//2 - height//16,
                                      self.buttonBackground.h()//2 - height//16,
                                      "")
        self.buttonYellow.color(94)

        self.buttonRed = Fl_Button(height//8 + self.buttonBackground.w()//2 + height//16,
                                   height//6,
                                   self.buttonBackground.w()//2 - height//16,
                                   self.buttonBackground.h()//2 - height//16,
                                   " ")
        self.buttonRed.color(80)

        self.buttonBlue = Fl_Button(height//8,
                                    height//6 + self.buttonBackground.h()//2 + height//16,
                                    self.buttonBackground.w()//2 - height//16,
                                    self.buttonBackground.h()//2 - height//16,
                                    "  ")
        self.buttonBlue.color(176)

        self.buttonGreen = Fl_Button(height//8 + self.buttonBackground.w()//2 + height//16,
                                     height//6 + self.buttonBackground.h()//2 + height//16,
                                     self.buttonBackground.w()//2 - height//16,
                                     self.buttonBackground.h()//2 - height//16,
                                     "   ")
        self.buttonGreen.color(62)

        self.buttons = [self.buttonYellow,self.buttonRed,self.buttonBlue,self.buttonGreen]
        
        for but in range(len(self.buttons)) :
            self.buttons[but].callback(self.handleClick)
            self.buttons[but].box(FL_ENGRAVED_BOX)
            self.resizable(self.buttons[but])
        self.resizable(self.buttonBackground)

        self.gameOptions = Fl_Menu_Bar(0,0,width,24)
        self.gameOptions.add("Begin",FL_ALT | ord("s"),self.beginSequence)
        self.gameOptions.add("Difficulty/Normal",0,self.chooseDifficulty,0)
        self.gameOptions.add("Difficulty/Hard",0,self.chooseDifficulty,1)
        self.gameOptions.add("Difficulty/Extreme",0,self.chooseDifficulty,2)
        self.gameOptions.box(FL_ENGRAVED_BOX)
        self.gameOptions.color(0)
        self.gameOptions.textcolor(7)

        self.buttonColors = [3,128,220,FL_GREEN,94,80,176,62]

        self.end()

    def handleClick(self,wid) :
        if not Blinken.sequenceStarted :
            return
        elif len(wid.label()) == 3 :
            Blinken.userSequence.append(3)
        elif len(wid.label()) == 2 :
            Blinken.userSequence.append(2)
        elif len(wid.label()) == 1 :
            Blinken.userSequence.append(1)
        else :
            Blinken.userSequence.append(0)

        if Blinken.userSequence != Blinken.masterSequence[:len(Blinken.userSequence)] :
            fl_message("Stinker input")
            with open("ssrecords.pickle","rb") as recordsFile :
                recordsList = list(pickle.load(recordsFile))
                recordsList.append(len(Blinken.masterSequence) - patternAdditions)
            with open("ssrecords.pickle","wb") as recordsFile :
                pickle.dump(recordsList,recordsFile)
            Blinken.masterSequence = []
            Blinken.userSequence = []
            return

        elif len(Blinken.userSequence) == len(Blinken.masterSequence) :
            Blinken.userSequence = []
            Blinken.sequenceStarted = False
            self.simpleCountdown()
            self.runSequenceLoop()

    def chooseDifficulty(self,wid,difficulty) :
        if Blinken.skipOptions :
            return
        match difficulty :
            case 2 :
                Blinken.gameDifficulty = 2
            case 1 :
                Blinken.gameDifficulty = 1
            case 0 :
                Blinken.gameDifficulty = 0

    def simpleCountdown(self) :
        self.gameOptions.textcolor(40)
        Blinken.skipOptions = True
        for period in range(3,-1,-1) :
            self.buttonBackground.label("."*period)
            self.redraw()
            Fl.flush()
            Fl.check()
            time.sleep(0.5)
    
    def beginSequence(self,wid) :
        if Blinken.skipOptions :
            return
        Blinken.masterSequence = []
        Blinken.sequenceStarted = False
        
        match Blinken.gameDifficulty :
            case 2 :
                Blinken.patternAdditions = 4
            case 1 :
                Blinken.patternAdditions = 2
            case 0 :
                Blinken.patternAdditions = 1
        
        self.simpleCountdown()
        self.runSequenceLoop()

    def runSequenceLoop(self) :

        for i in range(len(Blinken.masterSequence) + Blinken.patternAdditions) :
            if i + 1 > len(Blinken.masterSequence) :
                chosenButton = random.randrange(4)
                Blinken.allChosenButtons.append(chosenButton)
                Blinken.masterSequence.append(chosenButton)
            else :
                chosenButton = Blinken.masterSequence[i]

            self.buttons[chosenButton].color(self.buttonColors[chosenButton])
            self.redraw()
            Fl.flush()
            Fl.check()
            time.sleep(0.5)
            self.buttons[chosenButton].color(self.buttonColors[chosenButton+4])
            self.redraw()
            Fl.flush()
            Fl.check()
            time.sleep(0.5)

        Blinken.sequenceStarted = True
        Blinken.skipOptions = False
        self.gameOptions.textcolor(7)
        self.redraw()

ligma = Blinken(512,256,"LirmaBlinken")
ligma.show()

#Fl.background(33,32,33)
Fl.visible_focus(0)
Fl.run()
