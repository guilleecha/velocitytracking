def undistor_video(path,video_name,ext,filename_out,cam_matrix,dist_coef):
    import cv2
    import numpy as np

    video = cv2.VideoCapture(path + '/' + video_name  + '.'+ ext)
    fps = video.get(cv2.CAP_PROP_FPS) 
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    writer = cv2.VideoWriter(path + '/' + filename_out  + '.mkv', cv2.VideoWriter_fourcc(*'FMP4') , fps, size)
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for i in range(length):
        success,frame = video.read()
        print('Proceso completo en un ' + str(np.round(i/length*1000)/10) + ' %')
        if success==True:
            frame =  cv2.undistort(frame, cam_matrix, dist_coef)
            writer.write(frame)
    video.release()
    writer.release()


