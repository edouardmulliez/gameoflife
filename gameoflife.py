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



class Golife:
    """
    Class for the implementation of the Game of Life
    """

    GRID_SIZE=(500, 500)
    ## Classical Patterns
    PATTERNS = dict({
        'glider': np.array([[0, 1, 0],
                            [0, 0, 1],
                            [1, 1, 1]], dtype=np.int),
        'small_exploder': np.array([[0,1,0],
                                    [1,1,1],
                                    [1,0,1],
                                    [0,1,0]], dtype=np.int),
        'exploder': np.array([[1,0,1,0,1],
                              [1,0,0,0,1],
                              [1,0,0,0,1],
                              [1,0,0,0,1],
                              [1,0,1,0,1]], dtype=np.int),
        'line': np.ones((1,10), dtype=np.int),
        'spaceship': np.array([[0,1,1,1,1],
                               [1,0,0,0,1],
                               [0,0,0,0,1],
                               [1,0,0,1,0]], dtype=np.int),
        'tumbler': np.array([[0,1,1,0,1,1,0],
                             [0,1,1,0,1,1,0],
                             [0,0,1,0,1,0,0],
                             [1,0,1,0,1,0,1],
                             [1,0,1,0,1,0,1],
                             [1,1,0,0,0,1,1]]),
        'gun': np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0],
                         [1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]], dtype=np.int)
    })

    def __init__(self, pattern='line'):
        self.tab = np.zeros(Golife.GRID_SIZE, dtype=np.bool)
        self.set_pattern(pattern)

    def add_to_grid(self, element):
        """
        Add element to tab (centered). element should be a numpy array.
        """
        h, w = Golife.GRID_SIZE
        he, we = element.shape
        self.tab[(h-he)/2:(h+he)/2, (w-we)/2:(w+we)/2] = element

    def add_point(self, row, col):
        """
        Add or remove point in tab.
        """
        self.tab[row, col] = not self.tab[row, col]

    def set_pattern(self, name):
        """
        Set the chosen pattern in the middle of tab
        """
        if (name not in Golife.PATTERNS.keys()):
            raise NameError(
                'Incorrect pattern name. Possible names are: ' +
                ', '.join(Golife.PATTERNS.keys())
            )
        self.tab[:,:] = False
        self.add_to_grid(Golife.PATTERNS[name])

    def next(self):
        """
        Computes one steps of the game of life and update tab
        """
        kernel = np.ones((3,3), dtype=np.int8)
        nbors = convolve2d(self.tab, kernel, mode='same', boundary='fill')
        self.tab[:,:] = ((nbors == 3) | (self.tab & (nbors == 4)))






# X = np.zeros(GRID_SIZE)
# X = X.astype(np.bool)


# def add_to_grid(X, element):
#     """
#     Add element to tab (centered). element should be a numpy array.
#     """
#     h,w = X.shape
#     he, we = element.shape
#     X[(h-he)/2:(h+he)/2, (w-we)/2:(w+we)/2] = element

# add_to_grid(X, patterns['gun'])


# def evolve(X):
#     """
#     Computes one steps of the game of life
#     """
#     kernel = np.array([[1,1,1],
#                    [1,1,1],
#                    [1,1,1]], dtype=np.int8)
#     nbors = convolve2d(X, kernel, mode='same', boundary='fill')
#     X[:,:] = ((nbors == 3) | (X & (nbors == 4)))

# fig = plt.figure()
# im = plt.imshow(np.zeros(X.shape, dtype=np.bool),
#                 cmap='gray', vmin=0, vmax=1, animated=True)

# def updatefig(i):
#     evolve(X)
#     im.set_array(X)
#     return im,

# ani = animation.FuncAnimation(fig, updatefig, frames=np.linspace(1,100,100), blit=True)
# plt.show()

# ani.save('life_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])




# To do:
# 2. In html page
# 4. Have an interface where user can click to add points


# Idea: create a canvas where we draw the image. Listen for mouse clicks.
# Optional: possibility to zoom in/out. Start/stop animation. Next button. 


