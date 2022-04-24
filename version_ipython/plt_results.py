
def plot_timestack_results(timestacks,rectification_parameters, data_filtered, results):
    
    from matplotlib import pyplot as plt
    from matplotlib.gridspec import GridSpec
    from angle2velocity import angle2velocity
    import numpy as np
    from scipy.stats import norm
    from matplotlib.ticker import (MultipleLocator, AutoMinorLocator,FormatStrFormatter,FuncFormatter)
    from tqdm import tnrange
    from itertools import cycle

    
    plt.ioff()
    
    sup_title_fontsize = 15 
    title_fontsize = 10
    label_fontsize = 8
    major_ticks_fontsize = 7
    minor_ticks_fontsize = 5 
    legend_fontsize = 5
    
    def ticks_velocity(value,index):

        tick = angle2velocity(rectification_parameters["Temporal_scale"],rectification_parameters["Dimension_scale"],value)

        return str('%.2f' % tick)

    def ticks_time(value,index):
        
        tick = timestacks["time"][0] + value * rectification_parameters["Temporal_scale"]
        return str('%.f' % tick)
    
    def ticks_distance(value,index):
        tick = value * rectification_parameters["Dimension_scale"]
        return str('%.2f' % tick)

    
    number_timestack = 0
    for k in data_filtered.keys():
        if k.startswith('timestack'):
            number_timestack += 1
            
            
    for t in tnrange(number_timestack):
        
        Angles_filtered = data_filtered["timestack" + str(t)]["Angles_filtered"]
        Angular_density_filtered = data_filtered["timestack" + str(t)]["Angular_density_filtered"]
        theta_max = data_filtered["timestack" + str(t)]["Angle_range"][1]
        theta_min = data_filtered["timestack" + str(t)]["Angle_range"][0]
        v_min = data_filtered["timestack" + str(t)]["Velocity_range"][0]
        v_max = data_filtered["timestack" + str(t)]["Velocity_range"][1]
        Angle_max = data_filtered["timestack" + str(t)]["Peaks"][:,0]
        peak = data_filtered["timestack" + str(t)]["Peaks"][:,1]
        timestack = timestacks["timestack"+str(t)]
        hist_Data = results["timestack" + str(t)]["Hist_data"]
        v_min = data_filtered["timestack" + str(t)]["Velocity_range"][0]
        v_max = data_filtered["timestack" + str(t)]["Velocity_range"][1]

    
