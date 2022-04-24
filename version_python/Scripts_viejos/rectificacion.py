
def rectification(I,pts_in,dx):
    
    # pts_in : Puntos de entrada en [m] - Arreglo 4x2 [top left,top right,bottom left, bottom right]
    # I : Imagen de referencia para marcar los puntos para la Homografia.
    #dx : Valor en m que queremos que tenga el px
    
    from matplotlib import pyplot as plt
    import numpy as np
    import cv2
    
    plt.rcParams['image.cmap'] = 'gray'
    
    
    
    pts_out = pts_in[:,::-1] * dx**-1 # 100 corresponde a que 1 px = 1/dx m
    pts_out=pts_out.astype(np.float32)
    

    
    fig,ax = plt.subplots(1)
    ax.imshow(I)
    region = np.round(plt.ginput(4),0) # el orden tiene que ser [top left,top right,bottom left, bottom right]
    region = region.astype(np.float32)
    
        
    
    H,_ = cv2.findHomography(region,pts_out)
    
    
    
        
    h1,w1 = I.shape[:2]
    


    
    vertexs = np.float32([[0,0],[0,h1-1],[w1-1,h1-1],[w1-1,0]]).reshape(-1,1,2)
    pts2 = cv2.perspectiveTransform(vertexs , H)
    tx, ty, new_width, new_height = cv2.boundingRect(pts2)
    
    pts = cv2.perspectiveTransform(region.reshape(-1,1,2), H)

#    [xmin, ymin] = np.int32(pts.min(axis=0).ravel() - 0.5)
#    [xmax, ymax] = np.int32(pts.max(axis=0).ravel() + 0.5)
#    [xmin, ymin] = pts2.min(axis=0).ravel() - 0.5
#    [xmax, ymax] = pts2.max(axis=0).ravel() + 0.5
    t = [-tx,-ty]
    Ht = np.array([[1,0,t[0]],[0,1,t[1]],[0,0,1]]) # translate      
    H2 = Ht.dot(H)
#    img_transformada = cv2.warpPerspective(I,H2,(xmax-xmin,ymax-ymin))
    img_transformada = cv2.warpPerspective(I,H2,(new_width,new_height) )
#    img_transformada = cv2.warpPerspective(I,H2,(5000,5000),cv2.BORDER_CONSTANT)
#    X,Y = [xmax,xmin],[ymax,ymin]
      
    plt.imshow(img_transformada)
    
    
    np.save('WarpMatrix',H)


    

    
    return H,img_transformada,X,Y

prueba = np.array([ [5, 5],[, h1],[w1, h1],[w1, 0] ])
corners2 = cv2.perspectiveTransform(np.float32([corners2]), H2)[0]    
bx2, by2, bwidth2, bheight2 = cv2.boundingRect(corners2)

print (bx, by, bwidth, bheight)
print (bx2, by2, bwidth2, bheight2)
