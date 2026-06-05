#import numpy as np
#a = np.array([2]*()
#print(a)
#row = 9
#col = 9
#proximity = -row
#print(proximity + col)
#proximity = {-row-1, -row, -row+1, -1, 1, row-1, row, row+1}
#print(proximity)
#print(9 % rowd
#for p in (1,2,4,6,7) :
#    print(p)
#if 9 % (row-1) == 1 :
#    print("yoyoyo")
#l = np.array([2]*81)
#print(l.reshape(9,9))
from fltk import *
win = Fl_Window(400, 300, "Best Times")
tabs = Fl_Tabs(10, 10, 380, 240)

# Beginner tab
beginner = Fl_Group(10, 35, 380, 215, "Beginner")
browser1 = Fl_Hold_Browser(20, 50, 360, 180)
beginner.end()

# Intermediate tab
intermediate = Fl_Group(10, 35, 380, 215, "Intermediate")
browser2 = Fl_Hold_Browser(20, 50, 360, 180)
intermediate.end()

# Expert tab
expert = Fl_Group(10, 35, 380, 215, "Expert")
browser3 = Fl_Hold_Browser(20, 50, 360, 180)
expert.end()

tabs.end()

close_btn = Fl_Button(160, 260, 80, 30, "Close")
close_btn.callback(lambda n: win.hide())

win.end()
win.show()
Fl.run()
