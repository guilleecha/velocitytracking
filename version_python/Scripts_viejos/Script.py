
#%% SCRIPT 
import sys
sys.path.append('/Users/guille/Dropbox/Maestria/002 - Scripts')


from angle2velocity import angle2velocity
from dist_solver import distance_solver
from matplotlib import ticker
from rectificacion import rectification
from undistor_video import undistor_video
from time_stack import time_stack
from matplotlib import pyplot as plt
from matplotlib import cm
import cv2
import numpy as np
from scipy import stats
from skimage.transform import radon
from peakdet import peakdet
from createCircularMask import createCircularMask
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

%matplotlib

#%% DATOS DE INGRESO

#VIDEO
path = '/Users/guille/Dropbox/Maestria/001 - Salidas de campo/001 - Rocha_Km244_20062017/001 - Procesamiento_Videos/Dia2/Drifters_3_2017-06-22'
video_name = 'Drifters_3_2017-06-22_undistorted'
ext = 'MKV' 


#PUNTOS DE REFERENCIA
# pts_in = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4]])
# pts_in : Puntos de entrada en [m] - Arreglo 4x2 [top left,top right,bottom left, bottom right]

pts_in = np.array([ [0 , 0] , 
          [ 36.3, 0] , 
          [36.7 , 33.7] ,
          [0 , 41.5] ])

pts_in = distance_solver(PuntosGPS = True)

#%% CALIBRACION DE CAMARA Y CORRECCION DE DISTORSION

Calib_Dir = '/Users/guille/Dropbox/Maestria/008 - Calibracion/001 - GoPro - Hero4+/'
CM = np.load(Calib_Dir + '/calibrationMatrix.npy')
DC = np.load(Calib_Dir + '/distortionCoeff.npy')

del Calib_Dir


video_name_out = video_name + '_undistorted'

undistor_video(path,video_name,ext,video_name_out,CM,DC)

#%% RECTIFICACION DE LAS IMAGENES

video_name = video_name_out

# PRIMER FRAME DEL VIDEO
vidcap = cv2.VideoCapture(path + '/' + video_name  + '.'+ ext)
success,frame = vidcap.read()
frame0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
I_for_rect=frame0.copy()

#CARGO UNA IMAGEN QUE TENGA PARA UTILIZAR
filename = '/Users/guille/Dropbox/Maestria/001 - Salidas de campo/001 - Rocha_Km244_20062017/001 - Procesamiento_Videos/Dia2/Para_rectificacion/Para_rect.png'
I_for_rect  = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
I_for_rect =  cv2.undistort(I_for_rect, CM, DC)


dx=1/10

H,img_transformada,X,Y = rectification(I_for_rect,pts_in,dx)


#%% ARMADO DEL TIME-STACK
time_start = 0  
time_stop = 1080
frame_rate = 29
timestacks = time_stack(path,video_name,ext,H,frame_rate,X,Y,time_start,time_stop,number_lines=1)
    
fig,ax = plt.subplots()
ax.imshow(timestack)
ax.set_title('Time_Stack')
ax.set_xlabel('Tiempo')
ax.set_ylabel('Distancia')

#%% TRATAMIENTO PREVIO A ANALISIS






      

#%% ANALISIS 
#RADON

overlaping = 50 # [%] en porcentaje

m, n = np.shape(timestack)

if n>m:
    times = int(np.floor(n/m))
else:
    print('El timestack es muy corto o la transecta es muy larga')
    
overlap_times = int(times/((100-overlaping)/100))
sinogram = np.zeros((m,m,overlap_times-1))
Angular_density = np.zeros((m,overlap_times-1))
Fourier_spec = np.zeros((m,m,overlap_times-1))

flag_show = False
mask = createCircularMask(m,m)



