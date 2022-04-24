
def rectification(video):
    
    # pts_in : Puntos de entrada en [m] - Arreglo 4x2 [top left,top right,bottom left, bottom right]
    # I : Imagen de referencia para marcar los puntos para la Homografia.
    #dx : Valor en m que queremos que tenga el px
    #n_points: por defecto 4. En caso de tener mas de 4 puntos para realizar la rectificacion
    #       
    
    from matplotlib import pyplot as plt
    import numpy as np
    import cv2
    from dist_solver import distance_solver
    import csv
    import itertools
    from matplotlib.patches import Polygon
    
    #%% CARGA DE LA IMAGEN PARA REALIZAR RECTIFICACION
    print("Imagen para recitificacion del video")
    print("Ingrese el numero de la opcion deseada : \n1: Utilizar primer frame del video\n2: Utilizar imagen cargada por el usuario")
    while True:
        option = (input("Opcion : "))
        try:
            if option == '1':
                vidcap = cv2.VideoCapture(video)
                success,frame = vidcap.read()
                frame0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                I = frame0.copy()
                
                break
            elif option == '2':
                filename = input("Ingresar nombre de la imagen a utilizar (con extension de archivo) : ")
                I  = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
                print("Desea corregir la distorsion de la camara en la imagen : \n1: Si\n2: No ")
                correction_option = input("Opcion : ")
                if correction_option == '1':
                    print("Ingresar los nombres de los archivos la Coefficient Matrix y Disstortion Coeficiente Matrix.\nRecordar que tienen que estar en formato .npy")
                    Coeeficient_Matrix_name = input("Ingresar nombre del archivo de Coefficient Matrix : ")
                    Dist_Matrix_name = input("Ingresar nombre del archivo de Distortion Coefficient Matrix : ")
                    CM = np.load(Coeeficient_Matrix_name + '.npy')
                    DC = np.load(Dist_Matrix_name + '.npy')                    
                    I =  cv2.undistort(I, CM, DC)
                break
            else:
                print("No presiono alguna de las opciones")
                print("Ingrese el numero de la opcion deseada : \n1: Ingresar los puntos manualmente\n2: Usar archivo de texto con informacion de puntos")
                pass
        except:
            break    
    #%%

    
    n_points = int(input("Ingresar con cuantos puntos de control desea hacer la rectificacion : "))
    print("Ha escogido hacer la rectificacion con " + str(n_points) + " puntos" )
    
    if n_points == 4:
        print("Ingrese el numero de la opcion deseada : \n1: Utilizar puntos tomados con GPS\n2: Utilizar distancias relativas entre puntos")
        while True:
            option = (input("Opcion : "))
            try:
                if option == '1':
                    PuntosGPS = True
                    break
                elif option == '2':
                    PuntosGPS = False
                    break
                else:
                    print("No presiono alguna de las opciones")
                    print("Ingrese el numero de la opcion deseada : \n1: Elegir cantidad de timestacks\n2: Elegir distancia entre timestacks")
                    pass
            except:
                break
        pts_in = distance_solver(PuntosGPS)
                
    elif n_points > 4:
        print("Si eligio esta opcion los puntos deben ser tomados por GPS, o ya estar referenciados a un sistema cartesiano")
        print("Ingrese el numero de la opcion deseada : \n1: Ingresar los puntos manualmente\n2: Usar archivo de texto con informacion de puntos")
        while True:
            option = (input("Opcion : "))
            try:
                if option == '1':
                    Txt = False
                    break
                elif option == '2':
                    Txt = True
                    break
                else:
                    print("No presiono alguna de las opciones")
                    print("Ingrese el numero de la opcion deseada : \n1: Ingresar los puntos manualmente\n2: Usar archivo de texto con informacion de puntos")
                    pass
            except:
                break
        if Txt:
            pts_in = []
            print("Recordar que el formato del archivo puntos debe ser .txt ")
            name = input("\nIngrese nombre del archivo de puntos sin la extension: ")
            with open(name + '.txt', newline='') as inputfile:
                for row in csv.reader(inputfile):
                    pts_in.append(row)
                pts_in = np.array(pts_in).astype(np.float)                
        else:    
            print("\nIngresar coordenadas GPS de la forma CorrdX,CoordY")
            pts_in = []
            point_count = 1
            for j in range(int(n_points)):
                pts_in.append(input('\nCoordenadas Punto' +str(point_count) + ' : ').split(','))
                point_count += 1
            pts_in = np.array(pts_in).astype(np.float)    
            pts_in -=  np.min(pts_in,axis=0)[:,None]
    else:
        print("El numero de puntos debe ser mayor o igual a 4")
 
    print("\nSeleccionar puntos en el mismo orden que se ingresaron las coordenadas")
    fig,ax1 = plt.subplots()
    ax1.imshow(I)
    region = np.round(plt.ginput(n_points),0) # el orden tiene que ser [top left,top right,bottom left, bottom right]
    region = region.astype(np.float32)
    
    plt.close(fig)
    
    

    #%% dx recomendado
    # Redimensiono de manera que la distancia mas grande en pixeles, no cambie su tamano
    
    print("La relacion px/m corresponde al valor en metros que se le dara a cada pixel") 
    distances_px = []
    
    for po,p1 in itertools.combinations(region,2):
        distances_px.append([np.linalg.norm(po-p1),po,p1])
        
    max_distance_px = np.nanmax([x[0] for x in distances_px])
    
    indice = int(np.where([x[0] for x in distances_px] == max_distance_px)[0])
    
    
    distances_m = [] 
    for po,p1 in itertools.combinations(pts_in,2):
        distances_m.append([np.linalg.norm(po-p1),po,p1])     
    
    distance_m = distances_m[indice][0]
    
    vidcap = cv2.VideoCapture(video)
