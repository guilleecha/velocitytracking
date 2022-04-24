#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 12:11:40 2018

@author: guille
"""

def print_figures(timestacks,rectification_parameters,data_filtered,processed_timestacks,results):
    from plt_results_log import plot_timestack_results
    from plt_individual_log import plot_timestack_individual
    
    
    print("Menu de figuras")
    print("Ingrese el numero de la opcion deseada :\n1 : Print de resultados individuales\n2 : Print de resultados por timestack\n3 : Ambos\n4 : Salir")
    option = input("Ingrese la opcion deseada : ")
    while True:
        try:        
            if option == '1':
                plot_timestack_individual(timestacks,rectification_parameters,data_filtered,processed_timestacks)
                break
                
            elif option == '2':
                plot_timestack_results(timestacks,rectification_parameters,data_filtered,results)
                break
        
            elif option == '3':
                plot_timestack_individual(timestacks,rectification_parameters,data_filtered,processed_timestacks)
                plot_timestack_results(timestacks,rectification_parameters,data_filtered,results)
                break
            
            elif option == '4':
                print("Ha salido del menu de ploteo")
                break
            else:
                print("No escribio ninguna de las opciones")
                pass
        except:
            break
        
    
    
    
    return