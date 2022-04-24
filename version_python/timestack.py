def timestack(video,rectification_parameters):
    from time_stack_lines import time_stack_lines
    from time_stack import time_stack


    print("\nDefinicion de timestacks")
    print("\nIngrese el numero de la opcion deseada : \n1: Trabajar con timestacks en una seccion \n2: Trabajar con timestacks definidos por el usuario\n3: Salir")

    while True:
        option = (input("Opcion : "))
        try:
            if option == '1':
                timestacks,rectification_parameters = time_stack_lines(video,rectification_parameters)
                break
            elif option == '2':
                timestacks,rectification_parameters = time_stack(video,rectification_parameters)
                break
            elif option == '3':
                print("Proceso terminado por el usuario")
                break
            else:
                print("No presiono alguna de las opciones")
                print("\nIngrese el numero de la opcion deseada : \n1: Trabajar con timestacks en una seccion \n2: Trabajar con timestacks definidos por el usuario\n3: Salir")
                pass
        except:
            break

    return timestacks,rectification_parameters