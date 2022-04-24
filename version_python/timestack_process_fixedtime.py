
def timestack_process_fixedtime(timestacks,overlaping,rectification_parameters):
    
    from createCircularMask import createCircularMask
    import numpy as np
    from skimage.transform import radon
    import pickle
    from scipy.ndimage.filters import gaussian_filter, median_filter


    # overlaping [%]  : intervalo de sobrelapamiento de los timestacks en porcentaje
    # intervalo de tiempo que quiero analizar los pequeños timestacks
    
    print("\nAgregar un filtro a los timestacks")
    print("\nIngrese el numero de la opcion deseada : \n1: Filtro Gaussiano\n2 : Filtro de mediana\n3: Sin filtro")   
    while True:
        option = (input("Opcion : "))
        try:
            if option == '1':
                blur_flag = True
                sigma = int(input("Ingresar el alcance del filtro en px : "))
                break
            elif option == '2':
                median_flag = True
                sigma = int(input("Ingresar el alcance del filtro en px : "))
                blur_flag = False
                break
            elif option == '3':
                blur_flag = False
                median_flag = False
                break
            else:
                print("No presiono alguna de las opciones")
                pass
        except:
            break
        
    processed_timestacks = {}
    processed_timestacks["Description"] = '''Estructura que contiene informacion y resultados del procesamiento
de los distintos timestacks (Radon,Fourier,etc) '''

    number_timestack = 0
    m, n = np.shape(timestacks["timestack0"])
    interval_fix = float(input("\nSeleccione duracion en [seg] mayor a %.1f seg para el analisis de timestacks individuales : " 
                                 % (m * rectification_parameters["Temporal_scale"])))
    
    length_individual_timestack = int(interval_fix / rectification_parameters["Temporal_scale"])
    
    for k in timestacks.keys():
        if k.startswith('timestack'):
            number_timestack+=1

    for t in range(number_timestack):
            
        processed_timestacks.update({"timestack" + str(t):{"Sinogram" : "","Fourier_Spec" : "","Angles" : "", 
                                     "Individual_timestacks" : "", "New_timestack" : " "}})
        
        if blur_flag:
            processed_timestacks['timestack' + str(t)]["Blurred_timestack"] = gaussian_filter(timestacks['timestack' + str(t)], sigma)
            processed_timestacks['timestack' + str(t)]["Sigma"] = sigma
            timestack = processed_timestacks['timestack' + str(t)]["Blurred_timestack"]
        elif median_flag:
            processed_timestacks['timestack' + str(t)]["Blurred_timestack"] = median_filter(timestacks['timestack' + str(t)], sigma)
            processed_timestacks['timestack' + str(t)]["Sigma"] = sigma
            timestack = processed_timestacks['timestack' + str(t)]["Blurred_timestack"]
        
        else:
            timestack = timestacks["timestack" + str(t)]
            
            m, n = np.shape(timestack)
       
        
        if length_individual_timestack >= m:
            
            new_timestack = np.resize(timestack, (length_individual_timestack,n))
                        
            m, n = np.shape(new_timestack)
            times = int(np.floor(n/m))
            overlap_times = int(times/((100-overlaping)/100))
            
            if m * ( (times) +(1-(overlaping/100))) > n:
                overlap_times = overlap_times - 1 
                

            sinogram = np.zeros((m, m, overlap_times))
            Individual_timestacks = np.zeros((m, m, overlap_times))
            Angular_density = np.zeros((m, overlap_times))
            Fourier_spec = np.zeros((m, m, overlap_times))
            mask = createCircularMask(m, m)
            
            
            
            for j in range(overlap_times):
                    
                print('Progreso de timestack '+ str(t) + ': %.1f' % ((j/(overlap_times))*100) + '%' )
                timestack_j = new_timestack [:,int(j* m * (1 - (overlaping/100))):int(( 1 + j*(1- (overlaping/100)))*m)]
                Individual_timestacks[:,:,j] = timestack_j
                timestack_masked = timestack_j * mask
                theta = np.linspace(0., 180., max(timestack_masked.shape), endpoint = False)
                
                sinogram[:,:,j] = radon(timestack_masked, theta = theta, circle = True)
                Angular_density[:,j] = np.var(sinogram[:,:,j], axis=0)
                    
                F = np.fft.fft2(timestack_j)
                F = np.abs(F)
                Fourier_spec[:,:,j]=np.fft.fftshift(F)
            print('Progreso de timestack '+ str(t) + ': %.1f' % (100) + '%' )

            processed_timestacks["timestack" + str(t)]["Fourier_Spec"] = Fourier_spec
            processed_timestacks["timestack" + str(t)]["Sinogram"] = sinogram
            processed_timestacks["timestack" + str(t)]["Angular_density"] = Angular_density
            processed_timestacks["timestack" + str(t)]["Angles"] = theta
            processed_timestacks["timestack" + str(t)]["Individual_timestacks"] = Individual_timestacks
            processed_timestacks["timestack" + str(t)]["New_timestack"] = new_timestack
            
        else:
            print('\nDebe seleccionar un tiempo mayor para el analisis de los timestacks individuales')

        

    processed_timestacks["overlaping"] = overlaping
    with open('Processed_timestacks.dat', 'wb') as outfile:
        pickle.dump(processed_timestacks, outfile, protocol = pickle.HIGHEST_PROTOCOL)

        
        
    return processed_timestacks