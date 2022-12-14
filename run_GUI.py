# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 18:58:45 2022
@author: jkhou
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from MoMpy import Uncertainty as unc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from MoMpy import Webscraper as web
import sympy as sym

    
    
def findvalue():
    '''Find the values selected in gui
    Args:
        Listbox selection area, mass, volume
    Returns:
        Values selected in listbox
    '''
    file = str(filedialog.askopenfilename())#select the name of the file that you want
    labeler=[] 
    x=0
    def deletebutton():
        '''Deletes selected value
        Args: 
            Button
        Returns: 
            Clears values from gui
        '''
        for i, label in list(enumerate(labeler)):
            label.destroy()#clears values from gui that were selected before
            delete.destroy()#clers the button that says delete
        
    for index in listbox.curselection():
        labeler+=[tk.Label(tab1, text='The value of '+ properties[index] + ' is ' + 
          str(unc.getStressStrain(file, float(area.get()), float(mass.get()),
                                  float(volume.get()))[index]))]#creates a list of all the properties that were selected
        labeler[x].pack()
        x+=1
    delete=tk.Button(tab1, text='delete', command=deletebutton)#adds delete button to gui
    delete.pack(anchor=tk.S)
    
        
def graphtime():
    '''Creates a stress strain graph 
    Args:
        Area
    Returns:
        Graph image in a new window
    
    '''
    graphwindow = tk.Tk()#creates window
    file = str(filedialog.askopenfilename())#select the file to graph
    values = unc.getStressStrain(file, float(area.get()))#creates a list of all the calyes returned my function

    fig  =  Figure(figsize = (15,15), dpi = 100)#creates the figure
    graphwindow.geometry('550x550')#creates the size of the window
    graphwindow.title("Stress vs Strain")#creates the title of the window
    graph = fig.add_subplot(111)#creates the graph
    
    graph.plot(values[6], values[5], 'm')#graphs the stress strain curve
    graph.plot(values [7], values[1], 'rx', label = "Yield Strength %f MPa" % values[1])#plots the Yield strength
    graph.plot(values[10], values[4], 'bo', label = "Ultimate Strength %f MPa" % values[4])#plots the ultimate strength
    graph.plot(values[9], values[8], 'ko', label = "Breaking Strength %f MPa" % values[8])#plots the breaking strength
    
    graph.grid()
    graph.set_xlabel("Strain")
    graph.set_ylabel("Stress")
    graph.legend();
    
    #draw the graph in the new window                                                                    
    canvas = FigureCanvasTkAgg(fig, graphwindow)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    
def theRSS():
    '''Shows the Root Sum Squared expression and creates a window to enter RSS values
    Args:
        Expression of the equaion
    Returns:
        RSS
    '''
    symbols  = list(sym.sympify(eq.get()).free_symbols)#creates a list of symbols
    U_symbol = []#starts a list of Uncertainty symbols
    
    for i, symbol in enumerate(symbols):#for each symbol adds an uncertainty symbol  

        U_symbol +=  ["U_"+str(symbol)]
        
        symbols[i] = str(symbol)
        
    rsslabel = tk.Label(tab2, text = unc.get_RSS(eq.get()))#creates space to enter expression
    rsslabel.pack()
    rsswindow  =  tk.Tk()
    entry  =  []
    newsymbols = symbols+U_symbol#creates a list of all the values required
    def rssvalue():
        '''
        Args:
            Values for prompted symbols
        Returns:
            Final value for the RSS
        '''
        entries = []#creates a list of entries
        
        
        for i in entry:
            entries += [float(i.get())]#adds the values for the symbols inputted
            
        kwargs = dict(zip(newsymbols, entries))#creates a dictionary with the symbols and the values
        label16 = tk.Label(rsswindow, text =  str(unc.get_RSS(eq.get(), **kwargs, evaluate = True)))#displays rss value
        label16.pack()
            
    for i, symbol in enumerate(newsymbols):
        label15 = tk.Label(rsswindow, text = "Enter value for " + str(symbol))#creates label indicating which values to input
        label15.pack()
        entry += [tk.Entry(rsswindow)]#adds spaces to enter the values
        entry[i].pack()
        
    submit6 = tk.Button(rsswindow, text = 'Submit', command = rssvalue)#submit button
    submit6.pack()
                         
    
