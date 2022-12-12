# -*- coding: utf-8 -*-
"""

@author: Israel

Purpose: Several high level functions that can calculate uncertainties either with calculus or with statistical methods. Also consists of functions to analyze UTM data. It was going to include functions for other labs but I did not see how they could work with other modules, so they seemed irrelevant. Thus, the main focus of this module is uncertainty analysis.

"""
import numpy as np
import scipy as sp
import sympy as sym
from scipy.stats import norm
import random
import pandas as pd

import warnings
warnings.filterwarnings("ignore") #lin regression gives runtime errors on occasion. 

def get_RSS(expr, evaluate = False, unicode = False, excel = False, **kwargs):

    """
    Returns the Root Sum Square uncertainty of an algebraic expression. User has the option to make it compatible with Microsoft's unicode,
    Microsoft's excel syntax, or evaluate the expression. 
    
    Parameters:
    
        expr: sympy_object, string
              a syntatically correct algebraic equation.
        evaluate: bool, optional
            determines if the RSS will be evaluated, requires keyword arguments.
        unicode: bool, optional
            makes it compatible with microsoft word unicode
        excel: bool, optional
            makes it compatible with MATLAB or excel
        kwargs: dict, optional
            If the user wishes to evaluate, they must provide either a dictionary or keyword inputs containting each variable and
            another variable of the name U_ + variable and their corresponding values.
            
    Returns:
        
        An algebraic expression if evaluate = False. If excel or unicode, it returns a string. If evaluate, it returns a float.
    """
    
    if isinstance(expr,str): #checks if the expression is a string, converts to sympy expr if it is
        expr = sym.sympify(expr)
        
    rss = 0 #RSS expression
    symbols = list(expr.free_symbols) #this method takes all of the variables in a sympy expression and puts them in a set.
    U_symbol = [] #list of uncertainty variable symbols
    U_sub = [] #corresponding values for the list above
    symbol_sub = [] #list of values that correspond to symbols respective values
    
            
    for i, symbol in enumerate(symbols):
                
        U_symbol += ["U_"+str(symbol)] #for every symbol in the expression, there will be a corresponding uncertainty symbol
        U_symbol[i] = sym.symbols(U_symbol[i]) #symbolizes the previous line
        
        if evaluate and str(symbol) not in kwargs: #checks if there is any missing value provided in kwargs
            raise ValueError(f"Symbol {symbol} value MUST be provided")
        elif evaluate and str(U_symbol[i]) not in kwargs:
            raise ValueError(f"Uncertainty {U_symbol[i]} value MUST be provided.")
        
        for j in kwargs: #loops through kwargs to check if the symbols match the any kwargs 
            if str(symbol) == j:
                symbol_sub += [kwargs[j]]#if they do match the corresponding subs list gets the variable at the same index as symbol
            elif str(U_symbol[i]) == j:
                U_sub += [kwargs[j]]               

        rss +=  sym.diff(expr,symbol)**2*U_symbol[i]**2 #RSS formula, not square rooted yet

    if (excel and evaluate) or (unicode and evaluate): #can't do both :P
        raise ValueError("Cannot use evaluate and unicode/excel simultaneously")
        
    elif evaluate:
        
        for i,symbol in enumerate(symbols): #evaluating the RSS expression with the substituted values
            rss_evaluated = rss.subs([(symbol,symbol_sub[i]),(U_symbol[i],U_sub[i])])
            rss = rss_evaluated
        result = float(sym.nsimplify(sym.sqrt(rss_evaluated)).evalf())
        
    elif unicode and not evaluate:
        result = str(sym.sqrt(rss))
        result = result.replace("**","^").replace("*"," \times ") #a minor convenience for me personally.
        
    elif excel and not evaluate: #a minor convenience for me personally
        result = str(sym.sqrt(rss))
        result = result.replace("**","^")
    
           
    else:
        result = sym.sqrt(rss)
        
    return result