for j in range(overlap_times-1):
    
    print('Progreso: %.1f' % ((j/overlap_times)*100) + '%' )
    timestack_j = timestack[:,int(j* m * (1 - (overlaping/100))):int(( 1 + j*(1- (overlaping/100)))*m)]
    image = timestack_j * mask
    theta = np.linspace(0., 180., max(image.shape), endpoint=False)

    sinogram[:,:,j] = radon(image, theta=theta, circle=True)
    Angular_density[:,j] = np.var(sinogram[:,:,j], axis=0)
    
    F = np.fft.fft2(timestack_j)
    F = np.abs(F)
    Fourier_spec[:,:,j]=np.fft.fftshift(F)
        

    
    if flag_show:
        
        fig3, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))
        
        ax1.set_title("Original")
        ax1.imshow(image, cmap=plt.cm.Greys_r)
        
        ax2.set_title("Transformada de Radon\n(Sinogram)")
        ax2.set_xlabel("Angulo de proyección (deg)")
        ax2.set_ylabel("Posicion de proyección (pixels)")
        ax2.imshow(sinogram[:,:,j], cmap=plt.cm.Greys_r,
                   extent=(0, 180, 0, sinogram[:,:,j].shape[0]), aspect='auto')
        
        fig3.tight_layout()
        plt.show()







#DESCARTO VELOCIADES MAYORES A 2.5 m/s y menores a -2.5 m/s

v_min = 1
theta_min = np.round((90 - np.arctan(v_min/(frame_rate*dx)) * 180 / np.pi)*.1 )/.1
theta_max = np.round((180 - theta_min)*.1)/.1

theta2 = theta [(theta>theta_min) & (theta<theta_max) ]
velocities = np.round(np.tan((90-theta2)*np.pi/180)*dx*frame_rate*100)/100

Angular_density_2 = Angular_density [(theta>theta_min) & (theta<theta_max) ]





thetas_max_t=list()
max_peaks_t=list()

for k in range(np.shape(Angular_density_2)[1]):
        
    maxpeaks_k, _ = peakdet(Angular_density_2[:,k], 10000)
        
    if maxpeaks_k.size :
        max_peak_k = np.max(maxpeaks_k[:,1])
            
        thetas_max_k = theta2[maxpeaks_k[:,0][maxpeaks_k[:,1]==np.max(maxpeaks_k[:,1])].astype(int)]
    else:
        max_peak_k = np.nan
        thetas_max_k = np.nan
                
               
    thetas_max_t.append(thetas_max_k)
    max_peaks_t.append(max_peak_k)
    
mean = np.mean(Angular_density_2,axis=1)
median = np.median(Angular_density_2,axis=1)
    
mean_peak,_ = peakdet(mean, 1000)
theta_mean_peak = theta2[mean_peak[:,0].astype(int)]



#FILTRADO POR MAXIMO DE MAXIMOS RELATIVOS
threshold_max = 1e7

thetas_max_t = np.asarray(thetas_max_t)
max_peaks_t = np.asanyarray(max_peaks_t)


thetas_max_t_filtered=np.copy(thetas_max_t)
max_peaks_t_filtered=np.copy(max_peaks_t)
thetas_max_t_filtered =thetas_max_t [max_peaks_t > threshold_max]
max_peaks_t_filtered = max_peaks_t [max_peaks_t > threshold_max]
Angular_density_filtered = np.copy(Angular_density_2)

for k in range(np.shape(Angular_density_2)[1]):
    
    if np.max(Angular_density_2[:,k]) < threshold_max:
        Angular_density_filtered[:,k] = np.nan
        
mean_filtered = np.nanmean(Angular_density_filtered,axis=1)
median_filtered = np.nanmedian(Angular_density_filtered,axis=1)


mean_peak_filtered,_ = peakdet(mean_filtered, 100)
theta_mean_peak_filtered = theta2[mean_peak_filtered[:,0][mean_peak_filtered[:,1] == np.max(mean_peak_filtered[:,1])].astype(int)]
mean_peak_filtered = np.max(mean_peak_filtered[:,1])

median_peak_filtered,_ = peakdet(median_filtered, 100)
theta_median_peak_filtered = theta2[median_peak_filtered[:,0][median_peak_filtered[:,1] == np.max(median_peak_filtered[:,1])].astype(int)]
median_peak_filtered = np.max(median_peak_filtered[:,1])


