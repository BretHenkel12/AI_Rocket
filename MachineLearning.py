import pandas as pd
import random
import numpy as np
from colors import *
from mapVals import *
import pygame
''''
This includes the following functions:
getWeightedArray()
seed_weights()
normalizeState()
getDecision()
compressOutput()
returnUpdatedArrays()
displayNetwork()
add_names()
'''

def getWeightedArrays(a,h1,h2,z):
    '''
    This creates weighted arrays to determine all of the calculations
    for the neural network
    :param a: The number of inputs to the system
    :param h1: The number of nodes in hidden layer 1
    :param h2: The number of nodes in hidden layer 2, can be zero and will
    not create this layer
    :param z: The number of outputs of the system
    :return:
    '''
    h1_weights = pd.DataFrame()
    for i in range(h1):
        seeds = seed_weights(a)
        h1_weights[i] = seeds
    # Seed the second weights array
    h2_weights = pd.DataFrame()
    for i in range(h2):
        seeds = seed_weights(h1)
        h2_weights[i] = seeds
    if (h2):
        # Seed the final weights array
        z_weights = pd.DataFrame()
        for i in range(z):
            seeds = seed_weights(h2)
            z_weights[i] = seeds
    else:
        # Seed the final weights array
        z_weights = pd.DataFrame()
        for i in range(z):
            seeds = seed_weights(h1)
            z_weights[i] = seeds
    return (h1_weights,h2_weights,z_weights)


def seed_weights(rows):
    '''
    Returns random weights ranging from +/- 1
    :param rows: The number of rows in the array
    :return: One column for the final array with the proper amount of rows
    '''
    seeds = []
    for i in range(rows):
        seeds.append(random.randrange(-100, 100) / 100)
    return (seeds)


def normalizeState(state,f=1):
    '''
    Normalizes the state series to have values only between +/- 1
    :param state: The original array, composed of readings from program
    :param f: Controls the translating of the original state to its new value
    A higher value will lead to smaller values of the state converging to +/- 1
    :return:
    '''
    for i in range(state.size):
        state[i] = (1 / (1 + np.exp(-f*state[i]))) - 0.5
    return(state)


def getDecision(state,h1_weights,h2_weights,z_weights):
    '''
    Calculates the decisions from the neural network
    :param state: The readings from the program, often normalized
    :param h1_weights: Array of weights detailing the relationship between
    inputs and hidden layer 1 nodes
    :param h2_weights:Array of weights detailing the relationship between
    hidden layer 1 and hidden layer 2 nodes
    :param z_weights:Array of weights detailing the relationship between
    hidden layer 2 and z layer nodes or hidden layer 1 and z layer nodes
    :return:
    '''
    h1_output = np.dot(state, h1_weights)
    #Changes depending on if h2_weights was passed in
    if (isinstance(h2_weights, pd.DataFrame)):
        h2_output = np.dot(h1_output, h2_weights)
        output = np.dot(h2_output,z_weights)
        #output = np.sqrt(output)
    else:
        h2_output = None
        output = np.dot(h1_output,z_weights)
    return(output,h1_output,h2_output)


def compressOutput(output, f=1, s=1):
    '''
    This function helps to adjust the output to match your needs
    :param output: Initial output of the neural network
    :param f: A scaling factor, adjusts the tightness of the curve.
    A larger value will cause a smaller value input to be forced to -1 or 1
    :param s: The max boundary value to which all values will converge. A
    value of 1 will lead to all outputs converging to +/- 1
    :return: Output of neural network adjusted to desired size
    '''
    for i in range(output.size):
        output[i] = s*((1 / (1 + np.exp(-f*output[i]))) - 0.5)
    return(output)


