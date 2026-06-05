#non = ["0ligma","2sigma","9origma","1togma",[]]
#non[:-1] = sorted(non[:-1],reverse=True)
#print(non)
#import random
#goo = [(1,"e"),(2,"e"),(1,"n"),(2,"n")]
#for t in range(len(goo)) :
#    if "e" in goo[t] :
#        print("ipkis")
#from os.path import expanduser
#from subprocess import Popen
#pathRecords = expanduser("~/")
#Popen(["paplay",f"{pathRecords}0/CODING/python/cs2/yellow.mp3"])
from fltk import *
def kungfoo(jimjohn=True) :
    jim,john = jimjohn
    print(jim)
    if john is True :
        print("john")
win = Fl_Window(100,100,"eek")
win.begin()
#Fl.add_timeout(1.0,kungfoo,(9,False))
Fl.remove_timeout(kungfoo)
win.end()
win.show()
Fl.run()