#    fps = np.floor(vidcap.get(cv2.CAP_PROP_FPS))
    
#    v_max_estimada = float(input("Velocidad maxima esperada : "))  #m/s
#    ang_max = 75
#    min_dx = (v_max_estimada*(1/fps)) / np.tan((ang_max*np.pi)/180)
    
    Recommend_dx = distance_m/max_distance_px #if distance_m/max_distance_px > min_dx else min_dx
    
       

    print("\nSe sugiere una relacion px/m de {:.3f} " .format(Recommend_dx)) # para una velocidad de muestreo de {1:.0f} fps " .format(Recommend_dx,fps))
    print("Ingrese el numero de la opcion deseada : \n1: Utilizar relacion px/m sugerida\n2: Utilizar relacion px/m escogida por el usuario")
    while True:
        option = (input("Opcion : "))
        try:
            if option == '1':
                dx = Recommend_dx
                break
            elif option == '2':
                dx = float(input("\nIngrese relacion px/m en [m] : "))
                break
            else:
                print("No presiono alguna de las opciones")
                print("Ingrese el numero de la opcion deseada : \n1: Utilizar relacion px/m optima\n2: Utilizar relacion px/m escogida por el usuario")
                pass
        except:
            break
        
    pts_out = pts_in[:,::-1] * dx ** -1 
    pts_out = pts_out.astype(np.float32)
    
    H,_ = cv2.findHomography(region,pts_out)

    print("\nDefinir zona de interes ") # para una velocidad de muestreo de {1:.0f} fps " .format(Recommend_dx,fps))
    print("Ingrese el numero de la opcion deseada : \n1: Utilizar area de rectificacion como zona de interes\n2: Elegir zona de interes")
    while True:
        option = (input("Opcion : "))
        try:
            if option == '1':
                pts = cv2.perspectiveTransform(region.reshape(-1,1,2), H)
                tx, ty, new_width, new_height = cv2.boundingRect(pts)
                t = [-tx,-ty]
                Ht = np.array([[1,0,t[0]],[0,1,t[1]],[0,0,1]]) # translate      
                H = Ht.dot(H)
                break
            elif option == '2':
                fig,ax1 = plt.subplots()
                ax1.imshow(I)
                while True:
                    try:
                        xy = np.round(plt.ginput(n = 1, timeout = 0, show_clicks = True),0).astype(np.float32) # el orden tiene que ser [top left,top right,bottom left, bottom right]                        
                        if not "region_of_interest" in locals():
                            region_of_interest = xy
                        else:
                            region_of_interest = np.append(region_of_interest,xy,axis = 0)

                        color = plt.rcParams['axes.prop_cycle'].by_key()['color'][1]
                        color_markers = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]
                        color_polygon = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]
                        ax1.plot(region_of_interest[:,0],region_of_interest[:,1], marker = 'o' , alpha = 0.6, fillstyle='none', linestyle ='', color = color_markers) 
                        if np.shape(region_of_interest)[0] > 1:
                            ax1.plot(region_of_interest[:,0],region_of_interest[:,1], linestyle ='-', alpha = 0.4, color = color) 
                        plt.pause(0.05)
                            
                    except:
                        break
                    
                pts = cv2.perspectiveTransform(region_of_interest.reshape(-1,1,2), H)
                tx, ty, new_width, new_height = cv2.boundingRect(pts)
                t = [-tx,-ty]
                Ht = np.array([[1,0,t[0]],[0,1,t[1]],[0,0,1]]) # translate      
                H = Ht.dot(H)
                lines = np.append(region_of_interest, region_of_interest[0,:].reshape(1,2), axis = 0)
                ax1.plot(lines[:,0],lines[:,1], linestyle ='-', alpha = 0.4, color = color) 
                ax1.plot(lines[:,0],lines[:,1], marker = 'o' , alpha = 0.6, fillstyle='none', linestyle ='', color = color_markers) 
                p = Polygon(np.array(region_of_interest), closed = True, alpha = 0.2, color = color_polygon)
                plt.gca().add_artist(p)
                plt.pause()
                break
            else:
                print("No presiono alguna de las opciones")
                print("Ingrese el numero de la opcion deseada : \n1: Utilizar area de rectificacion como zona de interes\n2: Elegir zona de interes")
                pass
        except:
            break

 #%%   

    color_CP = plt.rcParams['axes.prop_cycle'].by_key()['color'][3]

    

    img_transformada = cv2.warpPerspective(I,H,(new_width,new_height) )
      
    fig2,ax1 = plt.subplots()
    ax1.clear()
    ax1.imshow(img_transformada)
    xlim,ylim = ax1.get_xlim(),ax1.get_ylim()
    if "region_of_interest" in locals():
        CP_s = cv2.perspectiveTransform(region.reshape(-1,1,2), H)
        CP_s = CP_s.reshape(np.shape(CP_s)[0],np.shape(CP_s)[2])
        
        region_of_interest_transformed = cv2.perspectiveTransform(lines.reshape(-1,1,2), H)
        region_of_interest_transformed = region_of_interest_transformed.reshape(np.shape(region_of_interest_transformed)[0],np.shape(region_of_interest_transformed)[2])
        ax1.plot(region_of_interest_transformed[:,0],region_of_interest_transformed[:,1], linestyle ='-', alpha = 0.4, color = color) 
        ax1.plot(region_of_interest_transformed[:,0],region_of_interest_transformed[:,1], marker = 'o' , alpha = 0.6, fillstyle='none', linestyle ='', color = color_markers) 
        ax1.set_xlim(xlim)
        ax1.set_ylim(ylim)
        p = Polygon(np.array(region_of_interest_transformed), closed = True, alpha = 0.2)
        plt.gca().add_artist(p)
        count_CP = 0
        for CP in CP_s:
            ax1.plot(CP[0],CP[1], marker = 'o' , alpha = 0.6, fillstyle='none', linestyle ='', color = color_CP) 
            ax1.text(CP[0],CP[1],"Control Point {:.0f}".format(count_CP),fontsize = 8, ha = 'left')
            count_CP +=1
        
    fig2.savefig("Imagen_rectificada.png")
    
    
    rectification_parameters = {}
    rectification_parameters["Rect_Matrix"] = H
    rectification_parameters["Headers"] = "Rect_Matrix : Rectification Homography Matrix" 
    rectification_parameters["Rectificated_Image"] = img_transformada
    rectification_parameters["Headers"] += "\nRectificated Image : Rectificated Work Region" 
    rectification_parameters["Size"] = (new_width,new_height)
    rectification_parameters["Headers"] += "\nSize : Size of Rectificated Work Region (width,height)" 
    rectification_parameters["Dimension_scale"] = dx
    rectification_parameters["Headers"] += "\nDimension scale : [meters]" 

    return rectification_parameters

