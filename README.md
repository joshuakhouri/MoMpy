# MoMpy


# Project Description

This package aims to assist students in analyzing their UTM data for Mechanics of Materials lab EML3301C by creating a user-friendly python package. The first module will contain functions to automatically generate a stress strain curve from UTM data and uncertainties using RSS or Monte Carlo simulations. The second module will include a graphical user interface so students can easily navigate the package, create plots, find material properties, or determine the material based on given properties. The last module will involve web scraping as some labs will require students to determine the material based on certain physical properties. Web scraping may also be employed to find uncertainties in some constants. 

## Module 1: Uncertainty - Israel Chinn

Calculate the propagated uncertainty of an algebraic expression given individual variable values and their respective uncertainties. This module is used directly by the GUI to create a user friendly uncertainty calculator, generate a stress strain curve simply by importing a csv file with material dimensions, and creates a monte carlo simulation for linear regressions. 

This is not the main module the user interacts with, but it is designed to be high-level and can be used on its own in a Jupyter notebook/IDE. 

`From MoMpy import Uncertainty
`

Example function:

`
Uncertainty.get_RSS("x/y")
`
>`sqrt(U_x**2/y**4 + 4*U_y**2*x**2/y**6)`

libraries used: numpy, scipy, sympy, pandas, random

## Module 2: Scrape Functions - Conor Hayden

Consists of functions that allows the user to either determine the material properties from a material name, or determine the material based on calculated material properties. This module is also used directly by the GUI by providing the user with an easy way to determine the desired information based on simple inputs. This is all accomplished using web scraping. 

`From MoMpy import Webscraper
`

libraries used: beatifulsoup, requests, pandas

## Module 3: GUI - Joshua Khouri

libraries used: tkinter, matplotlib

This module is the main way the user is expected to interact with the package. It can be run in the command line or in an IDE. All of the user inputs can be typed into the GUI using this package. The GUI consists of four different tabs for the user to use:

**Tab 1**: Stress-Strain diagram/material properties calculator. The user inputs specimen dimensions and optionally mass/volume and uploads a csv file of UTM data consisting of load and strain from an extensometer. In this tab the user can select what material properties they want to calculate. Additionally, there is a button that will generate the stress strain curve from the uploaded file if the user desires it. The curve will provide various key strength properties of the specimen material. 

**Tab 2**: RSS calculator. The user types in a syntactically corrrect algebraic expression and it will output the root sum square expression. A pop-up will appear afterwards prompting the user to input corresponding values for each variable and their uncertainty.

**Tab 3**: Monte Carlo Simulator. The user is prompted to give 4 data points in the x-axis and y-axis and their respective uncertainties, and the calculator will determine the linear regression and uncertainty using 10,000 simulations using the Monte Carlo method. 

**Tab 4**: Get material information. The user is prompted to either input material property values to identify the material, or the user can input the material name to get the material(s) properties.

## How to run the GUI:

The GUI is executed by running the script for mygui.py. This can be done in command line.

While in the `MoMpy` directory, enter in the command line: 
`python mygui.py`

