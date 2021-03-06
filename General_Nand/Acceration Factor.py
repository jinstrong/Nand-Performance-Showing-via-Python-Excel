#!/usr/bin/env python
'''
This API is intended to calculate the activation energy based on Arrhenius Equation

 Feb 5, 2015 Jinqiang He 
'''
import math

Ea=1.1 # by default, we use this value for all Nand flash devices to get spec of data retention 
ka=8.62*math.pow(10,-5)
h1=3. # please give the number of months for the spec given in original temperature
hr=h1*30*24
h2=-1       # the spec to be calculated
t1=40.        # original temperature
t2=85       # the actual temperature used
tt=273.
h2=hr* math.exp(-(1/(t1+tt)-1/(t2+tt))*Ea/ka)
print "Original spec is : ",h1," months @ ",t1," Degree"
print "The calculated spec is: " , h2," hours @ ",t2," Degree"