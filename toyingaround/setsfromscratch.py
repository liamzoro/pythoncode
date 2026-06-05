def makeSet(lst,idx=0,n=1) :
    dupes = []
    nlst = lst[idx+1:]
    for i in range(len(nlst)) :
        if nlst[i] == lst[idx] :
            dupes.append(i+n)
    for d in range(len(dupes)-1,-1,-1) :
        lst.pop(dupes[d])
    if idx < len(lst)-1 :
        makeSet(lst,idx+1,idx+2)
    else :
        lst.sort()

myList = [1,1,1,2,2,3,6,6,6,7,8,8,8,8,3,3,3,4,4,4,5,8]

print(myList)
makeSet(myList)
print(myList)
