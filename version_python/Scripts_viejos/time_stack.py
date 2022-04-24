def time_stack(path,video_name,ext,H,frame_rate,X,Y,time_start,time_stop,number_lines):
    
    # frame_rate : frame_rate deseado. No puede ser mayor al del video
    # CM : CalibrationMatrix
    # DC : Distorssion Coeeficiente
    # time_start : tiempo de comienzo del time-stack en el video [s]
    # time_stop : tiempo de fin del time-stack en el video [s]
    
    import numpy as np
    import matplotlib.pyplot as plt
    import cv2 #opencv
    import os
    import time
      
    start = time.process_time()
        
    oldpath = os.getcwd()
        
    os.chdir(path)
    vidcap = cv2.VideoCapture('./' +video_name + '.'+ ext)
    fps = np.round(vidcap.get(cv2.CAP_PROP_FPS))

    
    
    if fps > frame_rate:
        
            
        xmax = np.max(X)
        xmin = np.min(X)
        ymax = np.max(Y)
        ymin = np.min(Y)
    

        
        success,frame = vidcap.read()
        
        frame0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            
        frame0_rect = cv2.warpPerspective(frame0,H,(xmax-xmin,ymax-ymin))        
        
        fig1, axes1 = plt.subplots()
        axes1.set_title('Seleccionar inicio y fin de transecta/s deseada/s. Primer punto aguas arriba')    
        axes1.imshow(frame0_rect)
        x=list()
        y=list()
        
        for j in range(number_lines):
            vertex = np.round(plt.ginput(2),0)
            y0, x0 = vertex[0,1], vertex[0,0]
            y1, x1 = vertex[1,1],vertex[1,0]
            length = int(np.hypot(x1-x0, y1-y0))
            axes1.plot([x0, x1], [y0, y1], 'ro-')
            x.append(np.linspace(x0, x1, length))
            y.append(np.linspace(y0, y1, length))
        
        
        plt.close()
        
        
        success = True        
        
        duration = ( time_stop - time_start ) * frame_rate
        
        
        time_stack_aux = np.zeros( (len(frame0_rect[y.astype(np.int), x.astype(np.int)]) , int(duration)) )
        
        k = 0
        
        for t in np.arange(time_start , time_stop , 1/frame_rate):
            
            print('Proceso completo en un ' + str(np.round((t-time_start)/(time_stop-time_start)*1000)/10) + ' %')
            
            vidcap.set(cv2.CAP_PROP_POS_MSEC , t * 1000)
            success,frame = vidcap.read()
            frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
            image_i = cv2.warpPerspective(frame , H , (xmax-xmin , ymax-ymin)) 
            time_stack_aux[:,k] = image_i[y.astype(np.int) , x.astype(np.int)]
            
            k+=1
                
            if cv2.waitKey(10) == 27:                     # Salgo del script si presion 'esc'
                break
      
        
        stop = time.process_time()    
        time_elapsed = stop-start
        
        
        # LE SACO LA MEDIA POR FILAS 
        for j in range(time_stack_aux.shape[0]):
            time_stack_aux[j,:] -=  np.mean(time_stack_aux,axis=1)[j]
    

        
        print('Tiempo transcurrido : ' + str(time_elapsed) + ' segundos')
        
        os.chdir(oldpath)
        
        fig.savefig("timestack_selected" + str(time) +".png",dpi=1000)

     
        
    else:
        print('Tiene que escojer un frame_rate menor al framerate del video ')
        print('fps del video = ' + str(fps))


    return time_stack_aux