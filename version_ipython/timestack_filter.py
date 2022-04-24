
#v_range : rango de velocidades del filtro

def timestack_filter(processed_timestacks,rectification_parameters,threshold):
    
    from velocity2angle import velocity2angle
    import numpy as np
    from peakdet import peakdet
    import pickle
    from tqdm import tnrange

    
    print("Filtrado de datos")
    print("\nAhora debe ingresar el intervalo de velocidades de interes")
    v_min = float(input("Ingrese velocidad minima : "))
    v_max = float(input("Ingrese velocidad maxima : "))
    v_range = (v_min,v_max)
    
    theta_min = min(velocity2angle(rectification_parameters["Temporal_scale"],rectification_parameters["Dimension_scale"],v_min),
                    velocity2angle(rectification_parameters["Temporal_scale"],rectification_parameters["Dimension_scale"],v_max))
    
    theta_max = max(velocity2angle(rectification_parameters["Temporal_scale"],rectification_parameters["Dimension_scale"],v_min),
                    velocity2angle(rectification_parameters["Temporal_scale"],rectification_parameters["Dimension_scale"],v_max))
    
   
    number_timestack = 0
    
    for k in processed_timestacks.keys():
        if k.startswith('timestack'):
            number_timestack+=1
            
    data_filtered = {}
    
    for t in tnrange(number_timestack):
        
        data_filtered.update({"timestack" +str(t):{"Angular_density_filtered" : "","Angles_filtered" : "",
                                       "Velocity_range" : "" } })
    
        Angles_filtered = processed_timestacks["timestack" + str(t)]["Angles"] [(processed_timestacks["timestack"+str(t)]["Angles"] > theta_min) & 
                            (processed_timestacks["timestack" + str(t)]["Angles"] < theta_max) ]
    
    # Densidad angular restringida a los limites de velocidad pre-establecidos
        Restricted_Angular_Density = processed_timestacks["timestack" + str(t)]["Angular_density"][(processed_timestacks["timestack"+str(t)]["Angles"] > theta_min) & 
                            (processed_timestacks["timestack" + str(t)]["Angles"] < theta_max) ]
        

    
        Angle_max_t = list() # Angulo donde se maximiza la varianza para cada uno de los timestacks pequeños
        peak_t = list() # Valor de la varianza para el angulo que la maximiza
    
        for k in range(np.shape(Restricted_Angular_Density)[1]):
            
            maxpeaks_k, _ = peakdet(Restricted_Angular_Density[:,k], 10000)
            
            if maxpeaks_k.size :
                max_peak_k = np.max(maxpeaks_k[:,1])
                thetas_max_k = Angles_filtered[maxpeaks_k[:,0][maxpeaks_k[:,1] == np.max(maxpeaks_k[:,1])].astype(int)]
            else:
                max_peak_k = np.nan
                thetas_max_k = np.nan
                    
                   
            Angle_max_t.append(thetas_max_k)
            peak_t.append(max_peak_k)
        
            
    #FILTRADO POR MAXIMO DE MAXIMOS RELATIVOS

    
        Angle_max_t = np.asarray(Angle_max_t).astype('float64')
        peak_t = np.asarray(peak_t).astype('float64')
    
    
        Angle_max_t_filtered = np.copy(Angle_max_t)
        peak_t_filtered = np.copy(peak_t)
    
    #Aca detecto el angulo y los picos para luego graficarlos
        Angle_max_t_filtered = np.asarray( [ Angle_max_t[t] if peak_t[t]> threshold else np.nan for t in range(len(Angle_max_t))],dtype = np.float64)        
        peak_t_filtered = np.asarray( [ peak_t[t] if peak_t[t]> threshold else np.nan for t in range(len(Angle_max_t))],dtype = np.float64)
    
        Peaks = np.column_stack([Angle_max_t_filtered,peak_t_filtered])
        Peaks[ np.logical_or((Peaks[:,0] == min(Angles_filtered)),(Peaks[:,0] == max(Angles_filtered)))] = np.nan #Descarto maximos en los extremos
    
        Angular_density_filtered = np.copy(Restricted_Angular_Density)
        
    
    #Aca vuelvo nan toda la fila en la cual su maximo este por debajo del threshhold
        index =np.where(np.isnan(Peaks[:,1]))
        Angular_density_filtered[:,index] = np.nan
            
            
        data_filtered["timestack" + str(t)]["Angular_density_filtered"] = Angular_density_filtered
        data_filtered["timestack" + str(t)]["Angles_filtered"] = Angles_filtered
        data_filtered["timestack" + str(t)]["Peaks"] = Peaks
        data_filtered["timestack" + str(t)]["Velocity_range"] = v_range
        data_filtered["timestack" + str(t)]["Angle_range"] = (theta_min,theta_max)
        
    with open('data_filtered.dat', 'wb') as outfile:
        pickle.dump(data_filtered, outfile, protocol = pickle.HIGHEST_PROTOCOL)
        
    return data_filtered