import sys

if len(sys.argv) == 3 :
    s1 = sys.argv[1]
    s2 = sys.argv[2]
else :
    s1 = input("INPUT FIRST STRING TO COMPARE :")
    s2 = input("INPUT SECOND STRING TO COMPARE :")

print("THEY ARE THE SAME" if s1 == s2 else "THEY ARE DIFFERENT")

bobo = ""
if len(s1) > len(s2) :
    for i in range(len(s2)) :
        if s1[i] == s2[i] :
            bobo += s2[i]
        else :
            bobo += " "
    print(bobo)
elif len(s1) < len(s2) :
    for i in range(len(s1)) :
        if s1[i] == s2[i] :
            bobo += s1[i]
        else :
            bobo += " "
