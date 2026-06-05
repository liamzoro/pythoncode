def wrdcnt(file=False,allownum=False,allowspecial=False,specialspace=False) :
    abc = list("0123456789abcdefghijklmnopqrstuvwxyz")
    count = 0
    yn = False

    if file :
        with open(file,"r") as f :
            string = f.read().lower()
    else :
        string = input().lower()

    string = string.split()
    length = len(string)-1

    if allownum :
        count = len(string)
    else :
        for i in range(len(string)-1,-1,-1) :
            for x in range(len(string[i])) :
                if length != len(string) :

                    if string[i][x] in abc[:10] :
                        string.pop(i)

            length = len(string)-1

    if not allowspecial and not specialspace:
        for i in range(len(string)-1,-1,-1) :
            for x in range(len(string[i])-1,-1,-1) :
                if length != len(string) :
                    
                    if string[i][x] not in abc :
                        yn = True
                        newsplit = string.pop(i)
                        newsplit = list(newsplit)
                        for x in range(len(newsplit)-1,-1,-1) :
                            if newsplit[x] not in abc :
                                newsplit.pop(x)
            if yn :
                if newsplit != [] : string.append("".join(newsplit)) 
                yn = False

            length = len(string)-1
    elif not allowspecial and specialspace :
        for i in range(len(string)-1,-1,-1) :
            for x in range(len(string[i])-1,-1,-1) :
                if length != len(string) :
                    
                    if string[i][x] not in abc :
                        newsplit = string.pop(i)
                        newsplit.replace(newsplit[x]," ")
                        string.append(newsplit)

        count = len(string)
    
    return count,string

