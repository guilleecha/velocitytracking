
def timestack_process(timestacks,overlaping,rectification_parameters):
    
    from createCircularMask import createCircularMask
    import numpy as np
    from skimage.transform import radon
    import pickle
    from scipy.ndimage.filters import gaussian_filter, median_filter


# overlaping [%]  : intervalo de sobrelapamiento de los timestacks en porcentaje


    print("\nAgregar un filtro a los timestacks")
    print("\nIngrese el numero de la opcion deseada : \n1 : Filtro Gaussiano\n2 : Filtro de mediana\n3 : Sin filtro")   
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
    
    for k in timestacks.keys():
        if k.startswith('timestack'):
            number_timestack+=1
            




    for t in range(number_timestack):
        processed_timestacks.update({"timestack" + str(t):{"Sinogram" : "", 
                                     "Fourier_Spec" : "", "Angles" : "", "Individual_timestacks" : ""}})
            

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
            
        if n > m:
            times = int(np.floor(n/m))
        
                
            overlap_times = int(times/((100-overlaping)/100))
        
            if m * ( (times) +(1-(overlaping/100))) > n:
                overlap_times = overlap_times - 1 
            
            sinogram = np.zeros((m,m,overlap_times))
            Individual_timestacks = np.zeros((m,m,overlap_times))
            Angular_density = np.zeros((m,overlap_times))
            Fourier_spec = np.zeros((m,m,overlap_times))
            mask = createCircularMask(m,m)            
            
            
            for j in range(overlap_times):

                print('Progreso de timestack '+ str(t) +': %.1f' % ((j/overlap_times)*100) + '%' )
                timestack_j = timestack [:,int(j* m * (1 - (overlaping/100))):int(( 1 + j*(1- (overlaping/100)))*m)]
                Individual_timestacks[:,:,j] = timestack_j
                image = timestack_j * mask
                
#                theta_aux = np.logspace(.001,1,max(image.shape)/2,endpoint = True,base= 91)-1
#                theta_aux_2 = 180 - np.flip(theta_aux[:-1:])
#                if max(image.shape)%2:
#                    theta = np.hstack((np.array([0]),theta_aux,theta_aux_2,theta_aux_2[-1]))
#                else:
#                    theta = np.hstack((np.array([0]),theta_aux,theta_aux_2))
    
                theta = np.linspace(0., 180., max(image.shape), endpoint = False)
                
                sinogram[:,:,j] = radon(image, theta=theta, circle=True)
                Angular_density[:,j] = np.var(sinogram[:,:,j], axis = 0)
                    
                F = np.fft.fft2(timestack_j)
                F = np.abs(F)
                Fourier_spec[:,:,j] = np.fft.fftshift(F)
            
            processed_timestacks["timestack" + str(t)]["Fourier_Spec"] = Fourier_spec
            processed_timestacks["timestack" + str(t)]["Sinogram"] = sinogram
            processed_timestacks["timestack" + str(t)]["Angular_density"] = Angular_density
            processed_timestacks["timestack" + str(t)]["Angles"] = theta
            processed_timestacks["timestack" + str(t)]["Individual_timestacks"] = Individual_timestacks
            processed_timestacks["overlaping"] = overlaping
        else:
            print('El timestack es muy corto o la transecta es muy larga')
       
    with open('Processed_timestacks.dat', 'wb') as outfile:
        pickle.dump(processed_timestacks, outfile, protocol = pickle.HIGHEST_PROTOCOL)
        
    return processed_timestacks