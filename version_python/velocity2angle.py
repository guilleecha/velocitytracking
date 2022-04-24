def velocity2angle(dt,dx,velocity):
    import numpy as np

    angle = 90 - np.arctan((velocity*dt)/dx) * 180 / np.pi
    
    return angle