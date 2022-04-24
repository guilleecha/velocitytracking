def time_stack_lines(video,rectification_parameters):
    
    #Script que marca una seccion y marca lines de timestack cada cierta distancia en metros.
    
    # frame_rate : frame_rate deseado. No puede ser mayor al del video
    # time_start : tiempo de comienzo del time-stack en el video [s]
    # time_stop : tiempo de fin del time-stack en el video [s]
    # rect_par : Resultados de rectificacion
    # distance: Distancia entre lineas [m]
    # offset : largo de las lineas [m]
    
    import numpy as np
    import matplotlib.pyplot as plt
    import cv2 #opencv
    import os
    from pathlib import Path
    import time
    import itertools
    import pickle

#    import keyboard
      
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

#    while True:
#        try:
#            if keyboard.is_pressed('1'):
#                frame_rate = fps 
#            elif keyboard.is_pressed('2'):
#                frame_rate = float(input("\nIngresar frecuencia de muestreo a utilizar : "))
#            else:
#                pass
#        except:
#            break
   

        #%% Seleccion de transecta
    print('\nSeleccionar inicio y fin de seccion deseada. Primer punto "Margen Izquierda" , segundo punto "Margen Derecha"')    
    success,frame = vidcap.read()
    frame0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            
    frame0_rect = cv2.warpPerspective(frame0,rectification_parameters["Rect_Matrix"],rectification_parameters["Size"])     
    rectification_parameters["Rectificated_Image"] = frame0_rect # se agrego para que el grafico de donde estan los frames sea este y no donde se hace la rectificacion
    fig1, axes1 = plt.subplots()
    axes1.set_title('Transectas seleccionadas')
    axes1.imshow(frame0_rect)
    timestacks = {"X" : np.array([]), "Y" : np.array([])}
    timestacks["time"] = (time_start,time_stop)
    vertex = np.round(plt.ginput(2),0)
    y0, x0 = vertex[0,1], vertex[0,0]
    y1, x1 = vertex[1,1],vertex[1,0]
    length = int(np.hypot(x1-x0, y1-y0))
    axes1.plot([x0, x1], [y0, y1], 'go-')
    plt.pause(0.05)
    length_transect_m = length * rectification_parameters["Dimension_scale"]
    timestacks["section"] = np.array([[x0,y0],[x1,y1]])
    
      
      #%%  
    print("\nSeparacion entre lineas de los timestacks")
    print("La seccion tiene un largo de " + str(np.round(length_transect_m*100)/100) + " metros" )
    print("Ingrese el numero de la opcion deseada : \n1 : Elegir cantidad de timestacks\n2 : Elegir distancia entre timestacks\n3 : Volver a elegir seccion\n4 : Salir ")

    while True:
        option = (input("Opcion : "))
        try:
            if option == '1':
                number_lines = int(input("Ingresar numero de timestacks : "))
                number_space = number_lines - 1
                distance = length/number_space
                break
            elif option == '2':
                distance = float(input("Ingresar separacion entre timestacks en [m] : "))
                number_space = int(np.round(length_transect_m / distance))
                number_lines = int(number_space + 1)      
                break
            elif option == '3':
                success,frame = vidcap.read()
                frame0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            
                frame0_rect = cv2.warpPerspective(frame0,rectification_parameters["Rect_Matrix"],rectification_parameters["Size"])      
                fig1, axes1 = plt.subplots()
                axes1.set_title('Transectas seleccionadas')
                axes1.imshow(frame0_rect)
                timestacks = {"X" : np.array([]), "Y" : np.array([])}
                timestacks["time"] = (time_start,time_stop)
                vertex = np.round(plt.ginput(2),0)
                y0, x0 = vertex[0,1], vertex[0,0]
                y1, x1 = vertex[1,1],vertex[1,0]
                length = int(np.hypot(x1-x0, y1-y0))
                axes1.plot([x0, x1], [y0, y1], 'go-')
                plt.pause(0.05)
                length_transect_m = length * rectification_parameters["Dimension_scale"]
                print("Ingrese el numero de la opcion deseada : \n1 : Elegir cantidad de timestacks\n2 : Elegir distancia entre timestacks\n3 : Volver a elegir seccion\n4 : Salir ")
                pass
            elif option == '4':
                print("Ha salido de la seleccion de timestacks")
                break
        
            else:
                print("No presiono alguna de las opciones")
                print("Ingrese el numero de la opcion deseada : \n1: Elegir cantidad de timestacks\n2: Elegir distancia entre timestacks")

                pass
        except:
            break
        
        
    print("Disposicion de las lineas del timestack")
    print("\nIngrese el numero de la opcion deseada : \n1: Linea centrada en la transecta\n2: Linea hacia aguas abajo de la transecta")
    while True:
        option = (input("Opcion : "))
        try:
            if option == '1':
                offset = float(input("Ingresar largo de la linea en [m] : "))
                offset_px = offset * rectification_parameters["Dimension_scale"] ** -1
                Y = np.linspace(offset_px/2, -offset_px/2, 2)
                break
            elif option == '2':
                offset = float(input("Ingresar largo de la linea en [m] : "))
                offset_px = offset * rectification_parameters["Dimension_scale"] ** -1
                Y = np.linspace(offset_px, 0 , 2)
                break
            else:
                print("No presiono alguna de las opciones")
                print("\nIngrese el numero de la opcion deseada : \n1: Linea centrada en la transecta\n2: Linea hacia aguas abajo de la transecta")

                pass
        except:
            break
        
    
    if number_lines == 1:
        X = length/2
    else:
        X = np.linspace(length, 0, number_lines)
        
        
    lines_vertex = list(itertools.product(X,Y))
        
    angle = np.arctan2(y0-y1,x0-x1)
    RotMatrix = np.array([[np.cos(angle),    -np.sin(angle),        0],
                    [np.sin(angle),    np.cos(angle),     0],
                    [0,                     0,            1]])
    
    t = [-x1, -y1 ]
    Trans_Matr = np.array([[1,0,-t[0]],[0,1,-t[1]],[0,0,1]]) # translate
    Matrix = Trans_Matr.dot(RotMatrix)
    Rotated_vertex = []
    for xi,yi in lines_vertex:
        Rotated_vertex.append(np.dot(Matrix,[xi,yi,1])[:-1])
            
    Rotated_vertex = np.asarray(Rotated_vertex)
    timestacks["X"] = np.reshape(Rotated_vertex[:,0],(-1,2)).astype(int)
    timestacks["Y"] = np.reshape(Rotated_vertex[:,1],(-1,2)).astype(int)
        
    x = {}
    y = {}
        
    for t in range(number_lines) :
        length_line = int(np.hypot(np.diff(timestacks["X"][t]),np.diff(timestacks["Y"][t])))
        timestacks["timestack" + str(t)] = np.zeros( (length_line , int(duration)) )
        x['x' + str(t)] = np.linspace(timestacks["X"][t,0],timestacks["X"][t,1], length_line)[::-1]
        y['y' + str(t)] = np.linspace(timestacks["Y"][t,0],timestacks["Y"][t,1], length_line)
        axes1.plot(timestacks["X"][t],timestacks["Y"][t],'ro-')
        plt.pause(0.05)

        
        #%%
        
    axes1.set_title('Transectas seleccionadas')
    fig1.savefig("timestacks_selected.png")        
#    plt.close()
        
        
    success = True        
        
    k = 0
        
    for t in np.arange(time_start , time_stop , 1/frame_rate):
        
        print('Proceso completo en un ' + str(np.round((t-time_start)/(time_stop-time_start)*1000)/10) + ' %')
            
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
        
    os.chdir(oldpath)
        
    rectification_parameters["Temporal_scale"] = 1/frame_rate
    rectification_parameters["Headers"] += "\nTemporal scale : [seconds]" 
                
    with open('Rectification_parameters.dat', 'wb') as outfile:
        pickle.dump(rectification_parameters, outfile, protocol = pickle.HIGHEST_PROTOCOL)
        
    with open('timestacks.dat', 'wb') as outfile:
        pickle.dump(timestacks, outfile, protocol = pickle.HIGHEST_PROTOCOL)


    return timestacks,rectification_parameters