#!/usr/bin/env python

fact = int(input("Enter number to get fact"))

print (fact)

def factor(fact):
    if fact == 1:
    	return fact
    else:
    	return fact*factor(fact-1)


print " Factorial of "+ str(fact) + "is " + str(factor(fact))

