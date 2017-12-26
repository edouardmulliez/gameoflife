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
line = np.ones((1,10))
pos = (10,5)
X[pos[0]:pos[0]+line.shape[0],pos[1]:pos[1]+line.shape[1]] = line

X = X.astype(np.bool)

X[15,2]

plt.imshow(X)


# Compute next step of X

kernel = np.array([[1,1,1],
                   [1,1,1],
                   [1,1,1]], dtype=np.int8)
def evolve(X):
    nbors = convolve2d(X, kernel, mode='same', boundary='fill')
    X = ((nbors == 3) | (X & (nbors == 4)))
    return(X)

for i in range(10):
    X = evolve(X)
    plt.imshow(X)
    plt.show()




fig = plt.figure()

def f(x, y):
    return np.sin(x) + np.cos(y)

x = np.linspace(0, 2 * np.pi, 120)
y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)

im = plt.imshow(f(x, y), animated=True)

def updatefig(*args):
    global x, y
    x += np.pi / 15.
    y += np.pi / 20.
    im.set_array(f(x, y))
    return im,

ani = animation.FuncAnimation(fig, updatefig, frames=np.linspace(1,100,100), blit=True)
plt.show()

ani.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])



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





