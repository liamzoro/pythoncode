from fltk import *
import random

class Blinken(Fl_Window) :
    
    def __init__(self,width,height,title) :
        super().__init__(width,height,title)
        self.begin()
        self.buttonBackground = Fl_Box(height//8,height//8,width - (height//8)*2,height - (height//8)*2)
        self.buttonBackground.box(FL_UP_BOX)
        self.buttonYellow = Fl_Button(height//8,
                                      height//8,
                                      self.buttonBackground.w()//2,
                                      self.buttonBackground.h()//2)

        self.buttonRed = Fl_Button(height//8 + self.buttonBackground.w()//2,
                                   height//8,
                                   self.buttonBackground.w()//2,
                                   self.buttonBackground.h()//2)

        self.buttonBlue = Fl_Button(height//8,
                                   height//8 + self.buttonBackground.h()//2,
                                   self.buttonBackground.w()//2,
                                   self.buttonBackground.h()//2)

        self.buttonGreen = Fl_Button(height//8 + self.buttonBackground.w()//2,
                                     height//8 + self.buttonBackground.h()//2,
                                     self.buttonBackground.w()//2,
                                     self.buttonBackground.h()//2)
        self.end()

ligma = Blinken(812,256,"LirmaBlinken")
ligma.show()
Fl.run()