#%%
        plt.close('all')
        fig = plt.figure()
        plt.suptitle("Analisis de timestack " + str(t) , fontsize = sup_title_fontsize, 
                     fontweight = 'bold')
    
        
        gs1 = GridSpec(5,6)
        ax1 = plt.subplot(gs1[0,:])
        gs1.update(hspace = 0.7, wspace = 0)
    
        gs2 = GridSpec(5,6)
        ax2 = plt.subplot(gs2[1:,:-2])
        gs2.update(hspace = 0 , wspace = 0.5)
    
    
        gs3 = GridSpec(5,6)
        ax3 = plt.subplot(gs3[1:3,4:])
        gs3.update(hspace = 1 , wspace = 0)
    
        gs4 = GridSpec(5,6)
        ax4 = plt.subplot(gs3[3:,4:])
        gs4.update(hspace = 0 , wspace = 0 )
        
        #%%  AX1 - PLOT TIMESTACK
        

        ax1.imshow(timestack,aspect="auto")
        ax1.xaxis.tick_top()
        ax1.set_title("Timestack" , fontsize = title_fontsize, fontweight = 'bold', y = 1.35)
    
        
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
        
        #%%  AX2 - GRAFICO DE VARIANZA  
    
        marker = [',', '+', '.', 'o', '*']
        marker_cycle = cycle(marker)
        lines = ["-", "--", "-.", ":"]
        linecycler = cycle(lines)
        for k in range(np.shape(Angular_density_filtered)[1]):
            if not np.all(np.isnan( Angular_density_filtered[:,k])):
                ax2.plot(Angles_filtered, Angular_density_filtered[:,k], alpha = 0.4, linestyle = next(linecycler),linewidth = 2,
                     marker = next(marker_cycle), markersize = 8, markevery = 5, label = ('time %s' % k))

            else:
                ax2.plot(Angles_filtered, np.zeros(np.shape(Angles_filtered)[0]) , linestyle='', alpha = 0)

        
        if not np.all(np.isnan(peak)):
            ax2.plot(Angle_max,peak,marker = 'o', markersize = 12, fillstyle='none', linestyle ='',
                         color = 'r',label = "Maximos encontrados")
            
        if not np.all(np.isnan( Angular_density_filtered)):
            ax2.set_ylim(0,  )
        else:
            ax2.set_ylim(0, 1)   
            
    
        ax2_2 = ax2.twiny()
        ax2_2.plot(Angles_filtered,np.zeros(np.shape(Angles_filtered)[0]),linestyle='', alpha = 0) #dummyplot
    
    
        ax2.tick_params(axis = 'both', which='both', width = 2)
        ax2.tick_params(axis = 'x', which = 'minor', length = 4, color='r', labelsize = minor_ticks_fontsize)
        ax2.tick_params(axis = 'x', which='major', length = 5, labelsize = major_ticks_fontsize)
        ax2.tick_params(axis = 'y', which='major', length = 5, labelsize = major_ticks_fontsize)
        ax2.set_xlim(theta_min,theta_max)
        ax2.set_xlabel("Angulo de proyección (deg)", fontsize = label_fontsize, position = (1,0))
        ax2.xaxis.tick_top()
        ax2.set_ylabel('Varianza', fontsize = label_fontsize)
        ax2.xaxis.set_label_position('top')
        ax2.xaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
        ax2.yaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
        ax2.xaxis.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)
        ax2.invert_xaxis()
        
        majorLocator = MultipleLocator(15)
        majorFormatter = FormatStrFormatter('%d')
        minorLocator = AutoMinorLocator()
        ax2.set_title("Densidad Angular" , fontsize = title_fontsize, fontweight = 'bold', y=1.03)
        
        
        ax2.xaxis.set_major_locator(majorLocator)
        ax2.xaxis.set_major_formatter(majorFormatter)
        ax2.xaxis.set_minor_locator(minorLocator)
        
            
        ax2_2.set_xlim(ax2.get_xlim())
        ax2_2.set_xlabel("Velocidad (m/s)", fontsize = label_fontsize)
        ax2_2.xaxis.tick_bottom()
        ax2_2.xaxis.set_label_position('bottom')
    
    
        majorLocator2 = MultipleLocator(15)
        minorLocator2 = AutoMinorLocator()
        ax2_2.xaxis.set_major_locator(majorLocator2)
        ax2_2.xaxis.set_major_formatter(FuncFormatter(ticks_velocity))
        ax2_2.xaxis.set_minor_formatter(FuncFormatter(ticks_velocity))
        ax2_2.xaxis.set_minor_locator(minorLocator2)
    
        ax2_2.tick_params(which='both', width = 2)
        ax2_2.tick_params(which = 'both', length = 7, labelsize = 8)
        ax2_2.tick_params(which='minor', length=4, color='r', labelsize = minor_ticks_fontsize)
    

    
        if not np.all(np.isnan(Angular_density_filtered)):
            ax2.legend(fontsize = legend_fontsize, ncol = 4, fancybox = True, framealpha = 0.3,
                       labelspacing = 1.5, borderpad = 1)
            
        
        #%% AX3 - MUESTRA DE TIMESTACK ESCOGIDO
        
        dist_x = np.shape(rectification_parameters["Rectificated_Image"])[0]*rectification_parameters["Dimension_scale"]
        dist_y = np.shape(rectification_parameters["Rectificated_Image"])[1]*rectification_parameters["Dimension_scale"]
    
        ticks_ax3_x = (np.around(dist_x/5,decimals = 0) if (dist_x/5) > 1 else np.around(dist_x/5,decimals = 1))/rectification_parameters["Dimension_scale"]
        ticks_ax3_y = (np.around(dist_y/5,decimals = 0) if (dist_y/5) > 1 else np.around(dist_y/5,decimals = 1))/rectification_parameters["Dimension_scale"]
        
        majorLocator_ax3_x = MultipleLocator(ticks_ax3_x)
        minorLocator_ax3_x = AutoMinorLocator()
        
        majorLocator_ax3_y = MultipleLocator(ticks_ax3_y)
        minorLocator_ax3_y = AutoMinorLocator()
    
        ax3.xaxis.set_major_locator(majorLocator_ax3_x)
        ax3.xaxis.set_minor_locator(minorLocator_ax3_x)
        ax3.yaxis.set_major_locator(majorLocator_ax3_y)
        ax3.yaxis.set_minor_locator(minorLocator_ax3_y)
    
        ax3.imshow(rectification_parameters["Rectificated_Image"],aspect = 'auto')
        if number_timestack > 1:
            for d in range(number_timestack):
                ax3.plot(timestacks["X"][d,:],timestacks["Y"][d,:],'go-')
            ax3.plot(timestacks["X"][t],timestacks["Y"][t],'ro-')
        else:
            ax3.plot(timestacks["X"],timestacks["Y"],'ro-')
                                
        if "section" in timestacks:
            ax3.plot(timestacks["section"][:,0],timestacks["section"][:,1],'b-', alpha = 0.6)
            
        ax3.xaxis.tick_top()
        ax3.yaxis.tick_left()
        ax3.xaxis.set_major_formatter(FuncFormatter(ticks_distance))
        ax3.yaxis.set_major_formatter(FuncFormatter(ticks_distance))
        ax3.tick_params(which = 'both', width = 2)
        ax3.tick_params(axis = 'both', which = 'major', length = 7, labelsize = major_ticks_fontsize)
        ax3.tick_params(axis = 'both', which = 'minor', length = 4, color = 'r', labelsize = minor_ticks_fontsize)
        
        ax3.xaxis.tick_bottom()
        ax3.set_xlabel("Distancia (m)",fontsize = label_fontsize)
        ax3.xaxis.set_label_position('bottom')
        
        ax3.set_ylabel("Distancia (m)",fontsize = label_fontsize)
        ax3.yaxis.tick_right()
        ax3.yaxis.set_label_position('right')
        
        ax3.set_title("Timestack analizado" , fontsize = title_fontsize, fontweight = 'bold')
        
        

                #%% AX4 - HISTOGRAMA 
        if not results["timestack" + str(t)]["Mean_velocity"] == "No Data Detected":
            n,bins,pathces = ax4.hist(hist_Data[0], bins = hist_Data[1], weights = hist_Data[2], range = hist_Data[3]  , density = True, alpha = 0.6, color = 'g')
    
    
        majorLocator_ax4 = MultipleLocator(0.2)
        minorLocator_ax4 = AutoMinorLocator()
        
        ax4.set_title("Histograma ponderado por Varianza" , fontsize = title_fontsize, fontweight = 'bold')
    
    
        ax4.xaxis.set_major_locator(majorLocator_ax4)
        ax4.xaxis.set_minor_locator(minorLocator_ax4)
        ax4.tick_params(which = 'both', width = 2)
        ax4.tick_params(axis = 'x', which = 'major', length = 7, labelsize = major_ticks_fontsize)
        ax4.tick_params(axis = 'x', which = 'minor', length = 4, color = 'r', labelsize = minor_ticks_fontsize)
        ax4.tick_params(axis = 'y', which = 'major', length = 7, labelsize = major_ticks_fontsize)
        ax4.xaxis.grid(b = True, which = 'major', color = 'k', linestyle='-', alpha = 0.5)
        ax4.yaxis.grid(b = True, which = 'major', color = 'k', linestyle='-', alpha = 0.5)
        ax4.xaxis.grid(b = True, which = 'minor', color = 'r', linestyle='-', alpha = 0.2)
    
        
        ax4.set_xlim(v_min,v_max)
        ax4.set_xlabel("Velocidad (m/s)", fontsize = label_fontsize)
        
    
    
        ax4_2 = ax4.twinx()
        ax4_2.yaxis.set_major_formatter(plt.NullFormatter())
        ax4_2.tick_params(axis = 'y', which = 'both', length = 0, color = 'b', labelsize = 0)
        ax4_2.yaxis.tick_right()
        ax4_2.yaxis.set_label_position('right')
        ax4.yaxis.tick_right()
        ax4.yaxis.set_label_position('right')
        xmin, xmax = ax4.get_xlim()
        mu, std = results["timestack"+str(t)]["Mean_velocity"],results["timestack" + str(t)]["Standard_desviation"]
        x = np.linspace(xmin, xmax, 100)
    
    
        if not results["timestack"+str(t)]["Mean_velocity"] == "No Data Detected":
            p = norm.pdf(x, mu, std)
            ax4_2.plot(x, p, 'k', linewidth=2)
            ax4_2.annotate('Mean Velocity : ' + str(np.around(mu,decimals = 2)) + ' m/s\nStd : ' + str(np.around(std,decimals = 2)) +' m/s',
                           xy=(mu, max(p)), xycoords='data', xytext=(0.95, 0.85), textcoords='axes fraction',
                           arrowprops = dict(arrowstyle="->",connectionstyle="arc3"),
                           horizontalalignment='right', verticalalignment='bottom', fontsize = 8)
            
        fig.savefig("timestack" + str(t) + ".png")


    return