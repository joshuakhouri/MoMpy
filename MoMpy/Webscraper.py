# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:50:30 2022

@author: jkhou
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from IPython.display import display
import math

url = requests.get("https://www.engineeringtoolbox.com/young-modulus-d_417.html")
soup = BeautifulSoup(url.text, "html.parser")

table1 = soup.find('table', id = 'tablesorter')

headers = []
for i in table1.find_all('th'):
 title = i.text
 headers.append(title)
    
mydata = pd.DataFrame(columns = headers)

for j in table1.find_all('tr')[1:]:
 row_data = j.find_all('td')
 row = [i.text for i in row_data]
 length = len(mydata)
 mydata.loc[length] = row

    
mydata = mydata.rename(columns={"Tensile Modulus(Young's Modulus, Modulus of Elasticity) - E -(GPa)": "Youngs Modulus (GPa)", 
                       "Ultimate Tensile Strength - σu - (MPa)": "Ultimate Tensile Strength (MPa)", 
                       "Yield Strength - σy - (MPa)":"Yield Strength (MPa)"})

def Get_MatE(value):
    """ Obtain Material name from Youngs Modulus
    Args:
        Integer value (in GPa).
        
    Returns:
        DataFrame of potential materials and other associated properties with that material.
    """
    
    
    lower = math.trunc(value - (value*.1))
    upper = math.trunc(value + (value*.1))
    i = np.arange(lower, upper, 1)
    df=pd.DataFrame()
    
    for x in i:
        t = mydata.loc[mydata["Youngs Modulus (GPa)"]== str(x)]
        if t.empty:
            pass
        else:
            df = pd.concat([df, t], ignore_index = True)
    return df   

def Get_MatU(value):
    """ Obtain Material name from Ultimate Tensile Strength
    Args:
        Integer value (in MPa).
        
    Returns:
        DataFrame of potential materials and other associated properties with that material.
    """    
    lower = math.trunc(value - (value*.1))
    upper = math.trunc(value + (value*.1))
    i = np.arange(lower, upper, 1)
    df = pd.DataFrame()
    for x in i:
        t = mydata.loc[mydata["Ultimate Tensile Strength (MPa)"]== str(x)]
        if t.empty:
            pass
        else:
            df = pd.concat([df, t], ignore_index = True)
    return df
            
def Get_MatY(value):
    """ Obtain Material name from Yield Strength
    Args:
        Integer value (in MPa).
        
    Returns:
        DataFrame of potential materials and other associated properties with that material.
    """ 
    lower = math.trunc(value - (value*.1))
    upper = math.trunc(value + (value*.1))
    i = np.arange(lower, upper, 1)
    df=pd.DataFrame()
    for x in i:
        t = mydata.loc[mydata["Yield Strength (MPa)"]== str(x)]
        if t.empty:
            pass
        else:
            df = pd.concat([df, t], ignore_index = True)
    return df
            
def Get_Prop(mat):
    """ Obtain Material name from Ultimate Tensile Strength
    Args:
        string: Name of material
        
    Returns:
        DataFrame of that material's properties.
    """ 
    k = mydata.loc[mydata['Material']== mat]
    df=pd.DataFrame()
    if k.empty:
        print('Please check the spelling of the material')
    else:
        df = pd.concat([df, k], ignore_index = True)
    return df
            
