from fltk import *
import random
import time
import pickle
from os.path import expanduser
from tkinter import Tk

class Blinken(Fl_Window) :
    pathRecords = expanduser("~/Documents/.ssrecords.pickle")
    difficultyNames = ("Normal","Hard","Extreme")
    resolutionFinder = Tk()
    defaultWidth = resolutionFinder.winfo_screenwidth()//2
    defaultHeight = resolutionFinder.winfo_screenheight()//2

    def __init__(self,width=defaultWidth,height=defaultHeight,title="window_title") :
        super().__init__(width,height,title)

        self.masterSequence = []
        self.userSequence = []
        self.sequenceStarted = False
        self.gameDifficulty = 0
        self.patternAdditions = 1
        self.skipOptions = False
        self.isRecordsShowing = False

        self.begin()
        self.color(fl_rgb_color(33,32,33))

        self.buttonBackground = Fl_Box(height//8,height//8 + 12,width - (height//8)*2,height - (height//8)*2)
        self.buttonBackground.box(FL_FLAT_BOX)
        self.buttonBackground.color(FL_BLACK)
        self.buttonBackground.labelsize(height//8)
        self.buttonBackground.labelcolor(7)

        buttonSize = [self.buttonBackground.w()//2 - height//32,
                      self.buttonBackground.h()//2 - height//32]
        buttonPosition = [self.buttonBackground.w()//2 + height//32,
                          self.buttonBackground.h()//2 + height//32]

        self.buttonYellow = Fl_Button(height//8,
                                      height//8 + 12,
                                      buttonSize[0],
                                      buttonSize[1],
                                      "")
        self.buttonYellow.color(93)

        self.buttonRed = Fl_Button(height//8 + buttonPosition[0],
                                   height//8 + 12,
                                   buttonSize[0],
                                   buttonSize[1],
                                   " ")
        self.buttonRed.color(80)

        self.buttonBlue = Fl_Button(height//8,
                                    height//8 + 12 + buttonPosition[1],
                                    buttonSize[0],
                                    buttonSize[1],
                                    "  ")
        self.buttonBlue.color(176)

        self.buttonGreen = Fl_Button(height//8 + buttonPosition[0],
                                     height//8 + 12 + buttonPosition[1],
                                     buttonSize[0],
                                     buttonSize[1],
                                     "   ")
        self.buttonGreen.color(61)

        self.buttons = [self.buttonYellow,self.buttonRed,self.buttonBlue,self.buttonGreen]

        self.countdown = Fl_Box(height//8 + buttonSize[0],
                                height//8 + 12 + buttonSize[1],
                                height//16,
                                height//16)
        self.countdown.label("")
        self.countdown.labelsize(height//16)
        self.countdown.labelcolor(7)

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
        self.gameOptions.add("Records",0,self.showRecords)
        self.gameOptions.box(FL_ENGRAVED_BOX)
        self.gameOptions.color(0)
        self.gameOptions.textcolor(7)

        self.buttonColors = [3,128,220,FL_GREEN,93,80,176,60]

        self.records = Fl_Browser(0,self.gameOptions.h(),width,height - self.gameOptions.h())
        self.records.color(0)
        self.records.textcolor(7)
        self.records.hide()
        self.updateRecords()

        self.currentScore = Fl_Box(width,0,0,24)
        self.currentScore.label("00")
        self.currentScore.labelcolor(7)
        self.currentScore.labelsize(22)
        self.currentScore.align(FL_ALIGN_LEFT)

        self.end()

    def handleClick(self,wid) :
        if not self.sequenceStarted :
            return
        elif len(wid.label()) == 3 :
            self.userSequence.append(3)
        elif len(wid.label()) == 2 :
            self.userSequence.append(2)
        elif len(wid.label()) == 1 :
            self.userSequence.append(1)
        else :
            self.userSequence.append(0)

        if self.userSequence != self.masterSequence[:len(self.userSequence)] :
            fl_message("Stinker input")
            self.currentScore.label("00")
            self.writeRecords()
            return

        elif len(self.userSequence) == len(self.masterSequence) :
            self.userSequence = []
            self.sequenceStarted = False
            self.currentScore.label((lambda score: f"0{score}" if score < 10 else f"{score}")\
                    (len(self.masterSequence)//self.patternAdditions))
            self.simpleCountdown()
            self.runSequenceLoop()

    def chooseDifficulty(self,wid,difficulty) :
        if self.skipOptions :
            return
        match difficulty :
            case 2 :
                self.gameDifficulty = 2
            case 1 :
                self.gameDifficulty = 1
            case 0 :
                self.gameDifficulty = 0

    def simpleCountdown(self) :
        self.gameOptions.textcolor(40)
        self.skipOptions = True
        for period in range(3,0,-1) :
            self.countdown.label("."*period)
            self.redraw()
            Fl.flush()
            Fl.check()
            time.sleep(0.5)
        self.countdown.label("")

    def beginSequence(self,wid) :
        if self.isRecordsShowing :
            self.showRecords()
            return
        elif self.skipOptions :
            return
        self.currentScore.label("00")
        self.masterSequence = []
        self.sequenceStarted = False

        match self.gameDifficulty :
            case 2 :
                self.patternAdditions = 4
            case 1 :
                self.patternAdditions = 2
            case 0 :
                self.patternAdditions = 1

        self.simpleCountdown()
        self.runSequenceLoop()

    def runSequenceLoop(self) :
        for i in range(len(self.masterSequence) + self.patternAdditions) :
            if i + 1 > len(self.masterSequence) :
                chosenButton = random.randrange(4)
                self.masterSequence.append(chosenButton)
            else :
                chosenButton = self.masterSequence[i]

            self.buttons[chosenButton].color(self.buttonColors[chosenButton])
            self.redraw()
            Fl.flush()
            Fl.check()
            time.sleep(0.5)
            self.buttons[chosenButton].color(self.buttonColors[chosenButton+4])
            self.redraw()
            Fl.flush()
            Fl.check()
            time.sleep(0.1)

        self.sequenceStarted = True
        self.skipOptions = False
        self.gameOptions.textcolor(7)
        self.redraw()

    def showRecords(self,wid=None) :
        if not self.isRecordsShowing :
            self.records.show()
            self.isRecordsShowing = True
            self.updateRecords()
        else :
            self.records.hide()
            self.isRecordsShowing = False
        self.redraw()

    def writeRecords(self) :
        try :
            with open(Blinken.pathRecords,"rb") as recordsFile :
                recordsList = list(pickle.load(recordsFile))
                recordsList.append((len(self.masterSequence) - self.patternAdditions,
                                    Blinken.difficultyNames[self.gameDifficulty]))
        except (FileNotFoundError,EOFError):
            recordsList = [(len(self.masterSequence) - self.patternAdditions,
                            Blinken.difficultyNames[self.gameDifficulty])]

        with open(Blinken.pathRecords,"wb") as recordsFile :
            recordsList.sort(reverse=True)
            pickle.dump(recordsList,recordsFile)
        self.masterSequence = []
        self.userSequence = []

    def updateRecords(self) :
        self.records.clear()
        try :
            with open(Blinken.pathRecords,"rb") as recordsFile :
                recordsList = list(pickle.load(recordsFile))
                recordsList = list(filter(lambda r: r[0] > 0,recordsList))
                for rec in recordsList :
                    self.records.add(str(rec))
        except (FileNotFoundError,EOFError) :
            None

simonsays = Blinken(title="Blinken")
simonsays.show()

Fl.visible_focus(0)
Fl.run()

'''
References:
[Line(s), Link]
5 + 9, https://stackoverflow.com/questions/2057045/os-makedirs-doesnt-understand-in-my-path
227, https://www.geeksforgeeks.org/python/lambda-filter-python-examples/
128, https://stackoverflow.com/questions/1585322/is-there-a-way-to-perform-if-in-pythons-lambda
'''
