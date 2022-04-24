                    #%% DIAGRAMACION DE LA HOJA
    
#COMANDOS DE SEPARACION ENTRE SUBPLOTS   
#left : The left side of the subplots of the figure.
#right : The right side of the subplots of the figure.
#bottom : The bottom of the subplots of the figure.
#top : The top of the subplots of the figure.
#wspace : The amount of width reserved for space between subplots, expressed as a fraction of the average axis width.
#hspace : The amount of height reserved for space between subplots, expressed as a fraction of the average axis height.


    
    #timestack: timestack completo
    #overlap: overlaping en el procesamiento
    #time: referencia al progreso del procesamiento
    #timestack_j: porcion del timestack que se esta procesando
    #sinogram: transformada de radon para el instante de tiempo
    #figsize : tamaño de la figura en pulgadas
    #print_flag: bandera para ver si quiero guardar las archivos
    
        

#%%

def plot_timestack_individual(timestacks, rectification_parameters, data_filtered, processed_timestacks):
    
    from matplotlib import pyplot as plt
    from matplotlib.gridspec import GridSpec
    import matplotlib.patches as patches
    from matplotlib.ticker import (MultipleLocator, AutoMinorLocator,FormatStrFormatter,FuncFormatter)
    import numpy as np
    import os
    from angle2velocity import angle2velocity
    from pathlib import Path
    from tqdm import tnrange

    
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

    def ticks_time_slice(value,index):
        tick = timestacks["time"][0] + ( int(time * m * (1 - (overlaping/100)))+ value ) * rectification_parameters["Temporal_scale"]
        return str('%.f' % tick)

    
    original_path = Path(os.getcwd())
    
    number_timestack = 0
    for k in data_filtered.keys():
        if k.startswith('timestack'):
            number_timestack+=1



    
    for t in tnrange(number_timestack, desc = '1st loop'):
        new_path = original_path / ("individual_plots_timestack" + str(t))
        if not os.path.exists(str(new_path)):
            os.makedirs(str(new_path))
            
        os.chdir(new_path)

    
        timestack = timestacks["timestack" + str(t)]
        Angles_filtered = data_filtered["timestack" + str(t)]["Angles_filtered"]
        theta_max = data_filtered["timestack" + str(t)]["Angle_range"][1]
        theta_min = data_filtered["timestack" + str(t)]["Angle_range"][0]
        overlaping = processed_timestacks["overlaping"]

        
        try: # ESTA PARTE ES CUANDO ELIJO UN TIEMPO DE PROCESAMIENTO MAYOR EN LOS TIMESTACKS INDIVIDUALES
            np.any(processed_timestacks["timestack" + str(t)]["New_timestack"])
            m, n = np.shape(processed_timestacks["timestack" + str(t)]["New_timestack"])
        except:
            m, n = np.shape(timestack)
                        

    
        for time in tnrange(np.shape(processed_timestacks["timestack" + str(t)]["Angular_density"])[1],desc ='2nd loop', leave = False):
            
            plt.close('all')
            
            Angular_density = data_filtered["timestack" + str(t)]["Angular_density_filtered"][:,time]
            Angle_max = data_filtered["timestack" + str(t)]["Peaks"][time,0]
            peak = data_filtered["timestack" + str(t)]["Peaks"][time,1]
                
            Sinogram = processed_timestacks["timestack" + str(t)]["Sinogram"][:,:,time]
            Individual_timestack = processed_timestacks["timestack" + str(t)]["Individual_timestacks"][:,:,time]
            max_ax2 =  np.nanmax(data_filtered["timestack" + str(t)]["Angular_density_filtered"]) + 100000
            min_ax2 =  np.nanmin(data_filtered["timestack" + str(t)]["Angular_density_filtered"])
        
            

