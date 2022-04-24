def angle2velocity(dt,dx,angle):
    import numpy as np

    vel = (np.tan((90-angle)*np.pi/180)*dx)/dt
    return vel