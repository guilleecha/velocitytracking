#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 11:45:19 2018

@author: guille
"""

#Video Stabilization by Adam Spannbauer
#https://github.com/AdamSpannbauer/python_video_stab


#MIT License
#
#Copyright (c) 2017 Adam Spannbauer
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


#kp_method – String of the type of keypoint detector to use. Available options are: 
kp_methods = ["GFTT", "BRISK", "DENSE", "FAST", "HARRIS", "MSER", "ORB", "STAR","SIFT", "SURF"]


def stabilization(video_name):

#%% MASKING VIDEO

    import numpy as np
    import cv2
    from PIL import Image, ImageDraw
    from vidstab import VidStab
    import matplotlib.pyplot as plt
    plt.ioff()

    print(''' Elegir Metodo de Deteccion de Puntos Clave :
 Ingrese el metodo deseado : 
1  :  Por defecto("GFTT")
2  : "BRISK"
3  : "DENSE"
4  : "FAST"
5  : "HARRIS"
6  : "MSER"
7  : "ORB"
8  : "STAR"
9  : "SURF"
10 : "SIFT"''')
    kp_method = kp_methods[int(input("Elegir metodo deseado : ")) -1 ]   
    
    
    while True:
        print('''\nMENU DE ESTABILIZACION DE VIDEO
Ingrese el numero de la opcion deseada :
1 : Estabilizar video 
2 : Estabilizar video aplicando mascara
3 : Salir ''')
        option = (input("Opcion : "))
        
        if option == '1' :
            
            stabilized_video = 'stable_' + video_name.split('.')[0] + '.avi'
            
            stabilizer = VidStab(kp_method = kp_method)
            stabilizer.stabilize(input_path= video_name, output_path = stabilized_video,show_progress = False )
            stabilizer.plot_trajectory()
            fig1 = plt.gcf()
            fig1.savefig("trajectories.png")
        
            
            stabilizer.plot_transforms()
            fig2 = plt.gcf()
            fig2.savefig("transforms.png")
            break
        
        elif option == '2':


            vidcap1 = cv2.VideoCapture(video_name)
            success,frame = vidcap1.read()
            img = Image.fromarray(frame)
            fig,ax1 = plt.subplots()
            ax1.imshow(img)
            mask = np.round(plt.ginput(n = 0, timeout = 0, show_clicks = True),0).astype(np.int64).ravel().tolist() # el orden tiene que ser [top left,top right,bottom left, bottom right]
            
            masked = ImageDraw.Draw(img).polygon(mask, outline=1, fill=1)
            masked = np.array(img)
            
            fig,ax1 = plt.subplots()
            ax1.imshow(masked)
            plt.pause(1)
        
        #%% CREATE MASK
        
        
        #%% ADD_MASK_TO VIDEO
        
            vidcap = cv2.VideoCapture(video_name)
            fps = vidcap.get(cv2.CAP_PROP_FPS) 
            size = (int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            
            writer = cv2.VideoWriter("masked.mkv", cv2.VideoWriter_fourcc(*'FMP4') , fps, size)
            length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
            for i in range(length):
                success,frame = vidcap.read()
                print("Progress : " + str(np.around((i/length)*100,decimals = 2)) + "%")
                if success == True:
                    frame = Image.fromarray(frame)
                    ImageDraw.Draw(frame).polygon(mask, outline=1, fill=1)
                    masked = np.array(frame)
                    writer.write(masked)
                    
            vidcap.release()
            writer.release()
        
        #%%
        
        
        
            video2stibilize = video_name
            video_masked = "masked.MKV"
            stabilized_video = 'stable_' + video_name.split('.')[0] + '.avi'
            
            stabilizer = VidStab(kp_method = kp_method)
            stabilizer.gen_transforms(video_masked,show_progress = False) # OBTENGO TRANSFORMACIONES A VIDEO CON MASCARA
            stabilizer.apply_transforms(video2stibilize, stabilized_video, border_size = 'auto',show_progress = False)
            
            #stabilizer = VidStab()
            #stabilizer.stabilize(input_path='LSPIV mmt xsec1.AVI', output_path='stable_video.avi', border_size = 'auto')
            
            stabilizer.plot_trajectory()
            fig1 = plt.gcf()
            fig1.savefig("trajectories.png")
        
            
            stabilizer.plot_transforms()
            fig2 = plt.gcf()
            fig2.savefig("transforms.png")
            
            break
        
        elif option == '3':
            print("Proceso terminado por el usario")
            break
        
        else:
            print("No eligio ninguna de las opciones")
            pass

    
    return stabilized_video


