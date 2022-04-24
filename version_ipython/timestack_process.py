
def timestack_process(timestacks,overlaping,rectification_parameters):
    
    from createCircularMask import createCircularMask
    import numpy as np
    from skimage.transform import radon
    import pickle
    from tqdm import tnrange
    from scipy.ndimage.filters import gaussian_filter, median_filter


# overlaping [%]  : intervalo de sobrelapamiento de los timestacks en porcentaje


    print("\nAgregar un filtro a los timestacks")
    print("\nIngrese el numero de la opcion deseada : \n1 : Filtro Gaussiano\n2 : Filtro de mediana\n3 : No")   
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
    
    Processed_timestacks = {}
    Processed_timestacks["Description"] = '''Estructura que contiene informacion y resultados del procesamiento
de los distintos timestacks (Radon,Fourier,etc) '''

        
    number_timestack = 0
    
    for k in timestacks.keys():
        if k.startswith('timestack'):
            number_timestack+=1
            




    for t in tnrange(number_timestack,desc = '1st loop'):
        Processed_timestacks.update({"timestack" + str(t):{"Sinogram" : "", 
                                     "Fourier_Spec" : "", "Angles" : "", "Individual_timestacks" : ""}})
            

        if blur_flag:
            Processed_timestacks['timestack' + str(t)]["Blurred_timestack"] = gaussian_filter(timestacks['timestack' + str(t)], sigma)
            Processed_timestacks['timestack' + str(t)]["Sigma"] = sigma
            timestack = Processed_timestacks['timestack' + str(t)]["Blurred_timestack"]
        elif median_flag:
            Processed_timestacks['timestack' + str(t)]["Blurred_timestack"] = median_filter(timestacks['timestack' + str(t)], sigma)
            Processed_timestacks['timestack' + str(t)]["Sigma"] = sigma
            timestack = Processed_timestacks['timestack' + str(t)]["Blurred_timestack"]
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
            
            
            for j in tnrange(overlap_times,desc = '2nd loop', leave = False):

    
                timestack_j = timestack [:,int(j* m * (1 - (overlaping/100))):int(( 1 + j*(1- (overlaping/100)))*m)]
                Individual_timestacks[:,:,j] = timestack_j
                image = timestack_j * mask
                
    
                theta = np.linspace(0., 180., max(image.shape), endpoint = False)
                
                sinogram[:,:,j] = radon(image, theta=theta, circle=True)
                Angular_density[:,j] = np.var(sinogram[:,:,j], axis = 0)
                    
                F = np.fft.fft2(timestack_j)
                F = np.abs(F)
                Fourier_spec[:,:,j] = np.fft.fftshift(F)
            
            Processed_timestacks["timestack" + str(t)]["Fourier_Spec"] = Fourier_spec
            Processed_timestacks["timestack" + str(t)]["Sinogram"] = sinogram
            Processed_timestacks["timestack" + str(t)]["Angular_density"] = Angular_density
            Processed_timestacks["timestack" + str(t)]["Angles"] = theta
            Processed_timestacks["timestack" + str(t)]["Individual_timestacks"] = Individual_timestacks
            Processed_timestacks["overlaping"] = overlaping
        else:
            print('El timestack es muy corto o la transecta es muy larga')
       
    with open('Processed_timestacks.dat', 'wb') as outfile:
        pickle.dump(Processed_timestacks, outfile, protocol = pickle.HIGHEST_PROTOCOL)
        
    return Processed_timestacks