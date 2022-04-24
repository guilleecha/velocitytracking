def results(Data_filtered,rectification_parameters):
    import numpy as np
    from angle2velocity import angle2velocity
    from scipy.stats import norm
    import pickle
    
    number_timestack = 0
    for k in Data_filtered.keys():
        if k.startswith('timestack'):
            number_timestack+=1
            
    Results = {}
    
    for t in range(number_timestack):
        Results.update({"timestack" +str(t):{"Velocity_peaks": "","Median_velocity" : "",
                        "Mean_velocity" : "", "Standard_desviation" : ""}})

        
        if Data_filtered["timestack" + str(t)]["Peaks"].any():
            
            velocity_peaks = angle2velocity(rectification_parameters["Temporal_scale"],rectification_parameters["Dimension_scale"],
                                             Data_filtered["timestack" + str(t)]["Peaks"][:,0])
        
            mean_velocity, Standard_desviation = norm.fit(velocity_peaks)
            median_velocity = np.median(velocity_peaks)
            
            Results["timestack" + str(t)]["Velocity_peaks"] = velocity_peaks    
            Results["timestack" + str(t)]["Mean_velocity"] = mean_velocity
            Results["timestack" + str(t)]["Standard_desviation"] = Standard_desviation
            Results["timestack" + str(t)]["Median_velocity"] = median_velocity
            
              
        else:
            Results["timestack" + str(t)]["Velocity_peaks"] = "No Data Detected"
            Results["timestack" + str(t)]["Mean_velocity"] = "No Data Detected"
            Results["timestack" + str(t)]["Standard_desviation"] = "No Data Detected"
            Results["timestack" + str(t)]["Median_velocity"] = "No Data Detected"

    with open('Results.dat', 'wb') as outfile:
        pickle.dump(Results, outfile, protocol = pickle.HIGHEST_PROTOCOL)
        
    return Results
        
