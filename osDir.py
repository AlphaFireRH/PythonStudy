#!use/bin/env python3
# -*- coding utf-8 -*-

maxValue=10000000000000
lValue=1;
llValue=1;

print(llValue)

while lValue<maxValue:
    print(lValue)
    tempV=llValue
    llValue=lValue
    lValue=llValue+tempV

