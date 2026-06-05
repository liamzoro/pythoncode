def chrcnt(file=False,islet=True,isnum=True,isspace=True,isspecial=True) :

    abc = list("\n 0123456789abcdefghijklmnopqrstuvwxyz")

    leftovers = ""
    count = 0

    if file :
        with open(file,"r") as f :
            characters = f.read().lower()
    else :
        characters = input().lower()

    if not islet :
        leftovers += "".join(abc[12:])
        abc = abc[:12]
        

    for char in range(len(abc)-1,-1,-1) :
        if not isnum and abc[char] in "0123456789" :
            leftovers += abc.pop(char)

    if not isspace :
        leftovers += " "
        abc.remove(" ")

    for i in characters :
        if isspecial :
            count += 1 if i not in leftovers else 0
        else :
            count += 1 if i in abc else 0

    for x in characters :
        count -= 1 if x == abc[0] else 0

    return count

print(chrcnt())