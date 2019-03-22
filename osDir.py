#!use/bin/env python3
# -*- coding utf-8 -*-

resultArr = []

def lAndllAdd():
    maxValue=10000000000000
    lValue=1
    llValue=1
    print(llValue)

    while lValue<maxValue:
        print(lValue)
        tempV=llValue
        llValue=lValue
        lValue=llValue+tempV

def theContents(targetValue):
    state = True
    if len(resultArr)==0:
        state = True
    else:
        for temp in resultArr:
            if targetValue % temp == 0:
                state = False
                break
    if state:
        resultArr.append(targetValue)
    return state

def GetSingle():
    mylist = range(2, 10000000)
    #mylist = list(range(2,10000000000000))
    #mylist=[2,3,4,5,6,7,8,9,10,11,12,13,14,15]

    arr=list(filter(theContents,mylist))

def by_name(t):
    return str.lower(t[0])

def TestSort1():
    L = [('bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
    result=sorted(L,key=by_name)
    print(result)

def by_score(t):
    return t[1]

def TestSort2():
    L = [('bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
    result=sorted(L,key=by_score)
    print(result)

result=int('1000000',base=32)
print(result)
