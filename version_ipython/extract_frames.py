def extract_frames(path,video_name,ext):
    
 #%% COMENTARIOS
 # path: Directorio donde se encuentra el video
 # video_name: Nombre del video sin la extensio
 # ext : formato del video. (MP4,AVI,MOV)
 
#FALTA AGREGAR INICIO Y FIN DE EXTRACCION DE FRAMES
#INTERVALO DE FRAMES QUE SACO
#HACER CASE EN CASO DE QUE QUERAMOS GUARDAR LA IMAGEN EN 8-bits
 
#Guillermo Echavarria  15/05/2018
 
 
#%%
    import cv2
    import os
    import time
    
    time_start=time.process_time()
    
    oldpath = os.getcwd()
    
    os.chdir(path)
    new_directory= './'+ video_name
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
    vidcap = cv2.VideoCapture( path + '/' +video_name + '.'+ ext)
    success,image = vidcap.read()
    count = 0
    success = True
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_extraidos=0
    #while success:
    for i in range(length):
        
        if success:
            cv2.imwrite(os.path.join(new_directory, "frame%d.jpg" % count), image)     # save frame as JPEG file
            frames_extraidos+=1

        success,image = vidcap.read()
        count += 1       
  
    time_stop = time.process_time()    
    time_elapsed= time_stop-time_start
    
    file = open(new_directory+'/'+"extract_frames.txt","w")
    file.write("Extracción finalizada con éxito\n")
    file.write("Se extrajeron " + str(frames_extraidos) +"frames de un total de " + str(length) + "framesn\n" ) 
    file.write("Elapsed time: %f [min]\n" % (time_elapsed/60))
    file.write("Script creado por: Guillermo Echavarria\n")
    file.write("E-mail: gechavarria@fing.edu.uy\n")
    
    file.close()
    
    os.chdir(oldpath)
    
             
    return
                 
        