def returnUpdatedArrays(h1_weights_master=None,h2_weights_master=None,z_weights_master=None,sigma=1):
    '''
    This function is designed to produce new random arrays that are based
    off of a previous trial
    :param h1_weights_master: The best h1_weights array
    :param h2_weights_master: The best h2_weights array
    :param z_weights_master: The best z_weights array
    :param sigma: The standard deviation of the change added to the arrays.
    A standard deviation of 1 will cause 68% of values to fall within +/- 1.
    This value is added to the passed in array. A std of 0.5 will cause 68%
    to fall within +/- 1
    :return: Returns the same arrays passed in after having the change added
    '''
    #Finds the shape of the passed in array
    h1_shape = h1_weights_master.shape
    #Creates an empty array of the same size
    h1_weights = pd.DataFrame(np.nan,index=range(h1_shape[0]),columns=range(h1_shape[1]))
    #Adds in values from original array plus a change to every element
    for i in range(h1_shape[0]):
        for j in range(h1_shape[1]):
            change = np.random.normal(loc=0.0, scale=sigma)
            h1_weights.iloc[i,j] = h1_weights_master.iloc[i,j] + change
    #Changes any values outside of +/- 1 to +/- 1
    h1_weights = h1_weights.mask(h1_weights>1,1)
    h1_weights = h1_weights.mask(h1_weights<-1,-1)
    
    h2_shape = h2_weights_master.shape
    h2_weights = pd.DataFrame(np.nan, index=range(h2_shape[0]), columns=range(h2_shape[1]))
    for i in range(h2_shape[0]):
        for j in range(h2_shape[1]):
            change = np.random.normal(loc=0.0, scale=sigma)
            h2_weights.iloc[i, j] = h2_weights_master.iloc[i, j] + change
    h2_weights = h2_weights.mask(h2_weights > 1, 1)
    h2_weights = h2_weights.mask(h2_weights < -1, -1)

    z_shape = z_weights_master.shape
    z_weights = pd.DataFrame(np.nan, index=range(z_shape[0]), columns=range(z_shape[1]))
    for i in range(z_shape[0]):
        for j in range(z_shape[1]):
            change = np.random.normal(loc=0.0, scale=sigma)
            z_weights.iloc[i, j] = z_weights_master.iloc[i, j] + change
    z_weights = z_weights.mask(z_weights > 1, 1)
    z_weights = z_weights.mask(z_weights < -1, -1)
    return(h1_weights,h2_weights,z_weights)

def displayNetwork(a,h1,h2,z,h1_weights,h2_weights,z_weights):
    # Set the screen parameters
    width = 400
    height = 250
    # Set up the parameters for drawing
    radius = 10
    line_width = 2
    # Set up the stuff for pygame
    clock = pygame.time.Clock()
    screen = pygame.Surface((width, height))
    # These are the color ranges that are used for the lines
    redRange = (130, 255)
    greenRange = (77, 255)

    if (isinstance(h2_weights, pd.DataFrame)):
        a_x = 50
        h1_x = 150
        h2_x = 250
        z_x = 350
    else:
        a_x = 50
        h1_x = 200
        z_x = 350
        h2_x = 0
    # The main loop
    # Finds equal vertical spacing for the circles
    a_yspace = height / (a + 1)
    h1_yspace = height / (h1 + 1)
    h2_yspace = height / (h2 + 1)
    z_yspace = height / (z + 1)
    #List of positions for the circles and line end points
    a_pos = []
    h1_pos = []
    h2_pos = []
    z_pos = []
    # Fills the screen with black
    screen.fill(black)
    # Find all of the positions of the circles
    a_y_current = 0
    for i in range(a):
        a_y_current += a_yspace
        a_pos.append((a_x, a_y_current))
    h1_y_current = 0
    for i in range(h1):
        h1_y_current += h1_yspace
        h1_pos.append((h1_x, h1_y_current))
    z_y_current = 0
    for i in range(z):
        z_y_current += z_yspace
        z_pos.append((z_x, z_y_current))
    if (isinstance(h2_weights, pd.DataFrame)):
        h2_y_current = 0
        for i in range(h2):
            h2_y_current += h2_yspace
            h2_pos.append((h2_x, h2_y_current))
    # draws in the lines
    for i in range(a):
        for j in range(h1):
            w = h1_weights.iloc[i][j]
            if (w < 0):
                color = (mapVals(w, redRange), 0, 0)
            else:
                color = (0, mapVals(w, greenRange), 0)
            pygame.draw.line(screen, color, a_pos[i], h1_pos[j], line_width)
    if (isinstance(h2_weights, pd.DataFrame)):
        for i in range(h1):
            for j in range(h2):
                w = h2_weights.iloc[i][j]
                if (w < 0):
                    color = (mapVals(w, redRange), 0, 0)
                else:
                    color = (0, mapVals(w, greenRange), 0)
                pygame.draw.line(screen, color, h1_pos[i], h2_pos[j], line_width)
        for i in range(h2):
            for j in range(z):
                w = z_weights.iloc[i][j]
                if (w < 0):
                    color = (mapVals(w, redRange), 0, 0)
                else:
                    color = (0, mapVals(w, greenRange), 0)
                pygame.draw.line(screen, color, h2_pos[i], z_pos[j], line_width)
    else:
        for i in range(h1):
            for j in range(z):
                w = z_weights.iloc[i][j]
                if (w < 0):
                    color = (mapVals(w, redRange), 0, 0)
                else:
                    color = (0, mapVals(w, greenRange), 0)
                pygame.draw.line(screen, color, h1_pos[i], z_pos[j], line_width)
    # draw the circles
    for i in range(a):
        pygame.draw.circle(screen, white, a_pos[i], radius)
    for i in range(h1):
        pygame.draw.circle(screen, white, h1_pos[i], radius)
    for i in range(z):
        pygame.draw.circle(screen, white, z_pos[i], radius)
    if (isinstance(h2_weights, pd.DataFrame)):
        for i in range(h2):
            pygame.draw.circle(screen, white, h2_pos[i], radius)
    return(screen)


