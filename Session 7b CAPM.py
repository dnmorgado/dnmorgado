

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 18:51:21 2021


FOR ISEG MASTER IN FINANCE 2020/2021 EDUCATIONAL PURPOSE ONLY
working file

@author: fcald
"""
"""IMPORTING DATA"""

""" from CSV file"""

import pandas as pd 
import os 

path=os.getcwd() 

shell=pd.read_csv("RDSA.AS.csv")   
total=pd.read_csv("FP.PA.csv")  
stoxx=pd.read_csv("^STOXX.csv")  #importing stoxx600 daily stock price data - as market proxy for CAPM model
shell.index=shell['Date'] 
shell.index=pd.to_datetime(shell.index) 
total.index=total['Date'] 
total.index=pd.to_datetime(total.index) 
stoxx.index=stoxx['Date'] 
stoxx.index=pd.to_datetime(stoxx.index)
shell=shell[(shell.index > '2009-01-02')] 
frames=[shell['Close'],total['Close'],stoxx['Close']]
columns=['Shell C Price','Total C Price','Stoxx C Price']
stockprices=pd.concat(frames,axis=1,sort=False)
stockprices.columns=columns
stockprices=stockprices[(stockprices.index > '2009-01-02')]
stockprices=stockprices[(stockprices.index < '2021-04-01')]
drets=pd.DataFrame(index=stockprices.index,columns=stockprices.columns) #creating a new Dataframe with same index and same columns titles
import numpy as np 
drets=np.log(stockprices/stockprices.shift(1)) #daily retunrs






#OLS - linear regression - computing Total and Shell stock Beta - using daily returns and Stoxx 600 as market proxy

import statsmodels.api as sm
from statsmodels.api import add_constant

drets=drets.replace(np.nan,0) #replacing nan values with 0 on all drets dataframe

X=drets['Stoxx C Price'] 
T=drets['Total C Price']
X= sm.add_constant(X)
S=drets['Shell C Price']


res1 = sm.OLS(T,X).fit()
TotalBeta=res1.params.iloc[1]

res2 = sm.OLS(S,X).fit()
ShellBeta=res2.params.iloc[1]

print('Shell Stock Beta = ',ShellBeta)
print('Total Stock Beta = ',TotalBeta)

print('Press Any Key to see OLS summary ')
input()

print(res1.summary())
print('Press Any Key to see OLS summary ')
input()
print(res2.summary())