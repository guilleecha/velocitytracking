def process_timestack(timestacks,rectification_parameters):
    
    
    overlaping = int(input("Escriba el overlaping en porcentaje que habra entre los timestacks : "))
    print("Ingrese el numero de la opcion deseada : \n1: Analizar timestack en intervalos fijados por el usuario\n2: Analizar timestack en intervalos fijados por el programa\n3: Salir")
    while True:
        option = (input("Opcion : "))
        try:
            if option == '1':
                from timestack_process_fixedtime import timestack_process_fixedtime
                processed_timestacks = timestack_process_fixedtime(timestacks,overlaping,rectification_parameters)
                break
            elif option == '2':
                from timestack_process import timestack_process
                processed_timestacks = timestack_process(timestacks,overlaping,rectification_parameters)
                break
            elif option == '3':
                print("Proceso terminado por el usuario")
                break
            else:
                print("No presiono alguna de las opciones")
                print("Ingrese el numero de la opcion deseada : \n1: Analizar timestack en intervalos fijados por el usuario\n2: Analizar timestack en intervalos fijados por el programa\n3: Salir")
                pass
        except:
            break

    
    return processed_timestacks
