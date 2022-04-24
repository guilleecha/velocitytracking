def time_stack(video,rectification_parameters):
    
    # frame_rate : frame_rate deseado. No puede ser mayor al del video
    # CM : CalibrationMatrix
    # DC : Distorssion Coeeficiente
    # time_start : tiempo de comienzo del time-stack en el video [s]
    # time_stop : tiempo de fin del time-stack en el video [s]
    # rect_par : Resultados de rectificacion
    
    import numpy as np
    import matplotlib.pyplot as plt
    import cv2 #opencv
    import os
    from pathlib import Path
    import time
    import pickle
    from tqdm import tqdm_notebook
      
    start = time.process_time()
        
    oldpath = Path(os.getcwd())
        
#    os.chdir(path)
    vidcap = cv2.VideoCapture(video)
    fps = np.floor(vidcap.get(cv2.CAP_PROP_FPS))
    frameCount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    length_video = frameCount/fps
    
    print("\nEl video tiene un largo de " + str(np.round(length_video*10)/10) + " segundos")
    print("\nIngrese el numero de la opcion deseada : \n1: Utilizar todo el video \n2: Ingresar intervalo")

    while True:
        option = (input("Opcion : "))
        try:
            if option == '1':
                time_start = 0 
                time_stop = length_video
                break
            elif option == '2':
                time_start = float(input("\nIngresar comienzo de intervalo de procesamiento en segundos :  "))
                time_stop = float(input("\nIngresar fin de intervalo de procesamiento en segundos :  "))
                break
            else:
                print("No presiono alguna de las opciones")
                print("\nIngrese el numero de la opcion deseada : \n1: Utilizar todo el video \n2: Ingresar intervalo")

                pass
        except:
            break

    print("\nEl video tiene una frecuencia de muestreo maxima de {:.0f} cuadros/segundo.".format(fps))
    v_max_estimada = float(input("Velocidad esperada : "))  #m/s
    ang_max = 45
    Recommend_fps = np.ceil(v_max_estimada/(rectification_parameters["Dimension_scale"]*np.tan(np.radians(ang_max))))
    if Recommend_fps>fps:
        print(" Se recomienda utilizar la frecuencia maxima de muestreo")
        Recommend_fps = fps
        #PONER EN EL MANUAL QUE SI SE UTILIZA UN dx MAYOR, LA FRECUENCIA DE MUESTREO PUEDE SER MENOR
    else:
        print("Se recomienda utilizar una frecuencia de muestreo de {:.0f} fps o mayor.".format(Recommend_fps))
        print("Recordar que la frecuencia de muestreo a elegir debe ser menor a la maxima.")
    print("\nIngrese el numero de la opcion deseada : \n1: Utilizar frecuencia recomendada \n2: Utilizar frecuencia maxima \n3: Ingresar frecuencia")
    
    while True:
        option = (input("Opcion : "))
        try:
            if option == '1':
                frame_rate = Recommend_fps
                break
            elif option == '2':
                frame_rate = fps
                break
            elif option == '3':
                frame_rate = int(input("Ingresar frecuencia de muestreo a utilizar : "))
                if frame_rate > fps:
                    print("El frame rate escogido es muy alto, elija uno menor al fps maximo")
                    print("\nIngrese el numero de la opcion deseada : \n1: Utilizar frecuencia maxima\n2: Ingresar frecuencia")
                    pass
                else:
                    break
            else:
                print("No presiono alguna de las opciones")
                pass
        except:
            break
                
        
    duration = ( time_stop - time_start ) * frame_rate

    
    
    number_lines = int(input("\nIngresar el numero de timestacks a utilizar : "))
    

                    
    success,frame = vidcap.read()
        
    frame0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            
    frame0_rect = cv2.warpPerspective(frame0,rectification_parameters["Rect_Matrix"],rectification_parameters["Size"])      
    print('\nSeleccionar inicio y fin de transecta/s deseada/s. Primer punto "aguas arriba"')
    
    fig1, axes1 = plt.subplots()
    axes1.set_title('Transectas seleccionadas')

    axes1.imshow(frame0_rect)
        
    x = {}
    y = {}
    timestacks = {"X" : np.array([]), "Y" : np.array([])}
    timestacks["time"] = (time_start,time_stop)
                
    for t in range(number_lines):
        vertex = np.round(plt.ginput(2),0)
        y0, x0 = vertex[0,1], vertex[0,0]
        y1, x1 = vertex[1,1],vertex[1,0]
        length = int(np.hypot(x1-x0, y1-y0))
        axes1.plot([x0, x1], [y0, y1], 'ro-')
        plt.pause(0.05)
        x['x' + str(t)] = np.linspace(x0, x1, length)
        y['y' + str(t)] = np.linspace(y0, y1, length)
        timestacks["timestack" + str(t)] = np.zeros( (length , int(duration)) )
        timestacks["X"] = np.vstack([timestacks["X"],np.array([x0,x1])]) if timestacks["X"].size else np.array([x0,x1])
        timestacks["Y"] = np.vstack([timestacks["Y"],np.array([y0,y1])]) if timestacks["Y"].size else np.array([y0,y1])
           
    axes1.set_title('Transectas seleccionadas')
    fig1.savefig("timestacks_selected.png")        
#    plt.close()
        
        
    success = True        
        
    k = 0
        
    for t in tqdm_notebook(np.arange(time_start , time_stop , 1/frame_rate)):
            
#        print('Proceso completo en un ' + str(np.round((t-time_start)/(time_stop-time_start)*1000)/10) + ' %')
            
        vidcap.set(cv2.CAP_PROP_POS_MSEC , t * 1000)
        success,frame = vidcap.read()
        frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
        image_i = cv2.warpPerspective(frame , rectification_parameters["Rect_Matrix"] , rectification_parameters["Size"])
        for n in range(number_lines):
            timestacks['timestack' + str(n)][:,k] = image_i[y['y'+str(n)].astype(np.int) , 
                           x['x'+str(n)].astype(np.int)]
            
        k+=1
                
        if cv2.waitKey(10) == 27:                     # Salgo del script si presion 'esc'
            break
      
        
    stop = time.process_time()    
    time_elapsed = np.round((stop-start)/.001)*.001
        
        
        # LE SACO LA MEDIA POR FILAS 
    for n in range(number_lines):
        timestacks['timestack' + str(n)] -=  np.mean(timestacks['timestack' + str(n)],axis=1)[:,None]

            
        
    print('Tiempo transcurrido : ' + str(np.round(time_elapsed*100)/100) + ' segundos')
        
    os.chdir(str(oldpath))
        
    rectification_parameters["Temporal_scale"] = 1/frame_rate
    rectification_parameters["Headers"] += "\nTemporal scale : [seconds]" 
        



    with open('Rectification_parameters.dat', 'wb') as outfile:
        pickle.dump(rectification_parameters, outfile, protocol = pickle.HIGHEST_PROTOCOL)
        
    with open('timestacks.dat', 'wb') as outfile:
        pickle.dump(timestacks, outfile, protocol = pickle.HIGHEST_PROTOCOL)
    
    return timestacks,rectification_parameters