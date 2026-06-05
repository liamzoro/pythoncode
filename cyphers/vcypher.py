import sys

    ## functions

def pre1(x="ENTER MESSAGE :",y="ENTER PASSWORD :") :
    global msg,pss
    msg = input(x).lower().replace(" ","")
    pss = input(y).lower().replace(" ","")
    pss = pss*(len(msg)//len([pss])+1)

def pre2() :
    global msg,pss
    msg = f1.read().lower().replace(" ","")
    pss = sys.argv[4].lower().replace(" ","")
    pss = pss*(len(msg)//len([pss])+1)


    ## variables

mp = list("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
abc = list("abcdefghijklmnopqrstuvwxyz")
cc = []
result = ""
msg = ""
pss = ""


    ## code

if __name__ == "__main__" :


    ## with file io

    if len(sys.argv) == 5 :

        with open(sys.argv[2],"r") as f1 :
            pre2()

    # encryption

        if sys.argv[1].lower() == "e" :

            for let in range(len(msg)) :
                current = mp.index(msg[let])

                for i in range(current,current+26) :
                    cc.append(mp[i])
                
                result += cc[mp.index(pss[let])]
                cc = []

            with open(sys.argv[3],"w") as f2 :
                f2.write(result)
        
    # decryption
        
        elif sys.argv[1].lower() == "d" :

            for let in range(len(msg)) :
                current = abc.index(pss[let])

                for i in range(26) :
                    firstcc = mp.index(abc[i])

                    for x in range(firstcc,firstcc+26) :
                        cc.append(mp[x])

                    if cc[current] == msg[let] :
                        result += cc[0]
                    
                    cc = []
            
            with open(sys.argv[3],"w") as f2 :
                f2.write(result)
        

    ## in terminal

    else :

    # encryption

        if sys.argv[1].lower() == "e" :

            pre1("ENTER MESSAGE FOR ENCRYPTION :","ENTER PASSWORD FOR ENCRYPTION :")

            for let in range(len(msg)) :
                current = mp.index(msg[let])

                for i in range(current,current+26) :
                    cc.append(mp[i])
                
                result += cc[mp.index(pss[let])]
                cc = []

    # decryption

        elif sys.argv[1].lower() == "d" :
            
            pre1("ENTER CODE FOR DECRYPTION :","ENTER PASSWORD FOR DECRYPTION :")

            for let in range(len(msg)) :
                current = abc.index(pss[let])

                for i in range(26) :
                    firstcc = mp.index(abc[i])

                    for x in range(firstcc,firstcc+26) :
                        cc.append(mp[x])

                    if cc[current] == msg[let] :
                        result += cc[0]
                    
                    cc = []

        print(result)
