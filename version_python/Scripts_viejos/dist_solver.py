
def distance_solver(PuntosGPS):
    
    #PuntosGPS = bool (True,False)

    from scipy.optimize import least_squares
    import numpy as np
    import csv
    from str2bool import str2bool
     
    
    
    if PuntosGPS == True :
        print(" \nIngresar de la forma CorrdX,CoordY ")
        
        Txt = str2bool(input('''\nSi tiene los puntos en un .txt, contestar True, en caso
                             de ingresar los puntos manualmente contestar False'''))
        if Txt:
            results = np.array()
            with open('pts.txt', newline='') as inputfile:
                for row in csv.reader(inputfile):
                    results.append(row)
        else:
        CordX1,CordY1 = input('\nCoordenadas Punto 1 : ').split(',')
        CordX2,CordY2 = input('Coordenadas Punto 2 : ').split(',')
        CordX3,CordY3 = input('Coordenadas Punto 3 : ').split(',')
        CordX4,CordY4 = input('Coordenadas Punto 4 : ').split(',')
    
        P1 = np.array([float(CordX1),float(CordY1)])
        P2 = np.array([float(CordX2),float(CordY2)])
        P3 = np.array([float(CordX3),float(CordY3)])
        P4 = np.array([float(CordX4),float(CordY4)])
        
        del(CordX1,CordY1,CordX2,CordY2,CordX3,CordY3,CordX4,CordY4)
    
        l12 = np.linalg.norm(P1-P2)
        l13 = np.linalg.norm(P1-P3)
        l14 = np.linalg.norm(P1-P4)
        l23 = np.linalg.norm(P2-P3)
        l34 = np.linalg.norm(P3-P4)
        l24 = np.linalg.norm(P2-P4)
        
    else:
        print('Usar distancias en metros')
        l12 = float(input('Distancia Punto 1 a Punto 2 : '))
        l13 = float(input('Distancia Punto 1 a Punto 3 : '))
        l14 = float(input('Distancia Punto 1 a Punto 4 : '))
        l23 = float(input('Distancia Punto 2 a Punto 3 : '))
        l34 = float(input('Distancia Punto 3 a Punto 4 : '))
        l24 = float(input('Distancia Punto 2 a Punto 4 : '))
            
    #    
    #l12 = 2
    #l13 = 2 * np.sqrt(2)
    #l14 = 2
    #l23 = 2
    #l34 = 2
    #l24 = 2 * np.sqrt(2)   
    
    data = (l12,l13,l14,l23,l34,l24)
    
    def equations(variables , *data):
        l12,l13,l14,l23,l34,l24 = data
        x3 = variables[0]
        y3 = variables[1]
        x4 = variables[2]
        y4 = variables[3]
        
        b= np.asarray([l13**2,l14**2,l23**2,l34**2,l24**2])
        
        F=np.empty((5))
        
        F[0]  = (x3**2) + (y3**2) - b[0]
        F[1] = (x4**2) + (y4**2) - b[1]
        F[2]  = (x3-l12)**2 + (y3**2) - b[2]
        F[3] = (x3-x4)**2 + (y3-y4)**2 - b[3]
        F[4]  = (l12-x4)**2 + (y4**2) - b[4]
            
        return F
    
    wo = (1,1,1,1)
    solve  =  least_squares( equations , wo ,bounds = (0,np.inf) ,args=data )
    x = solve.x
    
    
    X1 = 0
    Y1 = 0
    X2 = l12
    Y2 = 0
    X3 = x[0]
    Y3 = x[1]
    X4 = x[2]
    Y4 = x[3]
    
    X = np.asarray([X1,X2,X3,X4])
    Y = np.asarray([Y1,Y2,Y3,Y4])
    Points = np.transpose(np.asarray([X,Y]))

    return Points 