def getMonteCarlo(x, y, U_x, U_y, num_sims = 4000, slope = False, integral = False):
    
    """
    Calculates uncertainty of a linear regression or numerical integration using the Monte Carlo method (buncha random simulations).
    
    Parameters: 
        x: list or numpy array
            no matter the type the code will reshape it to the desired configuration
        y: list or numpy array
            no matter the type the code will reshape it to the desired configuration
        U_x: list or numpy array
            x uncertainty. no matter the type the code will reshape it to the desired configuration
        U_y: list or numpy array 
            y uncertainty. no matter the type the code will reshape it to the desired configuration
        num_sims: int
            determines number of simulations
        slope: bool
            if chosen the function will return a linear regression and its respective uncertainty.
        integral: bool
            if chosen the function will return a numerical integral (simpsons rule) and its respective uncertainty.
        
    Returns:
            the average result of the desired calculation from the simulations and its uncertainty.      
    """
    
    if len(x) != len(y) and len(x) != len(U_x) and len(y) != len(U_y):
        raise ValueError("Array lengths must be equal length.")
    
    slopes = []
    integrals = []
    
    x = np.array(x)[None:] #reshapes inputs to be 1D numpy row vectors
    U_x = np.array(U_x)[None:]
    y = np.array(y)[None:]
    U_y = np.array(U_y)[None:]
    
    if not(slope) and not(integral):
        raise ValueError("Must make either slope or integral True.")
    elif slope and integral:
        raise ValueError("Cannot have both integral and slope True.")
        
    if slope: 
        for j in range(num_sims):
                #calculates alternative values for x and y using the inverse cumulative distribution function
                #where the probabiltiy is random, the mean is the data points, and the uncertainty is assumed to be two STDEVS.
                x_mc = norm.ppf(random.uniform(0,1), loc = x, scale = U_x/2) 
                y_mc = norm.ppf(random.uniform(0,1), loc = y, scale = U_y/2)
                slopes += [sp.stats.linregress(x_mc,y_mc)[0]] #creating a list of slopes for each simulation
        avg = np.mean(slopes)
        CI = 1.95*np.std(slopes) #95% confidence interval assuming an infinite set
        
    if integral: 
        for j in range(num_sims): #similar to above except for an integral
                x_mc = norm.ppf(random.uniform(0,1), loc = x, scale = U_x/2)
                y_mc = norm.ppf(random.uniform(0,1), loc = y, scale = U_y/2)
                integrals += [sp.integrate.simpson(y_mc, x_mc)]
        avg = np.mean(integrals)
        CI = 1.95*np.std(integrals) #95% CI for infinite set
    
    return(avg, CI)


def getStressStrain(filename, area, mass = 1, volume = 1, MC_sim = False):
    
    """
    Takes data from a UTM and generates stress, strain, and various material properties.
    
    Parameters: 
        filename: str, csv file. 
        area: float
            cross sectional area of testing specimen
        mass: float
            used to calculate any specific properties
        volume: float
            used to calculate various material properties
        MC_sim: bool, optional
            If the user wants uncertainty in the modulus of elasticty, making this true will make it a returned value.
    Returns:
      a dataframe column of stress values, a dataframe column of strain values, modulus of elasticity, uncertainty if MC_sim = True, 
      yield strength, yield strain, specific modulus, breaking strength, breaking strain, specific strength, ultimate strength, ultimate
      strain
    """
    
    df = pd.read_csv(filename).dropna(axis = 1).drop(0, axis = 0) #second row usually has units, so it is removed
    row_vals = list(df.iloc[5]) #Pulling a row in the dataframe to ascertain which columns are strain or load.

    load_col = row_vals.index(max(row_vals))
    strain_col = row_vals.index(min(row_vals))
    
    #to prevent errors with the number types when reading the csv, turn the df into np arrays first and forcibly remove errors
    data = df.copy()[pd.to_numeric(df.iloc[:,load_col],errors='coerce') >= 0] #removing all negative loads
    data["strain"] = pd.to_numeric(data.iloc[:,strain_col],errors='coerce') 
    data["stress"] = pd.to_numeric(data.iloc[:,load_col],errors='coerce').div(area)

    e_y = .2/100 #for the .2% yield strength method
    
    data_elastic = data.copy()[data["strain"] <= e_y] #split the data into plastic and elastic
    data_plastic = data.copy()[data["strain"] > e_y]
    
    E = sp.stats.linregress(data_elastic["strain"], data_elastic["stress"])[0]
    
    Sigma_y = data_elastic["stress"].iloc[-1]
    Strain_y = data_elastic["strain"].iloc[-1]
    
    dens = mass/volume #density
    SM = E/dens #specific stiffness
    
    Sigma_b = data["stress"].iloc[-2] #last value of the stress strain curve 
    Strain_b = data["strain"].iloc[data.index[data['stress'] == Sigma_b].tolist()[0]] #corresponding strain by matching index
    
    S = Sigma_b/dens #specific strength   
    
    Sigma_U = data["stress"].max() #finds maximum value
    Strain_U = data["strain"].iloc[data.index[data['stress'] == Sigma_U].tolist()[0]] #corresponding strain by matching index
                    
    
    
    if MC_sim:
        indices = np.round(np.linspace(10,len(data_elastic)-10,5)).astype(int)#takes 5 equally spaced points in elastic region to find slope
        x = [] 
        y = []
        U_x = []
        U_y = []

        for i in indices:
            x += [data_elastic["strain"][i]]
            y += [data_elastic["stress"][i]]
            U_x += [data_elastic["strain"][i]*.5/100] #assumes a .5% uncertainty for load cell and extensometer
            U_y += [data_elastic["stress"][i]*.5/100]


        slope, uncert = getMonteCarlo(x, y ,U_x ,U_y, slope = True) #returns E and uncertainty of E

        return data["stress"], data["strain"], slope/1000, uncert/1000, Sigma_y, Strain_y, SM, Sigma_b, Strain_b, S, Sigma_U, Strain_U
    else:
        return data["stress"], data["strain"], E/1000, Sigma_y, Strain_y, SM, Sigma_b, Strain_b, S, Sigma_U, Strain_U
    
