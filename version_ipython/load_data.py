#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 17:50:51 2018

@author: guille
"""
def load_data(name_file):
    import pickle
    try:
        with open(name_file +'.dat', "rb") as file:
            variable = pickle.load(file)
            file.close()
        print("Archivo cargado correctamente")
    except:
        print("Hay un error en el archivo de timestacks")
        
    return variable