def theMC():
    '''Monte Carlo simulation
    Args:
        x-values and x-uncertainties
        y-values and y uncertainties
    Returns:
        Slope with a 95% CI
    '''
    #creates floats of all the values inputed in the GUI
    x_1 = float(x1.get())
    x_2 = float(x2.get())
    x_3 = float(x3.get())
    x_4= float(x4.get())
    x_5 = float(x5.get())
    Ux_1 = float(U_x1.get())
    Ux_2 = float(U_x2.get())
    Ux_3 = float(U_x3.get())
    Ux_4 = float(U_x4.get())
    Ux_5 = float(U_x5.get())
    y_1 = float(y1.get())
    y_2 = float(y2.get())
    y_3 = float(y3.get())
    y_4 = float(y4.get())
    y_5 = float(y5.get())
    Uy_1 = float(U_y1.get())
    Uy_2 = float(U_y2.get())
    Uy_3 = float(U_y3.get())
    Uy_4 = float(U_y4.get())
    Uy_5 = float(U_y5.get())
    x, y = unc.getMonteCarlo((x_1,x_2,x_3,x_4, x_5), (y_1,y_2,y_3,y_4, y_5), 
                      (Ux_1, Ux_2, Ux_3, Ux_4, Ux_5), (Uy_1, Uy_2, Uy_3, Uy_4, Uy_5), slope = True)#Monte Carlo simulation
    label=tk.Label(tab3, text='The slope is ' + str(x)+' with a 95% confidence interval of ' + str(y))
    label.pack(anchor=tk.S)
    
    
def Scrape():
    if (material.get() == 0):
        materialwindow = tk.Tk()
        x  =  web.Get_MatE(float(thevalue.get()))
        for index, row in x.iterrows():
            mylist  =  [row["Material"], row["Youngs Modulus (GPa)"]]
            label14 = tk.Label(materialwindow, text = "The material is " + str(mylist[0]) + "with a Youngs Modulus of "  + 
                             str(mylist[1])+ " GPa")
            label14.pack()   
    elif (material.get() == 1):
        materialwindow = tk.Tk()
        x  =  web.Get_MatU(float(thevalue.get()))
        for index, row in x.iterrows():
            mylist  =  [row["Material"], row["Ultimate Tensile Strength (MPa)"]]
            label14 = tk.Label(materialwindow, text = "The material is " + 
                               str(mylist[0]) + "with a Ultimate Tensile Strength of "  + 
                             str(mylist[1])+ " MPa")
            label14.pack()
    elif (material.get() == 2):
        materialwindow = tk.Tk()
        x  =  web.Get_MatY(float(thevalue.get()))
        for index, row in x.iterrows():
            mylist  =  [row["Material"], row["Yield Strength (MPa)"]]
            label14 = tk.Label(materialwindow, text = "The material is " + 
                               str(mylist[0]) + "with a Yield Strength of "  + 
                             str(mylist[1])+ " MPa")
            label14.pack()  
    else:
        raise ValueError("Please select the value you are entering")
        
        
def matprop():
    x=web.Get_Prop(matname.get())
    for index, row in x.iterrows():
        mylist  =  [row["Material"], row["Yield Strength (MPa)"],
                    row["Ultimate Tensile Strength (MPa)"],  
                    row["Yield Strength (MPa)"]]
        label14 = tk.Label(tab4, text = "The material is " + str(mylist[0]) +
                           "\n with a Yield Strength of "  + 
                         str(mylist[1]) + " MPa \nand a Ultimate Tensile Strength of "  + 
                       str(mylist[2])+ " MPa and a Yield Strength of "  + 
                     str(mylist[3])+ " MPa")
    label14.pack()
    
           
#properties for Stress Strain Analysis   
properties = ['Youngs Modulus', 'Yield Strength', 'Specific Stiffness',
            'Specific Strength', 'Ultimate Tensile Strength']
#Properties to find material
moreprops = ['Youngs Modulus', 'Ultimate Tensile Strength', 'Yield Strength']

#create the window
root = tk.Tk()


root.geometry("600x700")
root.title("MoMpy")
notebook = ttk.Notebook(root)

#Create Frame instances of different tabs
tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)
tab3 = tk.Frame(notebook)
tab4 = tk.Frame(notebook)


#add names to the different tabs
notebook.add(tab1, text = "Stress")
notebook.add(tab2, text = "RSS")
notebook.add(tab3, text = "MonteCarlo")
notebook.add(tab4, text = "Webscraping")
notebook.pack(expand = True, fill = 'both')

#tab1 contents
label2 = tk.Label(tab1, text = "Enter the area of the specimen in mm\u00b2", font = 12)
label2.pack(anchor = tk.W, pady = 10)

area = tk.Entry(tab1, font = 10)
area.pack(anchor = tk.W, padx = 5, pady = 5)

label3 = tk.Label(tab1, text = "Enter the mass of the specimen", font = 12)
label3.pack(anchor = tk.W, pady = 10)

mass = tk.Entry(tab1, font = 10)
mass.pack(anchor = tk.W, padx = 5, pady = 5)

label4 = tk.Label(tab1, text = "Enter the volume of the specimen", font = 12)
label4.pack(anchor = tk.W, pady = 10)

