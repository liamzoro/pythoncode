from fltk import *
def click(wid) :
    print("I'm working y'all")
win = Fl_Window(256,256,"ornald")
win.begin()
but = Fl_Button(64,64,128,128)
but.callback(click)
but.box(FL_NO_BOX)
print(but.visible())
win.end()
win.show()
Fl.visible_focus(0)
Fl.run()
