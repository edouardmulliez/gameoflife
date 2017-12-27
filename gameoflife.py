#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Conway's Game of Life

@author: em


1. Implement Game if life with wraping borders.
2. When done, implement a User interface with: 
    - default patterns
    - possibility for the user to add some point himself
    - change the number of squares on the image
    
example here: https://bitstorm.org/gameoflife/

"""

import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
import matplotlib.animation as animation

X = np.zeros((20,20))
X = X.astype(np.bool)
line = np.ones((1,10))

# Add pattern in the middle of X.
def add_to_grid(X, element):
    """
    Add element to grid X (centered)
    """
    h,w = X.shape
    he, we = element.shape
    X[(h-he)/2:(h+he)/2, (w-we)/2:(w+we)/2] = element

add_to_grid(X, line)

plt.imshow(X)


# Compute next step of X

kernel = np.array([[1,1,1],
                   [1,1,1],
                   [1,1,1]], dtype=np.int8)
def evolve(X):
    """
    Computes one steps of the game of life
    """
    nbors = convolve2d(X, kernel, mode='same', boundary='fill')
    X = ((nbors == 3) | (X & (nbors == 4)))
    return(X)


fig = plt.figure()
im = plt.imshow(np.zeros(X.shape, dtype=np.bool),
                cmap='gray', vmin=0, vmax=1, animated=True)

def updatefig(i):
    global X
    X = evolve(X)
    im.set_array(X)
    return im,

ani = animation.FuncAnimation(fig, updatefig, frames=np.linspace(1,100,100), blit=True)
plt.show()

ani.save('life_animation.mp4', fps=5, extra_args=['-vcodec', 'libx264'])




# To do:
# 1. Insert it in Jupyter Notebook
# 2. In html page
# 3. Save some classical patterns and propose it
# 4. Have an interface where user can click to add points


# Idea: create a canvas where we draw the image. Listen for mouse clicks.
# Optional: possibility to zoom in/out. Start/stop animation. Next button. 


acorn = np.array([[0, 1, 1],
                  [1, 1, 1],
                  [1, 0, 0]], dtype=np.int)