volume = tk.Entry(tab1, font = 10)
volume.pack(anchor = tk.W, padx = 5, pady = 5)


label5 = tk.Label(tab1, text = "Select wanted Value", font = 10)
label5.pack(anchor = tk.W, pady = 20)

listbox = tk.Listbox(tab1,font = 10, selectmode = tk.MULTIPLE)
listbox.pack(anchor = tk.W)

for i in range(len(properties)):
    listbox.insert(i+1, properties[i])
    
listbox.config(height = listbox.size())

submit1 = tk.Button(tab1, text = 'Enter', command = findvalue)
submit1.pack(anchor = tk.W)

graphbutton = tk.Button(tab1, text = "Press for graph", command = graphtime)
graphbutton.pack(anchor = tk.S, pady = 50)

#tab2 contents
label6 = tk.Label(tab2, text = "Enter the equation", font = 10)
label6.pack(anchor = tk.W)

eq = tk.Entry(tab2, font = 10)
eq.pack(anchor = tk.W)

submit2 = tk.Button(tab2, text = 'submit', command = theRSS)
submit2.pack(anchor = tk.E)

#tab3 contents
label7 = tk.Label(tab3, text = "Monete Carlo Simulation", font = ("Arial",25, 'bold'))
label7.pack(anchor = tk.N)

label8 = tk.Label(tab3, text = 'Enter x values')
label8.pack(anchor = tk.W)

x1 = tk.Entry(tab3, font = 10)
x1.pack(anchor = tk.W)

x2 = tk.Entry(tab3, font = 10)
x2.pack(anchor = tk.W)

x3 = tk.Entry(tab3, font = 10)
x3.pack(anchor = tk.W)

x4 = tk.Entry(tab3, font = 10)
x4.pack(anchor = tk.W)

x5 = tk.Entry(tab3, font = 10)
x5.pack(anchor = tk.W)

label9 = tk.Label(tab3, text = 'Enter x Uncertainties')
label9.pack(anchor = tk.W)

U_x1 = tk.Entry(tab3, font = 10)
U_x1.pack(anchor = tk.W)

U_x2 = tk.Entry(tab3, font = 10)
U_x2.pack(anchor = tk.W)

U_x3 = tk.Entry(tab3, font = 10)
U_x3.pack(anchor = tk.W)

U_x4 = tk.Entry(tab3, font = 10)
U_x4.pack(anchor = tk.W)

U_x5 = tk.Entry(tab3, font = 10)
U_x5.pack(anchor = tk.W)


label10 = tk.Label(tab3, text = 'Enter y values')
label10.place(x = 400, y = 48)

y1 = tk.Entry(tab3, font = 10)
y1.place(x = 400, y = 70)

y2 = tk.Entry(tab3, font = 10)
y2.place(x = 400, y = 92)

y3 = tk.Entry(tab3, font = 10)
y3.place(x = 400, y = 114)

y4 = tk.Entry(tab3, font = 10)
y4.place(x = 400, y = 136)

y5 = tk.Entry(tab3, font = 10)
y5.place(x = 400, y = 158)

label11 = tk.Label(tab3, text = 'Enter y Uncertainties')
label11.place(x = 400, y = 180)

U_y1 = tk.Entry(tab3, font = 10)
U_y1.place(x = 400, y = 202)

U_y2 = tk.Entry(tab3, font = 10)
U_y2.place(x = 400, y = 224)

U_y3 = tk.Entry(tab3, font = 10)
U_y3.place(x = 400, y = 246)

U_y4 = tk.Entry(tab3, font = 10)
U_y4.place(x = 400, y = 268)

U_y5 = tk.Entry(tab3, font = 10)
U_y5.place(x = 400, y = 290)

submit3 = tk.Button(tab3, text = 'Submit', command = theMC)
submit3.pack()

#tab4 contents
label12 = tk.Label(tab4, text = "Find material", font = ('Arial', 25, 'bold'))
label12.pack(anchor = tk.N)

material = tk.IntVar()

for i in range(len(moreprops)):#creates buttons based on the available properties
    radiobutton = tk.Radiobutton(tab4,text = moreprops[i], variable = material, value = i)
    radiobutton.pack(anchor = tk.W)
    
thevalue = tk.Entry(tab4, font = 10)
thevalue.pack(anchor = tk.W)

submit4 = tk.Button(tab4, text = 'Submit', command = Scrape)
submit4.pack(anchor = tk.W)

label13 = tk.Label(tab4, text = "Enter the material name", font = ('arial', 20, 'bold'))
label13.pack()

matname = tk.Entry(tab4, font = 10)
matname.pack(anchor = tk.W)

submit5 = tk.Button(tab4, text = 'Submit', command = matprop)
submit5.pack(anchor = tk.W)



root.mainloop()