## CALCULO DE VELOCIADES FINALES
angle_median_filtered = np.median(thetas_max_t_filtered)
angle_mean_filtered = np.mean(thetas_max_t_filtered)


#%%

#VISULIAZACION RADON (SIN DEPURAR)
        

def ticks_velocity(value,index):
    
    tick=angle2velocity(frame_rate,dx,value)
    
    return str('%.2f' % tick)







flag_plot_individual_max = True 

    
#xticks_positions =  np.sort(list(set(np.round(np.linspace(theta2.min(),theta2.max(),19)*.1)/.1))).astype(int)
#xticks_labels = xticks_positions

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()


lines = ax1.plot(theta2,median,theta2,mean)
l1,l2 = lines
plt.setp(l1,linewidth=8)
plt.setp(l2,linewidth=8)
#ax1.set_xticks(xticks_positions)
#ax1.set_xticklabels(xticks_labels)


majorLocator = MultipleLocator(10)
majorFormatter = FormatStrFormatter('%d')
minorLocator = AutoMinorLocator()
#minorLocator = MultipleLocator(2)

ax1.xaxis.set_major_locator(majorLocator)
ax1.xaxis.set_major_formatter(majorFormatter)
ax1.xaxis.set_minor_locator(minorLocator)
ax1.tick_params(which='both', width=2)
ax1.tick_params(which='major', length=7)
ax1.tick_params(which='minor', length=4, color='r')
x_ticks =  ax1.get_xticks()

ax1.set_xlim(theta_min,theta_max)
ax1.set_xlabel("Angulo de proyección (deg)")
ax1.set_ylabel('Varianza')
#ax1.grid()
ax1.xaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
ax1.yaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
ax1.xaxis.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)





        
#        for xy in zip(thetas_max_k, maxpeaks_k[:,1]):
#            ax1.annotate('Velocidad: %s m/s' % angle2velocity(frame_rate,dx,thetas_max_k), xy=xy)
            

velocity_xticks_labels = angle2velocity(frame_rate,dx,ax1.get_xticks())

ax2.plot(theta2,Angular_density_2,'-',alpha=0.4)


ax2.xaxis.set_major_locator(majorLocator)
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(ticks_velocity))
ax2.xaxis.set_minor_formatter(ticker.FuncFormatter(ticks_velocity))
ax2.xaxis.set_minor_locator(minorLocator)

ax2.tick_params(which='both', width=2)
ax2.tick_params(which='major', length=7)
ax2.tick_params(which='minor', length=4, color='r')


ax2.set_xlim(ax1.get_xlim())
#ax2.set_ylim(0,)
ax2.set_xlabel("Velocidad (m/s)")

if flag_plot_individual_max:
    ax1.plot(thetas_max_t,max_peaks_t ,'bo', markersize = 5)
    
ax1.plot(theta_mean_peak,mean_peak[:,1] ,'ro', markersize = 15)
#BANDERA PARA PLOTEAR VALOR MAXIMO DE MEAN
for xy in zip(theta_mean_peak, mean_peak[:,1]):
    ax1.annotate('Velocidad: %s m/s' % angle2velocity(frame_rate,dx,theta_mean_peak), xy=xy,fontsize=12)
plt.show()



#%% #VISULIAZACION RADON (DEPURADA)


flag_plot_individual_max = True 
  

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()


lines = ax1.plot(theta2,median_filtered,theta2,mean_filtered)
l1,l2 = lines
plt.setp(l1,linewidth=8)
plt.setp(l2,linewidth=8)


majorLocator = MultipleLocator(10)
minorLocator = AutoMinorLocator()

ax1.xaxis.set_major_locator(majorLocator)
ax1.xaxis.set_minor_locator(minorLocator)
ax1.tick_params(which='both', width=2)
ax1.tick_params(which='major', length=7)
ax1.tick_params(which='minor', length=4, color='r')
x_ticks =  ax1.get_xticks()

ax1.set_xlim(theta_min,theta_max)
ax1.set_xlabel("Angulo de proyección (deg)")
ax1.set_ylabel('Varianza')

