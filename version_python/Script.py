import sys
from pathlib import Path
script_folder = Path("/Users/guille/Dropbox/Maestria/002 - Scripts/Version_Python/")
sys.path.append(str(script_folder))
%matplotlib
from load_data import load_data
from process_timestack import process_timestack
from timestack_filter import timestack_filter
from data_results import data_results
from print_figures import print_figures
from timestack import timestack
from rectificacion import rectification
from undistor_video import undistor_video
from stabilization import stabilization
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np

plt.rcParams['image.cmap'] = 'gray'
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.dpi'] = 150
plt.rcParams['figure.figsize'] = 11.69,8.27





#%% MENU


while True:
    print('''\nMENU
Ingrese el numero de la opcion deseada :
1) Cargar datos ya procesados
2) Cargar video
3) Estbilizacion de video
4) Calibracion y correcion de distorsion de camara
5) Rectificacion
6) Armado de los timestacks
7) Procesamiento de timestacks
8) Filtrado de la informacion
9) Resultados
10) Salidas graficas
11) Salir ''')
        
    option = (input("Opcion : "))
    try:
        if option == '1':
            print("\nMenu de carga de datos")
            print("Ingrese la opcion deseada :\n1 : Cargar Parametros de Rectificacion\n2 : Cargar Timestacks\n3 : Cargar Timestacks procesados\n4 : Cargar Datos Filtrados\n5 : Cargar Resultados\n6 : Salir")
            while True:
                load_option = input("Opcion : ")        
                if load_option == '1':
                    rect_par_name = input("Nombre del archivo de Parametros de Rectificacion : ")
                    rectification_parameters = load_data(rect_par_name)
                    del rect_par_name
                    pass       
                elif load_option == '2':
                    time_stacks_name = input("Nombre del archivo de timestacks : ")
                    timestacks = load_data(time_stacks_name)
                    del time_stacks_name
                    pass
                elif load_option == '3':
                    processed_timestacks_name = input("Nombre del archivo de timestacks procesados : ")
                    processed_timestacks = load_data(processed_timestacks_name)
                    del processed_timestacks_name
                    pass
                elif load_option == '4':
                    data_filtered_name = input("Nombre del archivo de datos filtrados : ")
                    data_filtered = load_data(data_filtered_name)
                    del data_filtered_name
                    pass
                elif load_option == '5':
                    results_name = input("Nombre del archivo de Resultados : ")
                    results = load_data(results_name)
                    del results_name
                    pass
                elif load_option == '6':
                    print("Ha salido del menu de carga de datos")
                    break
                
                else:
                    print("No presiono alguna de las opciones")
                    pass
        
        elif option == '2':
            print("Para cargar el video debera ingresar el nombre del video con su extension")
#            video_path = input("Escribir path del video : ")
            video_name = input("Nombre del video con su extension : ")
#            video = video_path + '/' + video_name
            video = video_name
            pass
        elif option == '3':
            video = stabilization(video)
            pass
        elif option == '4':

            pass
        elif option == '5':
            rectification_parameters = rectification(video) #video es la direccion del video o en caso que este trabajando en esa carpeta el nombre del video con extension
            pass
        elif option == '6':
            timestacks,rectification_parameters = timestack(video,rectification_parameters)
            pass
        elif option == '7':
            processed_timestacks = process_timestack(timestacks,rectification_parameters)
            pass
        elif option == '8':
            data_filtered = timestack_filter(processed_timestacks,rectification_parameters,threshold = 1e5)
            pass
        elif option == '9':
            results = data_results(data_filtered,rectification_parameters)
            pass
        elif option == '10':
            print_figures(timestacks,rectification_parameters,data_filtered,processed_timestacks,results)
            pass
        elif option == '11':
            print("Proceso terminado por el usuario")
            break
        else:
            print("No presiono alguna de las opciones")
            print("Ingrese el numero de la opcion deseada : \n1: Elegir cantidad de timestacks\n2: Elegir distancia entre timestacks")
            pass
    except:
        break


#%% CALIBRACION DE CAMARA Y CORRECCION DE DISTORSION

Calib_Dir = '/Users/guille/Dropbox/Maestria/008 - Calibracion/001 - GoPro - Hero4+/'
CM = np.load(Calib_Dir + '/calibrationMatrix.npy')
DC = np.load(Calib_Dir + '/distortionCoeff.npy')

del Calib_Dir


video_name_out = video_name + '_undistorted'

undistor_video(path,video_name,ext,video_name_out,CM,DC)



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





















