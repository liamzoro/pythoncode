import keyboard
import getpass as hide
import random

def ranum(x=0) :
    rand = random.randrange(0,x+1)
    return rand

blob = "[-_+]"
movement = "    "
pos = "\n\n"
secret = ""
inputs = 0
unknown = ""
truth = ""

print(f"\n\n\n{blob}\n\n")

while True :
    
    fakeout = keyboard.read_key()
    inp = keyboard.read_key()

# up,w

    if inp == "w" and truth != "snipsnip":
        if len(pos) < 4 and truth == "boxer" :
            pos += "\n\n"
            print(f"\n\n\n\n\n{movement}{blob}{pos}")
        
        if "   " in movement and truth == "..." :
            movement = "".join(list(movement)[3:-1])
            print(f"\n\n\n\n\n{movement}{blob}{pos}")

    # default

        if len(pos) < 5 and truth not in ("boxer","...") :
            pos += "\n"
            print(f"\n\n\n\n\n{movement}{blob}{pos}")

# left,a

    elif inp == "a" :
        if "      " in movement and truth == "shy" :
            movement = "".join(list(movement)[6:-1])
            print(f"\n\n\n\n\n{movement}{blob}{pos}")

        elif " " in movement and truth == "snipsnip" :
            movement = "".join(list(movement)[1:-1])
            snipper = blob[0:9]
            dingaling = blob[9:]
            print(f"\n\n\n\n\n{snipper}{movement}{dingaling}\n\n")

        if len(pos) > 0 and truth == "..." :
            pos = "".join(list(pos)[0:-1])
            print(f"\n\n\n\n\n{movement}{blob}{pos}")

    # default

        if "   " in movement and truth not in ("shy","snipsnip","..."):
            movement = "".join(list(movement)[3:-1])
            print(f"\n\n\n\n\n{movement}{blob}{pos}")

# down,s

    elif inp == "s" and truth != "snipsnip":
        if len(pos) > 1 and truth == "boxer" :
            pos = "".join(list(pos)[0:-2])
            print(f"\n\n\n\n\n{movement}{blob}{pos}")

        if len(movement) < 156 and truth == "..." :
            movement += "    "
            print(f"\n\n\n\n\n{movement}{blob}{pos}")

    # default

        if len(pos) > 0 and truth not in ("boxer","...") :
            pos = "".join(list(pos)[0:-1])
            print(f"\n\n\n\n\n{movement}{blob}{pos}")

# right,d

    elif inp == "d" :
        if len(movement) < 138 and truth == "boxer" or truth == "freak" :
            movement += "        "
            print(f"\n\n\n\n\n{movement}{blob}{pos}")

        elif len(movement) < 144 and truth == "snipsnip" :
            movement += "  "
            snipper = blob[0:9]
            dingaling = blob[9:]
            print(f"\n\n\n\n\n{snipper}{movement}{dingaling}\n\n")
        
        if len(pos) < 5 and truth == "..." :
            pos += "\n"
            print(f"\n\n\n\n\n{movement}{blob}{pos}")

    # default

        if len(movement) < 156 and truth not in ("boxer","freak","snipsnip","...") :
            movement += "    "
            print(f"\n\n\n\n\n{movement}{blob}{pos}")

    elif inp == "k" :
        blob = "[#_#]"
        print(f"\n\n\n\n\n{movement}{blob}{pos}")
        truth = ""
        blob = "[-_+]"

    elif inp == "b" :
        blob = "[- _ +]"
        print(f"\n\n\n\n\n{movement}{blob}{pos}")
        truth = ""
        blob = "[-_+]"

    elif inp == "q" :

        break

# codes

    if inp == "]" :
        secret = hide.getpass("enter code :")

        if "=" in secret :
            secret = list(secret)
            ind1 = secret.index("=")
            secret = secret[ind1:]
            secret = "".join(secret)

        if secret == "=shy" : #shy
            blob = '(˶˃_˂˶)'
            truth = "shy"
    
        elif secret == "=shrug" : #shrug
            blob = "¯\(ツ)/¯"
            truth = "shrug"
    
        elif secret == "=freak" : #freak
            blob = "(ˆ𐃷ˆ)"
            truth = "freak"
        
        elif secret == "=boxer" : #boxer
            blob = "(ง'̀-'́)ง"
            truth = "boxer"

        elif secret == "=snipsnip" : #snipsnip
            blob = "( ＾◡＾)っ✂ ╰⋃ ╯"
            truth = "snipsnip"
            movement = ""
        
        elif secret == "=emoji" : #emoji
            blob = "😎"
            truth = "emoji"
    
        elif secret == "=unknown" : #unknown
            blob = ""
            for i in range(6) :
                blob += chr(ranum(5120))
                print(blob)
            truth = "..."
        
        secret = ""