def MonteCarlo(expr, N = 10000,  **kwargs):
    
    """
    Calculates propagated error using the Monte Carlo method, does not work for large uncertainties.
    
    Parameters:
        expr: sympy_object, string
            a syntactically correct algebraic expression
        N: int, optional
            number of Monte Carlo simulations
        kwargs: dict, optional
            user must give the symbols and corresponding values, as well as the uncertainties by giving U_ followed by the var symbol.
            
    Returns:
        the result of the expression and the corresponding uncertainty.
    """
    
    if isinstance(expr,str): #if input is a string, it turns it into a sympy expression
        expr = sym.sympify(expr)

    MC = [] #a list of different rand_data lists
    rand_data = [] # a list that will simulate new expression evaluations using the inverse cdf function where the values
                   # are means, the uncertainties are two STDEVs, and the probability is random
    symbols = expr.free_symbols #creates a list of symbols in a sympy expression
    U_symbol = [] #uncertainty symbols
    U_sub = [] #uncertainty symbol substitution values
    symbol_sub = [] #symbol substitution values

    for i, symbol in enumerate(symbols):
        U_symbol += ["U_"+str(symbol)] #creates a list of uncertainty symbols
        U_symbol[i] = sym.symbols(U_symbol[i])
        
        if str(symbol) not in kwargs:  #checks if there is any missing value provided in kwargs
            raise ValueError(f"Symbol {symbol} value MUST be provided")
        elif str(U_symbol[i]) not in kwargs:
            raise ValueError(f"Uncertainty {U_symbol[i]} value MUST be provided.")

        for j in kwargs:
            if str(symbol) == j:
                symbol_sub += [kwargs[j]]
            elif str(U_symbol[i]) == j:
                U_sub += [kwargs[j]]

    MC_evaluated = sym.lambdify(tuple(symbols), expr, "numpy") #creates a function that evaluates an expression and can take np array inputs

    for i,symbol in enumerate(symbols):
        for j in range(N):
            rand_data += [norm.ppf(random.uniform(0,1), loc = symbol_sub[i], scale = U_sub[i]/2)]
        MC.insert(i, np.array(rand_data)) #creates a list of multiple monte carlo simulations
        rand_data = [] #initializizng to null list again
    
    #the list of simulations are then substituted back into the lambdify function and its standard deviation is used to get uncertainty
    return print(f"{MC_evaluated(*symbol_sub):.5f} +/- {1.95*MC_evaluated(*MC).std()}")

def main():
    
    pass

if __name__ == "__main__":
    main()
