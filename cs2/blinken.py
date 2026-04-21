from fltk import *
import random
import pickle
from sys import exit
try :
    from tkinter import Tk
    importSuccess = True
except (ModuleNotFoundError,ImportError) as e :
    importSuccess = False
    print("Recommended dependency missing")
    print(e)
from subprocess import Popen


class Blinken(Fl_Window) :
    soundEffects = ("yellow.mp3","red.mp3","blue.mp3","green.mp3","error.mp3")
    difficultyNames = {1:"Normal",2:"Hard",4:"Extreme"}
    if importSuccess : # get screen info of the user, to keep window size consistent
        resolutionFinder = Tk()
        defaultWidth = resolutionFinder.winfo_screenwidth()//2
        defaultHeight = resolutionFinder.winfo_screenheight()//2
    else : # (1920x1080) / 2 a good default
        defaultWidth = 960
        defaultHeight = 540

    def __init__(self,width=defaultWidth,height=defaultHeight,title="window_title") :
        super().__init__(width,height,title)

        self.title = title # saving to change window title later
        self.masterSequence = []
        self.userSequence = []
        self.patternAdditions = 1
        self.sequenceLength = 0
        self.sequenceStarted = False
        self.isRecordsShowing = False

        self.begin()
        self.label(f"{title} - Normal")
        self.color(fl_rgb_color(33,32,33)) # dark mode reigns supreme

        self.buttons = []

        self.buttonBackground = Fl_Box(height//8,height//8 + 12,
                                       width - (height//8)*2,
                                       height - (height//8)*2)
        self.buttonBackground.box(FL_FLAT_BOX)
        self.buttonBackground.color(FL_BLACK)

        buttonSize = (self.buttonBackground.w()//2 - height//32,
                      self.buttonBackground.h()//2 - height//32)
        buttonPosition = (0,self.buttonBackground.w()//2 + height//32,
                          self.buttonBackground.h()//2 + height//32) # to prevent repeated code ^^^
        self.buttonColors = [3,128,220,2,93,80,176,60]

        for but in range(4) : # took some time, but figured out equations that got the right indices
            self.buttons.append(Fl_Button(height//8 + buttonPosition[(but*3)%2],
                                          height//8 + 12 + buttonPosition[int((but//1.6)*2)],
                                          buttonSize[0],
                                          buttonSize[1],
                                          " "*but)) # label length tells the program which button was pressed
            self.buttons[but].box(FL_ENGRAVED_BOX)
            self.buttons[but].callback(self.handleClick)
            self.buttons[but].color(self.buttonColors[but+4])
            self.buttons[but].down_color(self.buttonColors[but])
        # creates all buttons in a loop ^^^ (harder to read, but much less repetition)

        self.countdown = Fl_Box(height//8 + buttonSize[0],
                        height//8 + 12 + buttonSize[1],
                        height//16,
                        height//16)
        self.countdown.labelsize(height//16)
        self.countdown.labelcolor(7) # to visualize the countdown between sequences

        self.gameOptions = Fl_Menu_Bar(0,0,width,24)
        self.gameOptions.add("Begin",FL_ALT | ord("s"),self.beginSequence)
        self.gameOptions.add("Difficulty/Normal",0,self.chooseDifficulty,0)
        self.gameOptions.add("Difficulty/Hard",0,self.chooseDifficulty,1)
        self.gameOptions.add("Difficulty/Extreme",0,self.chooseDifficulty,2)
        self.gameOptions.add("Records",0,self.showRecords)
        self.gameOptions.box(FL_ENGRAVED_BOX) # extra stuff ^^^
        self.gameOptions.color(0)
        self.gameOptions.textcolor(7)

        self.records = Fl_Browser(0,self.gameOptions.h(),width,height - self.gameOptions.h())
        self.records.color(0)
        self.records.textcolor(7)
        self.records.textsize((lambda s: s[0]//32 if s[0] < s[1] else s[1]//32)((width,height))) # lots and lots of lambdas to come
        self.records.hide() # to keep text size conistent whether a monitor is taller or wider ^^^
        self.updateRecords()

        self.currentScore = Fl_Box(width,0,0,24)
        self.currentScore.label("00")
        self.currentScore.labelcolor(7)
        self.currentScore.labelsize(22)
        self.currentScore.align(FL_ALIGN_LEFT) # simple way to keep it in the same place no matter what

        self.resizable(self) # "self" explanatory HAHAHAHAHAHAHAHAHAHAHA

        self.end()

    def handleClick(self,wid) :
        button = len(wid.label())
        if self.sequenceStarted is False :
            return # makes clicks do nothing while sequence is playing out

        if button == 3 : # a pretty elegant system if i do say so myself
            self.userSequence.append(3)
        elif button == 2 :
            self.userSequence.append(2)
        elif button == 1 :
            self.userSequence.append(1)
        else :
            self.userSequence.append(0)
            
        if self.userSequence != self.masterSequence[:len(self.userSequence)] :
            self.gameOver(False)
            return # on every click, checks equality of portion of masterSequence with userSequence ^^^

        Fl.remove_timeout(self.gameOver)
        Fl.add_timeout(5.0,self.gameOver) # resets gameOver timeout on every click
        self.playSound(button)

        if len(self.userSequence) == len(self.masterSequence) :
            self.userSequence = []
            self.sequenceStarted = False
            self.currentScore.label((lambda score: f"0{score}" if score < 10 else f"{score}")\
                    (len(self.masterSequence)//self.patternAdditions)) # used lambda func to substitute <<<THAT for "score"
            # to add zero before single digit numbers ^^^
            Fl.remove_timeout(self.gameOver)
            self.simpleCountdown()
            for t in range(1,4) : # admittedly a bit clunky, might use repeats instead later
                Fl.add_timeout(0.33*t,self.simpleCountdown,3-t)


    def chooseDifficulty(self,wid,difficulty) : # pretty self explanatory
        self.removeAllTimeouts() # stops the game
        match difficulty :
            case 2 :
                self.patternAdditions = 4
                self.label(f"{self.title} - Extreme")
            case 1 :
                self.patternAdditions = 2
                self.label(f"{self.title} - Hard")
            case 0 :
                self.patternAdditions = 1
                self.label(f"{self.title} - Normal")
        self.currentScore.label("00")
        self.masterSequence = []
        self.sequenceStarted = False

    def simpleCountdown(self,period=3) : # ( ...  ..  . ) 3 2 1 GO!
            self.countdown.label("."*period)
            self.redraw()
            if period == 0 : # start the sequence when there are no more periods drawn
                self.runSequenceLoop()

    def beginSequence(self,wid) :
        if self.isRecordsShowing is True : # so a game isn't started when looking at records
            self.showRecords()
            return
        self.removeAllTimeouts()
        self.currentScore.label("00")
        self.currentScore.labelfont(FL_HELVETICA)
        self.masterSequence = []
        self.sequenceStarted = False

        self.simpleCountdown()
        for t in range(1,4) :
            Fl.add_timeout(0.33*t,self.simpleCountdown,3-t)

    def flashButton(self,buttonpress) :
        button,press = buttonpress[:-1]
        iteration = buttonpress[-1]

        if press is True :
            self.playSound(button)
            self.buttons[button].color(self.buttonColors[button])
            self.redraw()
            Fl.add_timeout(0.5,self.flashButton,(button,False,iteration))
        else :
            self.buttons[button].color(self.buttonColors[button+4])
            self.redraw()

            if iteration == self.sequenceLength - 1 :
                self.sequenceStarted = True
                self.redraw()
                Fl.add_timeout(5.0,self.gameOver)


    def runSequenceLoop(self) :
        self.sequenceLength = len(self.masterSequence) + self.patternAdditions
        for i in range(self.sequenceLength):
            if i + 1 > len(self.masterSequence) :
                chosenButton = random.randrange(4)
                self.masterSequence.append(chosenButton)
            else :
                chosenButton = self.masterSequence[i]
            Fl.add_timeout(0.75*i,self.flashButton,(chosenButton,True,i))

    def showRecords(self,wid=None) :
        if self.isRecordsShowing is False :
            self.records.show()
            self.isRecordsShowing = True
        else :
            self.records.hide()
            self.isRecordsShowing = False
        self.redraw()

    def writeRecords(self) :
        calculatedScore = (len(self.masterSequence) - self.patternAdditions)//self.patternAdditions
        try :
            with open("ssrecords.pickle","rb") as recordsFile :
                recordsList = list(pickle.load(recordsFile))
                recordsList.append((calculatedScore,
                                    Blinken.difficultyNames[self.patternAdditions]))
        except (FileNotFoundError,EOFError):
            recordsList = [(calculatedScore,
                            Blinken.difficultyNames[self.patternAdditions])]

        with open("ssrecords.pickle","wb") as recordsFile :
            recordsList.sort(reverse=True)
            recordsList = sorted(recordsList,key=lambda r: r[1])
            pickle.dump(recordsList,recordsFile)

    def updateRecords(self) :
        self.records.clear()
        try :
            with open("ssrecords.pickle","rb") as recordsFile :
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
        Popen(["paplay",Blinken.soundEffects[sound]]) # cleaner and more readable than typing this a bunch

    def gameOver(self,timedOut=True) :
        self.playSound(4)
        self.currentScore.labelfont(FL_HELVETICA_BOLD)
        self.removeAllTimeouts()
        for but in self.buttons :
            but.value(0)
        if timedOut is True :
            fl_message("Game Over\nTime's Up")
        else :
            fl_message("Game Over")
        self.writeRecords()
        self.updateRecords()
        self.masterSequence = []
        self.userSequence = []
        self.sequenceStarted = False

    def removeAllTimeouts(self) :
        for but in range(len(self.buttons)) :
            self.buttons[but].color(self.buttonColors[but+4])
        Fl.remove_timeout(self.gameOver)
        Fl.remove_timeout(self.flashButton)
        Fl.remove_timeout(self.simpleCountdown)
        self.countdown.label(None)
        self.redraw()


simonsays = Blinken(title="Simon Says")
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