#%%
            fig = plt.figure()
            plt.suptitle("Análisis timestack individual de timestack" + str(t),fontsize = sup_title_fontsize)
        
        
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
                            
            #%%  AX1 - PLOTEO TIMESTACK
            
            ax1.imshow(timestack, aspect = "auto")
            rect = patches.Rectangle((int(time * m * (1 - (overlaping/100))),0), m, m, linewidth=1, 
                                     edgecolor='r', facecolor='none')
            ax1.add_patch(rect)
            ax1.set_title("Timestack" , fontsize = title_fontsize, fontweight = 'bold', y= 1.35)
        
            
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
            
            #%%  AX2 - GRAFICO DE VARIANZA
            marker_list = [',', '+', '.', 'o', '*']
            line_list = ["-", "--", "-.", ":"]
            color_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
            
            markers = np.tile(marker_list,np.ceil(np.shape(data_filtered["timestack" + str(t)]["Angular_density_filtered"])[1]/len(marker_list)).astype('int'))
            lines = np.tile(line_list,np.ceil(np.shape(data_filtered["timestack" + str(t)]["Angular_density_filtered"])[1]/len(line_list)).astype('int'))
            colors = np.tile(color_list,np.ceil(np.shape(data_filtered["timestack" + str(t)]["Angular_density_filtered"])[1]/len(color_list)).astype('int'))
        
            if not np.all(np.isnan(Angular_density)):
                ax2.plot(Angles_filtered, Angular_density,alpha = 0.6, linestyle = lines[time], linewidth = 2 ,
                         marker = markers[time], color = colors[time], markersize = 8, 
                         markevery = 5,label = "time {:.0f}" .format(time) )
                ax2.plot(Angle_max,peak,marker = 'o', markersize = 12, fillstyle='none', linestyle ='',
                         color = 'r',label = "Maximo encontrados")
                
                ax2.legend(fontsize = legend_fontsize, ncol = 4, fancybox = True, framealpha = 0.3,
                           labelspacing = 1.5, borderpad = 1)
                
                ax2.set_ylim(min_ax2, max_ax2)   

            else:
                ax2.plot(Angles_filtered,np.zeros(np.shape(Angles_filtered)[0]),linestyle='', alpha = 0)
                ax2.set_ylim(0, 1)   
                            
            
            ax2_2 = ax2.twiny()
            ax2_2.plot(Angles_filtered,np.zeros(np.shape(Angles_filtered)[0]),linestyle='', alpha = 0) #dummyplot
        
        
        
            majorLocator = MultipleLocator(15)
            majorFormatter = FormatStrFormatter('%d')
            minorLocator = AutoMinorLocator()
            ax2.set_title("Densidad Angular" , fontsize = title_fontsize, fontweight = 'bold', y=1.03)
        
        
            ax2.xaxis.set_major_locator(majorLocator)
            ax2.xaxis.set_major_formatter(majorFormatter)
            ax2.xaxis.set_minor_locator(minorLocator)
            ax2.tick_params(axis = 'both', which='both', width = 2)
            ax2.tick_params(axis = 'x', which = 'minor', length = 4, color='r', labelsize = minor_ticks_fontsize)
            ax2.tick_params(axis = 'x', which='major', length = 5, labelsize = major_ticks_fontsize)
            ax2.tick_params(axis = 'y', which='major', length = 5, labelsize = major_ticks_fontsize)
            ax2.set_xlim(theta_min,theta_max)
            ax2.set_xlabel("Angulo de proyección (deg)", fontsize = label_fontsize, position = (0,0))
            ax2.xaxis.tick_top()
            ax2.set_ylabel('Varianza', fontsize = label_fontsize)
            ax2.xaxis.set_label_position('top')
            ax2.xaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
            ax2.yaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
            ax2.xaxis.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)
            ax2.invert_xaxis()
        
        
            majorLocator2 = MultipleLocator(15)
            minorLocator2 = AutoMinorLocator()
            ax2_2.xaxis.set_major_locator(majorLocator2)
            ax2_2.xaxis.set_major_formatter(FuncFormatter(ticks_velocity))
            ax2_2.xaxis.set_minor_formatter(FuncFormatter(ticks_velocity))
            ax2_2.xaxis.set_minor_locator(minorLocator2)
        
            ax2_2.tick_params(which = 'both',  width = 2)
            ax2_2.tick_params(which = 'major', length = 7, labelsize = major_ticks_fontsize)
            ax2_2.tick_params(which = 'minor', length = 4, color='r', labelsize = minor_ticks_fontsize)
        
        
            ax2_2.set_xlim(ax2.get_xlim())
            ax2_2.set_xlabel("Velocidad (m/s)", fontsize = label_fontsize)
            ax2_2.xaxis.tick_bottom()
            ax2_2.xaxis.set_label_position('bottom')
            
            
            #%%  AX3 - TROZO DE TIMESTACK
            
            ax3.imshow(Individual_timestack , cmap = plt.cm.Greys_r, aspect = 'auto')
            
            max_dist_slice =         np.shape(Individual_timestack)[0]*rectification_parameters["Dimension_scale"]
            length_timestack_slice = np.shape(Individual_timestack)[1]*rectification_parameters["Temporal_scale"]
        
            ticks_ax3_y = (np.around(max_dist_slice/5,decimals = 0) if (max_dist_slice/5) > 1 else np.around(max_dist_slice/5,decimals = 1))/rectification_parameters["Dimension_scale"]
            ticks_ax3_x = (np.around(length_timestack_slice/8,decimals = 0) if (length_timestack_slice/8) > 1 else np.around(length_timestack_slice/8,decimals = 1))/rectification_parameters["Temporal_scale"]
        
            
            majorLocator_ax3_xaxis = MultipleLocator(ticks_ax3_x)
            minorLocator_ax3_xaxis = AutoMinorLocator()
            ax3.xaxis.set_major_locator(majorLocator_ax3_xaxis)
            ax3.xaxis.set_minor_locator(minorLocator_ax3_xaxis)
            
            majorLocator_ax3_yaxis = MultipleLocator(ticks_ax3_y)
            minorLocator_ax3_yaxis = AutoMinorLocator()
            ax3.yaxis.set_major_locator(majorLocator_ax3_yaxis)
            ax3.yaxis.set_minor_locator(minorLocator_ax3_yaxis)
            
            ax3.yaxis.set_major_formatter(FuncFormatter(ticks_distance))
            ax3.xaxis.set_major_formatter(FuncFormatter(ticks_time_slice))
            
            ax3.tick_params(which = 'both', width = 2)
            ax3.tick_params(axis = 'both', which = 'major', length = 7, labelsize = major_ticks_fontsize)
            ax3.tick_params(axis = 'both', which = 'minor', length = 4, color = 'r', labelsize = minor_ticks_fontsize)
            
            ax3.xaxis.tick_bottom()
            ax3.set_xlabel("Tiempo (s)",fontsize = label_fontsize)
            ax3.xaxis.set_label_position('bottom')
            
            ax3.set_ylabel("Distancia (m)",fontsize = label_fontsize)
            ax3.yaxis.tick_right()
            ax3.yaxis.set_label_position('right')
            
            ax3.set_title("Trozo de timestack analizado" , fontsize = title_fontsize, fontweight = 'bold')
                
            #%%  AX4 - SINOGRAMA - RESULTADO RADON
            
            ax4.imshow(Sinogram,extent=(0, 180, 0, Sinogram.shape[0]), aspect='auto')
            ax4.set_title("Transformada de Radon : (Sinograma)" , fontsize = title_fontsize, fontweight = 'bold')
            
            ax4.tick_params(which = 'both', width = 2)
            ax4.tick_params(axis = 'both', which = 'major', length = 7, labelsize = major_ticks_fontsize)
            ax4.tick_params(axis = 'both', which = 'minor', length = 4, color = 'r', labelsize = minor_ticks_fontsize)
            
            ax4.xaxis.tick_bottom()
            ax4.set_xlabel("Angulo de proyección (deg)", fontsize = label_fontsize)
            ax4.xaxis.set_label_position('bottom')
            
            ax4.set_ylabel("Posicion de proyección (pixels)", fontsize = label_fontsize)
            ax4.yaxis.tick_right()
            ax4.yaxis.set_label_position('right')
            
            fig.savefig("timestack" + str(t) + "_" + str(time) + ".png")



        os.chdir(str(original_path))

    return