ax1.xaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
ax1.yaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
ax1.xaxis.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)


        

ax2.plot(theta2,Angular_density_filtered,'-',alpha=0.4)


ax2.xaxis.set_major_locator(majorLocator)
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(ticks_velocity))
ax2.xaxis.set_minor_formatter(ticker.FuncFormatter(ticks_velocity))
ax2.xaxis.set_minor_locator(minorLocator)

ax2.tick_params(which='both', width=2)
ax2.tick_params(which='major', length=7)
ax2.tick_params(which='minor', length=4, color='r')


ax2.set_xlim(ax1.get_xlim())
ax2.set_ylim(bottom=0)
#ax2.set_ylim(0,)
ax2.set_xlabel("Velocidad (m/s)")


if flag_plot_individual_max:
    ax1.plot(thetas_max_t_filtered,max_peaks_t_filtered ,'bo', markersize = 5)
 

#BANDERA PARA PLOTEAR VALOR MAXIMO DE MEAN
ax1.plot(theta_mean_peak_filtered,mean_peak_filtered ,'go',markersize=15)
ax1.annotate('Velocidad: %s m/s' % angle2velocity(frame_rate,dx,theta_mean_peak_filtered),
              xy=[theta_mean_peak_filtered,mean_peak_filtered],fontsize=12)

#BANDERA PARA PLOTEAR VALOR MAXIMO DE MEDIAN
ax1.plot(theta_median_peak_filtered,median_peak_filtered ,'ro',markersize=15)
ax1.annotate('Velocidad: %s m/s' % angle2velocity(frame_rate,dx,theta_median_peak_filtered), 
             xy=[theta_median_peak_filtered,median_peak_filtered],fontsize=12) 
plt.show()



#%%SELECCION DE CORRIENTE MEDIA




#%%
##VISUALIZACION Fourier
def ticks_x_fourier(value,index):
    
    tick=-frame_rate + (2*frame_rate/b)*value
    
    return str('%.2f' % tick)

def ticks_y_fourier(value,index):
    
    tick = (-(1/a)*value + (1/2)) / dx
    
    return str('%.2f' % tick)

a,b = np.shape(Fourier_mean)

Fourier_mean = np.mean(Fourier_spec,axis=2)
Fourier_mean_log10 = np.log10(Fourier_mean)
Fourier_mean_log10_plot = Fourier_mean_log10[0:int(a/2),::]






fig = plt.figure()
ax1 = fig.add_subplot(111)
plot_spec = ax1.imshow(Fourier_mean_log10_plot,cmap=cm.viridis)
ax1.set_xlabel('Frequency [Hz]')
ax1.set_ylabel('Wavenumbers [1/m]')
fig.colorbar(plot_spec,ax=ax1)

majorLocator_x = MultipleLocator(int(b/10))
minorLocator_x = AutoMinorLocator()
#minorLocator = MultipleLocator(2)
ax1.xaxis.set_major_locator(majorLocator_x)
ax1.xaxis.set_major_formatter(ticker.FuncFormatter(ticks_x_fourier))
ax1.xaxis.set_minor_locator(minorLocator_x)
ax1.tick_params(which='both', width=2)
ax1.tick_params(which='major', length=7)
ax1.tick_params(which='minor', length=4, color='r')
#

majorLocator_y = MultipleLocator(int(a/10))
minorLocator_y = AutoMinorLocator()
ax1.yaxis.set_major_locator(majorLocator_y)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(ticks_y_fourier))
ax1.yaxis.set_minor_locator(minorLocator_y)

x_ticks = ax1.get_xticks()







# espectro con colorbar

fig, (ax1, ax2) = plt.subplots(2, 1, sharey=True)
plot_ts = ax1.imshow(timestack,cmap='gray')
#fig.colorbar(plot_ts,ax=ax1)
plot_spec = ax2.imshow(mag,cmap='jet')
fig.colorbar(plot_spec,ax=ax2)


#%% PRESENTACION DE RESULTADOS
























