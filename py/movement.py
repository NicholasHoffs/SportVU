import pandas as pd
import numpy as np

def velocity(x_loc,y_loc):

    diffx = np.diff(x_loc)
    diffy = np.diff(y_loc)

    diffx2 = np.square(diffx)
    diffy2 = np.square(diffy)

    a = diffx2+diffy2
    b = np.sqrt(a)*25

    return b

def acceleration(x_loc,y_loc):

    diffx = np.diff(x_loc, n=2)
    diffy = np.diff(y_loc, n=2)

    diffx2 = np.square(diffx)
    diffy2 = np.square(diffy)

    a = diffx2+diffy2
    b = np.sqrt(a)*25*25

    return b