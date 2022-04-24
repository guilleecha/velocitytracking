def data_results(data_filtered,rectification_parameters):
    
    import numpy as np
    from angle2velocity import angle2velocity
    from scipy.stats import norm
    import pickle
    
    number_timestack = 0
    for k in data_filtered.keys():
        if k.startswith('timestack'):
            number_timestack+=1
            
    results = {}
    
    for t in np.arange(number_timestack):
        results.update({"timestack" +str(t):{"Velocity_peaks": "","Median_velocity" : "","Mean_weighted_velocity": "",
                        "Mean_velocity" : "", "Standard_desviation" : "", "Hist_data": ""}})


        velocity_peaks = np.around(angle2velocity(rectification_parameters["Temporal_scale"],rectification_parameters["Dimension_scale"],
                                             data_filtered["timestack" + str(t)]["Peaks"][:,0]), decimals = 2)
        
        indices = np.where(np.logical_not(np.isnan(velocity_peaks)))[0] # indices donde no son NaN
        Peaks = data_filtered["timestack" + str(t)]["Peaks"][indices,1]
#        Angles = data_filtered["timestack" + str(t)]["Peaks"][indices,0]
        data_4_adjust = []
        if velocity_peaks[indices].any():
            weights = Peaks**2
            mean_weighted_velocity = np.average(velocity_peaks[indices], weights = weights)
            hist_range = data_filtered["timestack" + str(t)]["Velocity_range"]
            bins_number = int((hist_range[1]-hist_range[0])/.01)
            hist, bins = np.histogram (velocity_peaks[indices],density = True,bins = bins_number , weights = weights, range = hist_range )
            
            for k in np.arange(len(hist)):
                if hist[k]!= 0 :
                    aux = np.repeat(bins[k], np.round(100 * (hist[k]/np.nansum(hist))).astype('int') )
                    data_4_adjust.append(aux)
            data_4_adjust = [item for sublist in data_4_adjust for item in sublist]
#            _, bins = np.histogram (data_4_hist, bins = 'auto' , density = True)#


            mean_velocity, Standard_desviation = norm.fit(data_4_adjust)
            median_velocity = np.nanmedian(velocity_peaks)
            
            results["timestack" + str(t)]["Velocity_peaks"] = velocity_peaks
            results["timestack" + str(t)]["Mean_weighted_velocity"] = np.around(mean_weighted_velocity, decimals = 2)
            results["timestack" + str(t)]["Mean_velocity"] = mean_velocity
            results["timestack" + str(t)]["Standard_desviation"] = Standard_desviation
            results["timestack" + str(t)]["Median_velocity"] = median_velocity
            results["timestack" + str(t)]["Hist_data"] = [velocity_peaks[indices] ,bins_number, weights, hist_range]

        else:
            results["timestack" + str(t)]["Velocity_peaks"] = "No Data Detected"
            results["timestack" + str(t)]["Mean_weighted_velocity"] = "No Data Detected"
            results["timestack" + str(t)]["Mean_velocity"] = "No Data Detected"
            results["timestack" + str(t)]["Standard_desviation"] = "No Data Detected"
            results["timestack" + str(t)]["Median_velocity"] = "No Data Detected"
            results["timestack" + str(t)]["Hist_data"] = "No Data Detected"


    with open('results.dat', 'wb') as outfile:
        pickle.dump(results, outfile, protocol = pickle.HIGHEST_PROTOCOL)
        
    return results
        
