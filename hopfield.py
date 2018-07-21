# A Hopfield Network Application that stores and recalls patterns
# Author: Parker Sorenson
# 04/19/18

#Point: Each time you start the application, the weight matrix is all zeros
#During each time the application is run, the weight matrix is never
#zeroed out.  The state vector at any point may be removed in order to
#either store another stable state or to start from a random state
#and see where it converges.  The updating is applied asynchonously,
#but each element in the state vector x is updated x_1,...,x_n
#so it is deterministic

#currently doing the simple implementation that uses a grid of squares
#in the future, we will do grayscale images
#and then the model using 3 networks, one each for R, G, and B
#implementing the pictures would not be hard.  You just have to use PIL
#and convert them to grayscale and then apply the algorithm.

#to do in future:
#1. implement the energy function and print the energy of the network
#   at each step
#2. the ability to drag across states to make it easier
#   to input state vectors

from tkinter import *
import numpy as np
import random as rand

##class for the squares in the GUI
class Square(Frame):
    def __init__(self, onColor, offColor, parent=None):

        self.state = -1

        self.offColor = offColor
        self.onColor = onColor
        
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)                 

        canv = Canvas(self, bg=self.offColor)
        canv.config(width=50, height=50)                    
        canv.pack(side=LEFT, expand=YES, fill=BOTH)
        canv.bind('<Button-1>', self.onClick)     
        self.canvas = canv
        
    def onClick(self, event):
        if self.state == -1:
            self.state = 1
            self.canvas.config(self.canvas, bg = self.onColor)
        else:
            self.state = -1
            self.canvas.config(self.canvas, bg = self.offColor)

    #set the state depending on a number
    def update(self, num):
        if num >= 0:
            self.state = 1
            self.canvas.config(self.canvas, bg = self.onColor)
        else:
            self.state = -1
            self.canvas.config(self.canvas, bg = self.offColor)

#function to reset the states of all of the Square objects
#i.e. if you want to store another stable state
#or start from a random state and see where you converge to 
def clear(squares):
    for square in squares:
        square.update(-1)

####the part of the program with the logic of the Hopfield network####

# a function to set the current state of squares
# as a stable state of the network
def storeVector(squares, weights):

    ##the algorithm according to Rojas
    n = len(squares)
    
    for i in range(n):
        for j in range(n):
            if i != j:
                weights[i,j] += squares[i].state*squares[j].state

#a function to do one iteration of the update function
def step(squares, weights):

    n = len(squares)
    
    threshold  = []
    for i in range(n):
        threshold.append(0)

    #we don't create a new vector because we are
    #updating asynchronously but in order: 1,...,n
    for i,square in enumerate(squares):

        total = 0
        for j in range(n):
            total += weights[j,i]*squares[j].state - threshold[i]
            
        square.update(total)

# a function to run the network until it reaches a stable state
# we can probably just call step until the state of the network doesn't change
def run(squares, weights):

    while(True):
        #so we can check if the value has changed
        oldStates = []
        for square in squares:
            oldStates.append(square.state)
        
        step(squares,weights)

        changed = False
        for i in range(len(squares)):
            #the state vector changed
            if squares[i].state != oldStates[i]:
                changed = True
                break

        if changed == False: #nothing changed, we are at a fixed point
            break
            
    #old way of doing it
    #for i in range(20):
    #   step(squares, weights)

#a function to print out the current energy of the network
def energy(squares, weights):
    pass

# main function to initialize UI
def main():

    #our state vector will be of size n*n
    #n = rand.randint(5,11)

    n = 6
    
    root = Tk()
    root.title('Hopfield Network Simulation')

    #squares is the vector of Square objects
    squares = []
    
    #the program will select one of these colors to be the "on" color
    onColors = ['#0450fb', '#62ff84', '#00ffff', '#ff00ff', '#ff7f50','#3e0e4c']
    onColor = rand.choice(onColors)

    #the program will select one of these colors to be the "off" color
    offColors = ['#491600', '#fbffc0', '#62ff84', '#ff9be7', '#4dffce']
    offColor = rand.choice(offColors)
    offColor = '#dddddd'

    for i in range(n):
        for j in range(n):
            square = Square(onColor, offColor)
            squares.append(square)
            square.grid(row=i, column=j)

    ## section where we create our weight matrix
    #since state vector is of size n*n, weight matrix is of size n*n x n*n
    weights = np.zeros((n*n,n*n))

    #just to put the buttons in the right place

    if n > 3:
        halfNum = int(n/2)-1
    else:
        halfNum = 1
    #a button to start from a current state and step
    #through each iteration of the network
    stepButton = Button(text='Step', command  = lambda: step(squares,weights))
    stepButton.grid(row = n+1, column = halfNum - 1)
    #a button to run the network to a stable state
    runButton = Button(text='Run', command  = lambda: run(squares,weights))
    runButton.grid(row = n+1, column = halfNum)
    #a button to store the current state as a stable state
    storeButton = Button(text='Store', command  = lambda: storeVector(squares,weights))
    storeButton.grid(row = n+1, column = halfNum + 1)
    #a button to reset the states of the Squares (i.e. the state vector)
    # this can be used to add new stable states or to put in a start
    #state and see what it converges to
    resetButton = Button(text='Clear', command = lambda: clear(squares))
    resetButton.grid(row = n+1, column = halfNum+2)

    root.mainloop()
    
main()
