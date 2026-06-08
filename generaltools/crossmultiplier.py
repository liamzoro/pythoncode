print("'x' must be in the first two. type any letter other than x to end.")
while True :
    x1 = input("Top Left: ")
    if isinstance(x1, str) and x1 != "x" :
        break
    x2 = input("Bottom Left: ")
    if "x" not in (x1, x2) :
        if isinstance(x1, int) and isinstance(x2, int) :
            print("bruh no 'x'")
            continue
        else :
            break
    x3 = input("Top Right: ")
    x4 = input("Bottom Right: ")
    inputs = [x1, x2, x3, x4]
    for i in range(len(inputs)) :
        if inputs[i] != "x" :
            inputs[i] = int(inputs[i])
        else :
            place = i
            cross = 5 - i
    x1, x2, x3, x4 = inputs
    if place == 0 :
        result = (x3/x4)*x2
    elif place == 1 :
        result = (x4/x3)*x1
    print(result, "\n")
