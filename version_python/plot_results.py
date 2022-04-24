import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator,FormatStrFormatter)
from matplotlib.lines import Line2D

def plot_results(timestacks,rectification_parameters, data_filtered, results):
    number_timestack = 0
    for k in data_filtered.keys():
        if k.startswith('timestack'):
            number_timestack+=1
            
    cmap = cm.get_cmap('Set1')

    def choose_color(std):
        if std >= 0.20:
             color = cmap(0)
        elif 0.15 < std < 0.2 :
             color = cmap(0.25)
        elif 0.10 < std <= .15:
            color = cmap (0.5)
        elif 0.05 < std <= 0.10:
            color = cmap(0.75)
        elif 0 < std <= 0.05:
            color = cmap(1)
        return color
        
    
    title_fontsize = 10
    label_fontsize = 8
    major_ticks_fontsize = 7
    minor_ticks_fontsize = 5 


        
    dist = [np.hypot(timestacks["X"][t+1,0]-timestacks["X"][t,0], timestacks["Y"][t+1,0]-timestacks["Y"][t,0]) for t in range(number_timestack-1)]
    acumulate = 0
    dist_acumulate = [0]
    for dist_px in dist:
        acumulate+=dist_px
        dist_acumulate.append(acumulate*rectification_parameters["Dimension_scale"])
            
    dist_acumulate = np.asarray(dist_acumulate,dtype = np.float)
           
    mean_velocity_stack = []
    std_stack = []
    fig,ax = plt.subplots()        
    for t in range(number_timestack):
        
        mean_velocity = results["timestack" + str(t)]["Mean_velocity"]
        mean_velocity_stack.append(mean_velocity)
        std = results["timestack" + str(t)]["Standard_desviation"]
        std_stack.append(std)
        marker, cap, bars = ax.errorbar(dist_acumulate[t], mean_velocity, yerr = std , fmt='-o', color = 'k' , ecolor = choose_color(std),capsize = 5,fillstyle = 'none')
        ax.annotate('Mean Velocity : {:.2f} m/s\nStd : {:.2f} m/s' .format(mean_velocity,std) ,
                    xy=(dist_acumulate[t]-.2,mean_velocity+std + .01),xytext =(dist_acumulate[t]-0.2,
                       mean_velocity+std + 0.01), ha = 'left', fontsize = 5)
        
    mean_velocity_stack = np.asarray(mean_velocity_stack, dtype = np.float)
    ax.plot(dist_acumulate,mean_velocity_stack,linestyle = '-',color = 'k',alpha = 0.5)

    majorLocator = MultipleLocator(0.5)
    majorFormatter = FormatStrFormatter('%.1f')
    minorLocator = AutoMinorLocator()
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    ax.tick_params(axis = 'both', which='both', width = 2)
    ax.tick_params(axis = 'x', which='major', length = 5, labelsize = major_ticks_fontsize)
    ax.tick_params(axis = 'y', which='major', length = 5, labelsize = major_ticks_fontsize)
    ax.tick_params(which = 'minor', length = 4, color='r')
    ax.xaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
    ax.yaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
    ax.xaxis.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)
    ax.set_xlabel("Distancia (m)", fontsize = label_fontsize)
    ax.set_ylabel("Velocidad (m/s)", fontsize = label_fontsize)

    legend_elements = [Line2D([0], [0], color=cmap(0),    lw = 4, label='Rango : > 0.20 m/s'),
                       Line2D([0], [0], color=cmap(0.25), lw = 4, label='Rango : [0.15 - 0.20) m/s'),
                       Line2D([0], [0], color=cmap(0.5),  lw = 4, label='Rango : [0.10 - 0.15) m/s'),
                       Line2D([0], [0], color=cmap(0.75), lw = 4, label='Rango : [0.05 - 0.10) m/s'),
                       Line2D([0], [0], color=cmap(0.99), lw = 4, label='Rango : [0 - 0.05) m/s')]
    ax.legend(handles=legend_elements, title = "Rangos de desviacion estandar", fontsize = 'small')
    ax.set_xlim(right = dist_acumulate[-1]+.5)
    

    
    plt.show()
    
    
    return