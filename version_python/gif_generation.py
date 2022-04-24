import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import imageio
%matplotlib
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from angle2velocity import angle2velocity
import numpy as np
from scipy.stats import norm
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator,FormatStrFormatter,FuncFormatter)
from itertools import cycle
import cv2 #opencv
import os
from pathlib import Path
import time

def ticks_velocity(value,index):

    tick = angle2velocity(rectification_parameters["Temporal_scale"],rectification_parameters["Dimension_scale"],value)

    return str('%.2f' % tick)

def ticks_time(value,index):
    
    tick = timestacks["time"][0] + value * rectification_parameters["Temporal_scale"]
    return str('%.f' % tick)

def ticks_distance(value,index):
    tick = value * rectification_parameters["Dimension_scale"]
    return str('%.2f' % tick)


number_timestack = 5

timestack = timestacks["timestack" + str(number_timestack)]
empty_timestack = np.ones(np.shape(timestack))*255
frame_rate_gif = 1

#video = 

#rectification_parameters = 

# frame_rate : frame_rate deseado. No puede ser mayor al del video
# CM : CalibrationMatrix
# DC : Distorssion Coeeficiente
# time_start : tiempo de comienzo del time-stack en el video [s]
# time_stop : tiempo de fin del time-stack en el video [s]
# rect_par : Resultados de rectificacion



  
start = time.process_time()
    
oldpath = Path(os.getcwd())
    
#    os.chdir(path)
vidcap = cv2.VideoCapture(video)
fps = np.ceil(vidcap.get(cv2.CAP_PROP_FPS)) #para estar del lado de la seguridad
frameCount = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
length_video = frameCount/fps


#%%
            


