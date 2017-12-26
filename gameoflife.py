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
import matplotlib.pyplot as plt

X = np.zeros((30,30))
line = np.ones((1,8))
X[15,2:10] = line

X = X.astype(np.bool)

X[15,2]

plt.imshow(X)

    