def add_names(h1_weights=None,h2_weights=None,z_weights=None):
    '''
    Indices and columns names are added to the arrays
    :param h1_weights: Array of weights detailing the relationship between
    inputs and hidden layer 1 nodes
    :param h2_weights:Array of weights detailing the relationship between
    hidden layer 1 and hidden layer 2 nodes
    :param z_weights:Array of weights detailing the relationship between
    hidden layer 2 and z layer nodes or hidden layer 1 and z layer nodes
    :return: Returns the arrays with added indices and columns
    '''
    if (isinstance(h1_weights, pd.DataFrame)):
        h1_columns = []
        h1_indices = []
        h1_shape = h1_weights.shape  #rows,columns
        for i in range(h1_shape[0]):
            h1_indices.append("a_"+str(i))
        for i in range(h1_shape[1]):
            h1_columns.append("h1_"+str(i))
        h1_weights.columns = [h1_columns]
        h1_weights.index = [h1_indices]
    if (isinstance(h2_weights, pd.DataFrame)):
        h2_columns = []
        h2_indices = []
        h2_shape = h2_weights.shape  #rows,columns
        for i in range(h2_shape[0]):
            h2_indices.append("h1_"+str(i))
        for i in range(h2_shape[1]):
            h2_columns.append("h2_"+str(i))
        h2_weights.columns = [h2_columns]
        h2_weights.index = [h2_indices]
    if (isinstance(z_weights, pd.DataFrame) and isinstance(h2_weights, pd.DataFrame)):
        z_columns = []
        z_indices = []
        z_shape = z_weights.shape  #rows,columns
        for i in range(z_shape[0]):
            z_indices.append("h2_"+str(i))
        for i in range(z_shape[1]):
            z_columns.append("z_"+str(i))
        z_weights.columns = [z_columns]
        z_weights.index = [z_indices]
    if (isinstance(z_weights, pd.DataFrame) and isinstance(h2_weights, pd.DataFrame)==False):
        z_columns = []
        z_indices = []
        z_shape = z_weights.shape  # rows,columns
        for i in range(z_shape[0]):
            z_indices.append("h1_" + str(i))
        for i in range(z_shape[1]):
            z_columns.append("z_" + str(i))
        z_weights.columns = [z_columns]
        z_weights.index = [z_indices]
    return(h1_weights,h2_weights,z_weights)