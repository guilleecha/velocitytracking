#%% 3 - CALIBRACION DE CAMARAS
    
    
#%%

import numpy as np
import cv2
import glob

nx=9 #Numero de esquinas internas en la horizontal
ny=6 #Numero de esquinas internas en la vertical

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

#Modelo del damero en 3D
esquinasDamero3D = np.zeros((ny*nx,3), np.float32)
esquinasDamero3D[:,:2] = np.mgrid[0:nx,0:ny].T.reshape(-1,2)

## Listas que contienen los puntos que se utilizan para calibrar
puntosCalib3D = [] # puntos 3d a utilizar en la calibración
puntosCalib2D = [] # puntos 2d a utilizar en la calibración

images = glob.glob('*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (nx,ny),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        puntosCalib3D.append(esquinasDamero3D)

        cornersSubPixel = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        puntosCalib2D.append(cornersSubPixel)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (nx,ny), cornersSubPixel,ret)
        cv2.imshow('img',img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

#CALIBRACION

ret, calibrationMatrix, distortionCoeff, rvecs, tvecs = cv2.calibrateCamera(puntosCalib3D, puntosCalib2D, gray.shape[::-1],None,None)
print('Calibracion Terminada')
np.save('calibrationMatrix',calibrationMatrix )
np.save('distortionCoeff',distortionCoeff )
print('Matrices de calibración guardadas')


## UNDISTORETED
matrizIntrinsecos = np.load('calibrationMatrix.npy')
coeficientesDistorsion = np.load('distortionCoeff.npy')
frame = cv2.imread(images[0])
imagenCorregida = cv2.undistort(frame, calibrationMatrix, distortionCoeff)
cv2.imwrite('Corrediga.jpg',imagenCorregida)

#Re-projection Error

mean_error = 0
for i in range(len(puntosCalib3D)):
    imgpoints2, _ = cv2.projectPoints(puntosCalib3D[i], rvecs[i], tvecs[i], calibrationMatrix, distortionCoeff)
    error = cv2.norm(puntosCalib2D[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error

mean_error = np.round(mean_error*100)/100
total_error =np.round( mean_error/len(puntosCalib3D)*1000)/1000
print( "total error: " + str(total_error))


file = open('./'+"calibracion.txt","w")
file.write("Calibración finalizada con éxito\n")
file.write("Imágenes utilizadas: " + str(len(images)) + "\n")
file.write("Mean error reprojection : " + str(mean_error) + " px" "\n" ) 
file.write("Total error reprojection : " + str(total_error) + " px" "\n\n" ) 
file.write("Calibration Matrix \n"  )
file.write(str(calibrationMatrix) + "\n"+ "\n"  )
file.write("Distortion Coefficient \n" )
file.write(str(distortionCoeff) + "\n"+ "\n"  )
file.write("Calibration made in Python\n")
file.write("By Guillermo Echavarria\n")
file.write("IMFIA - FIng\n")
file.write("E-mail: gechavarria@fing.edu.uy\n")
file.close()