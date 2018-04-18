#!/usr/bin/env python

'''
These functions were developped to compute relevant medical descriptors on the MIMIC dataset (OMOP format).

'''

__authors__ = ['François-Guillaume Fernandez', 'Paul Roujanski', 'Dimitri C', 'Jeremy Desir', 'Julien Gaillet', 'Mateo L']
__license__ = 'MIT License'
__version__ = '0.1'
__maintainer__ = 'François-Guillaume Fernandez'
__status__ = 'Development'


import pandas as pd
import numpy as np


def compute_igs2_score():
    """
    Compute the IGS-II score

    Args:
        arg1 (type): description

    Returns:
        ret1 (type): description
    """

    return 0

def compute_sofa_score(paO2, platelets, bilirubin, map, dopamine, epinephrine, norepinephrine, glasgow_coma_score, creatinine):
    """
    Compute the SOFA score

    Args:
        paO2 (int): 
        platelets (int):
        bilirubin (int):
        map (int): 
        dopmine (int):
        epinephrine (int):
        norepinephrine (int):
        glasgow-coma_score (int):
        creatinine (int):

    Returns:
        sofa_score (int): SOFA score 
    """

    sofa_score = 0 
    if(paO2<100):
        sofa_score+=4 
    elif(paO2<200):
        sofa_score+=3
    elif(paO2<300):
        sofa_score+=2
    else:
        sofa_score+=1

    if(platelets<20):
        sofa_score+=4 
    elif(platelets<50):
        sofa_score+=3
    elif(platelets<100):
        sofa_score+=2
    else:
        sofa_score+=1  
        
    if(bilirubin<2):
        sofa_score+=1 
    elif(bilirubin<6):
        sofa_score+=2
    elif(bilirubin<12):
        sofa_score+=3
    else:
        sofa_score+=4
        
           
    if(dopamine>15 or epinephrine > 0.1 or norepinephrine > 0.1):
        sofa_score+=4 
    elif(dopamine>5 or epinephrine <= 0.1 or norepinephrine <= 0.1):
        sofa_score+=3
    elif(dopamine<=5):
        sofa_score+=2
    elif(map<70):
        sofa_score+=1
        
    if(glasgow_coma_score<6):
        sofa_score+=4 
    elif(glasgow_coma_score<9):
        sofa_score+=3
    elif(glasgow_coma_score<12):
        sofa_score+=2
    else:
        sofa_score+=1
        
    if(creatinine>5):
        sofa_score+=4 
    elif(creatinine>3.5):
        sofa_score+=3
    elif(creatinine>2):
        sofa_score+=2
    else:
        sofa_score+=1

    return sofa_score