t_start = 0
t_finish = 40
def plot_for_offset(t, timestacks):
    # Data for plotting
    print(str(t/t_finish*100) + '%')
    print(t)
    vidcap = cv2.VideoCapture(video)
    vidcap.set(cv2.CAP_PROP_POS_MSEC , (t + timestacks["time"][0]) * 1000)
    success,frame = vidcap.read()
    frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    image_i = cv2.warpPerspective(frame , rectification_parameters["Rect_Matrix"] , rectification_parameters["Size"])
    
    
    #%% ARMADO DE LA HOJA
    
    
    sup_title_fontsize = 15 
    title_fontsize = 10
    label_fontsize = 8
    major_ticks_fontsize = 7
    minor_ticks_fontsize = 5 
    legend_fontsize = 5
    
    plt.close('all')
    fig = plt.figure()


    
    gs1 = GridSpec(5,6)
    ax1 = plt.subplot(gs1[0,:])
    #gs1.update(hspace = 0.7, wspace = 0)

    gs2 = GridSpec(5,6)
    ax2 = plt.subplot(gs2[1:,:])
    #gs2.update(hspace = 0 , wspace = 0.5)


    #%% PLOT DEL TIMESTACK SELECCIONADO EN EL FRAME t
    
    dist_x = np.shape(rectification_parameters["Rectificated_Image"])[0]*rectification_parameters["Dimension_scale"]
    dist_y = np.shape(rectification_parameters["Rectificated_Image"])[1]*rectification_parameters["Dimension_scale"]

    ticks_ax2_x = (np.around(dist_x/5,decimals = 0) if (dist_x/5) > 1 else np.around(dist_x/5,decimals = 1))/rectification_parameters["Dimension_scale"]
    ticks_ax2_y = (np.around(dist_y/5,decimals = 0) if (dist_y/5) > 1 else np.around(dist_y/5,decimals = 1))/rectification_parameters["Dimension_scale"]
    
    majorLocator_ax2_x = MultipleLocator(ticks_ax2_x)
    minorLocator_ax2_x = AutoMinorLocator()
    
    majorLocator_ax2_y = MultipleLocator(ticks_ax2_y)
    minorLocator_ax2_y = AutoMinorLocator()

    ax2.xaxis.set_major_locator(majorLocator_ax2_x)
    ax2.xaxis.set_minor_locator(minorLocator_ax2_x)
    ax2.yaxis.set_major_locator(majorLocator_ax2_y)
    ax2.yaxis.set_minor_locator(minorLocator_ax2_y)

    ax2.imshow(image_i,aspect = 'auto')
    
    ax2.plot(timestacks["X"][number_timestack],timestacks["Y"][number_timestack],'ro-')


        
    ax2.xaxis.tick_top()
    ax2.yaxis.tick_left()
    ax2.xaxis.set_major_formatter(FuncFormatter(ticks_distance))
    ax2.yaxis.set_major_formatter(FuncFormatter(ticks_distance))
    ax2.tick_params(which = 'both', width = 2)
    ax2.tick_params(axis = 'both', which = 'major', length = 7, labelsize = major_ticks_fontsize)
    ax2.tick_params(axis = 'both', which = 'minor', length = 4, color = 'r', labelsize = minor_ticks_fontsize)
    
    ax2.xaxis.tick_bottom()
    ax2.set_xlabel("Distancia (m)",fontsize = label_fontsize)
    ax2.xaxis.set_label_position('bottom')
    
    ax2.set_ylabel("Distancia (m)",fontsize = label_fontsize)
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position('right')
    
        
    
    #%%
    i = int(t * fps)
    print(i)
    empty_timestack[::,:i] = timestack[::,:i]
    
    ax1.imshow(empty_timestack, aspect = 'auto') #VER TEMA DE ir agregando
    ax1.xaxis.tick_top()

    
    max_dist =         np.shape(timestack)[0]*rectification_parameters["Dimension_scale"]
    length_timestack = np.shape(timestack)[1]*rectification_parameters["Temporal_scale"]

    ticks_ax1_y = (np.around(max_dist/3,decimals = 0) if (max_dist/3) > 1 else np.around(max_dist/3,decimals = 1))/rectification_parameters["Dimension_scale"]
    ticks_ax1_x = (np.around(length_timestack/11,decimals = -1) if (length_timestack/11) > 10 else np.around(length_timestack/11,decimals = 0))/rectification_parameters["Temporal_scale"]

    
    majorLocator_ax1_xaxis = MultipleLocator(ticks_ax1_x)
    minorLocator_ax1_xaxis = AutoMinorLocator()
    ax1.xaxis.set_major_locator(majorLocator_ax1_xaxis)
    ax1.xaxis.set_minor_locator(minorLocator_ax1_xaxis)
    ax1.xaxis.set_major_formatter(FuncFormatter(ticks_time))
    
    majorLocator_ax1_yaxis = MultipleLocator(ticks_ax1_y)
    minorLocator_ax1_yaxis = AutoMinorLocator()
    ax1.yaxis.set_major_locator(majorLocator_ax1_yaxis)
    ax1.yaxis.set_minor_locator(minorLocator_ax1_yaxis)
    ax1.yaxis.set_major_formatter(FuncFormatter(ticks_distance))
    
    
    ax1.tick_params(which = 'both', width = 2)
    ax1.tick_params(axis = 'both', which = 'major', length = 7, labelsize = major_ticks_fontsize)
    ax1.tick_params(axis = 'both', which = 'minor', length = 4, color = 'r', labelsize = minor_ticks_fontsize)
    
    ax1.set_xlabel("Tiempo (s)", position = (1,0), fontsize = label_fontsize)
    ax1.xaxis.set_label_position('top')
    ax1.set_ylabel("Distancia (m)",fontsize = label_fontsize)
    
    
    #%%
    
    # Used to return the plot as an image rray
    fig.canvas.draw()       # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image

kwargs_write = {'fps':1.0, 'quantizer':'nq'}
imageio.mimsave('./animation.gif', [plot_for_offset(t, timestacks) for t in np.arange(0 , 40 , 1/frame_rate_gif)], fps_2 = 5)




#%%
