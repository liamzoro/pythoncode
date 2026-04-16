from fltk import *
import random
import time
import pickle
from os.path import expanduser
from sys import exit
try :
    from tkinter import Tk
except ModuleNotFoundError as e :
    fl_message(f"{e}: Dependency Missing <tkinter>")
    exit()
except ImportError as e :
    fl_message(f"{e}: Dependency Missing <tk>")
    exit()
from subprocess import Popen


class Blinken(Fl_Window) :
    pathRecords = expanduser("~/Documents/.ssrecords.pickle")
    soundEffects = ("yellow.mp3","red.mp3","blue.mp3","green.mp3","error.mp3")
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
        self.isRecordsShowing = False
        self.gameOverTimer = False

        self.begin()
        self.color(fl_rgb_color(33,32,33))

        self.buttons = []

        self.buttonBackground = Fl_Box(height//8,height//8 + 12,
                                       width - (height//8)*2,
                                       height - (height//8)*2)
        self.buttonBackground.box(FL_FLAT_BOX)
        self.buttonBackground.color(FL_BLACK)

        buttonSize = (self.buttonBackground.w()//2 - height//32,
                      self.buttonBackground.h()//2 - height//32)
        buttonPosition = (0,self.buttonBackground.w()//2 + height//32,
                          self.buttonBackground.h()//2 + height//32)
        self.buttonColors = [3,128,220,2,93,80,176,60]

        for but in range(4) :
            self.buttons.append(Fl_Button(height//8 + buttonPosition[(but*3)%2],
                                          height//8 + 12 + buttonPosition[int((but//1.6)*2)],
                                          buttonSize[0],
                                          buttonSize[1],
                                          " "*but))
            self.buttons[but].box(FL_ENGRAVED_BOX)
            self.buttons[but].callback(self.handleClick)
            self.buttons[but].color(self.buttonColors[but+4])
            self.buttons[but].down_color(self.buttonColors[but])

        for but in range(4) :
            self.resizable(self.buttons[but])
        self.resizable(self.buttonBackground)

        self.countdown = Fl_Box(height//8 + buttonSize[0],
                        height//8 + 12 + buttonSize[1],
                        height//16,
                        height//16)
        self.countdown.labelsize(height//16)
        self.countdown.labelcolor(7)

        self.gameOptions = Fl_Menu_Bar(0,0,width,24)
        self.gameOptions.add("Begin",FL_ALT | ord("s"),self.beginSequence)
        self.gameOptions.add("Difficulty/Normal",0,self.chooseDifficulty,0)
        self.gameOptions.add("Difficulty/Hard",0,self.chooseDifficulty,1)
        self.gameOptions.add("Difficulty/Extreme",0,self.chooseDifficulty,2)
        self.gameOptions.add("Records",0,self.showRecords)
        self.gameOptions.box(FL_ENGRAVED_BOX)
        self.gameOptions.color(0)
        self.gameOptions.textcolor(7)

        self.records = Fl_Browser(0,self.gameOptions.h(),width,height - self.gameOptions.h())
        self.records.color(0)
        self.records.textcolor(7)
        self.records.textsize((lambda s: s[0]//32 if s[0] < s[1] else s[1]//32)((width,height))) # lots and lots of lambdas to come
        self.records.hide()
        self.updateRecords()

        self.currentScore = Fl_Box(width,0,0,24)
        self.currentScore.label("00")
        self.currentScore.labelcolor(7)
        self.currentScore.labelsize(22)
        self.currentScore.align(FL_ALIGN_LEFT)
        self.redraw()
        self.end()

    def handleClick(self,wid) :
        button = len(wid.label())
        if self.sequenceStarted is False :
            return
        if self.gameOverTimer is True :
            self.gameOverTimer = False
            Fl.remove_timeout(self.gameOver)
        if button == 3 :
            self.userSequence.append(3)
        elif button == 2 :
            self.userSequence.append(2)
        elif button == 1 :
            self.userSequence.append(1)
        else :
            self.userSequence.append(0)

        if self.userSequence != self.masterSequence[:len(self.userSequence)] :
            self.gameOver(False)
            return

        self.playSound(button)
        Fl.add_timeout(5.0,self.gameOver)
        self.gameOverTimer = True

        if len(self.userSequence) == len(self.masterSequence) :
            self.userSequence = []
            self.sequenceStarted = False
            self.currentScore.label((lambda score: f"0{score}" if score < 10 else f"{score}")\
                    (len(self.masterSequence)//self.patternAdditions))
            Fl.remove_timeout(self.gameOver)
            self.simpleCountdown()
            self.runSequenceLoop()


    def chooseDifficulty(self,wid,difficulty) :
        match difficulty :
            case 2 :
                self.gameDifficulty = 2
            case 1 :
                self.gameDifficulty = 1
            case 0 :
                self.gameDifficulty = 0

    def simpleCountdown(self,period=3) :
            self.countdown.label("."*period)
            self.redraw()
            Fl.flush()
            Fl.check()
            if period == 0 :
                self.runSequenceLoop()

    def beginSequence(self,wid) :
        if self.isRecordsShowing is True :
            self.showRecords()
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
        Fl.add_timeout(0.33,self.simpleCountdown,2)
        Fl.add_timeout(0.67,self.simpleCountdown,1)
        Fl.add_timeout(1.0,self.simpleCountdown,0)

    def runSequenceLoop(self) :
        sequenceLength = len(self.masterSequence) + self.patternAdditions
        for i in range(sequenceLength) :
            if i + 1 > len(self.masterSequence) :
                chosenButton = random.randrange(4)
                self.masterSequence.append(chosenButton)
            else :
                chosenButton = self.masterSequence[i]

            self.playSound(chosenButton)
            self.buttons[chosenButton].color(self.buttonColors[chosenButton])
            self.redraw()
            Fl.flush()
            Fl.check()
            time.sleep(0.5)
            self.buttons[chosenButton].color(self.buttonColors[chosenButton+4])
            self.redraw()
            Fl.flush()
            Fl.check()
            if i != sequenceLength - 1 :
                time.sleep(0.25)

        self.sequenceStarted = True
        self.redraw()
        self.gameOverTimer = True
        Fl.add_timeout(5.0,self.gameOver)

    def showRecords(self,wid=None) :
        if self.isRecordsShowing is False :
            self.records.show()
            self.isRecordsShowing = True
            self.updateRecords()
        else :
            self.records.hide()
            self.isRecordsShowing = False
        self.redraw()

    def writeRecords(self) :
        calculatedScore = (len(self.masterSequence) - self.patternAdditions)//self.patternAdditions
        try :
            with open(Blinken.pathRecords,"rb") as recordsFile :
                recordsList = list(pickle.load(recordsFile))
                recordsList.append((calculatedScore,
                                    Blinken.difficultyNames[self.gameDifficulty]))
        except (FileNotFoundError,EOFError):
            recordsList = [(calculatedScore,
                            Blinken.difficultyNames[self.gameDifficulty])]

        with open(Blinken.pathRecords,"wb") as recordsFile :
            recordsList.sort(reverse=True)
            recordsList = sorted(recordsList,key=lambda r: r[1])
            pickle.dump(recordsList,recordsFile)

    def updateRecords(self) :
        self.records.clear()
        try :
            with open(Blinken.pathRecords,"rb") as recordsFile :
                recordsList = list(pickle.load(recordsFile))
            recordsList = list(filter(lambda r: r[0] > 0,recordsList))

            extremeRecords = ["- Extreme","\n"]
            hardRecords = ["- Hard","\n"]
            normalRecords = ["- Normal","\n"]

            for r in recordsList :
                if "Extreme" in r :
                    extremeRecords.insert(-1,r)
                elif "Hard" in r :
                    hardRecords.insert(-1,r)
                elif "Normal" in r :
                    normalRecords.insert(-1,r)
            recordsList = extremeRecords + hardRecords + normalRecords

            for rec in recordsList :
                if isinstance(rec,str) :
                    self.records.add(rec)
                    continue
                self.records.add(str(rec[0]))
        except (FileNotFoundError,EOFError) :
            None

    def playSound(self,sound) :
        Popen(["paplay",Blinken.soundEffects[sound]]) # cleaner and more readable than typing that a bunch

    def gameOver(self,timedOut=True) :
        self.playSound(4)
        for but in self.buttons :
            but.value(0)
        if timedOut is True :
            fl_message("Game Over\nTime's Up")
        else :
            fl_message("Game Over")
        self.currentScore.label("00")
        self.writeRecords()
        self.masterSequence = []
        self.userSequence = []
        self.sequenceStarted = False


simonsays = Blinken(title="Blinken")
simonsays.show()

Fl.visible_focus(0)
Fl.run()


'''
References:
[Line(s), Link]
5 + 9, https://stackoverflow.com/questions/2057045/os-makedirs-doesnt-understand-in-my-path
227, https://www.geeksforgeeks.org/python/lambda-filter-python-examples/
228, https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
128, https://stackoverflow.com/questions/1585322/is-there-a-way-to-perform-if-in-pythons-lambda
'''
