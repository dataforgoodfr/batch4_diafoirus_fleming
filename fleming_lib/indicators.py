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


def compute_igs2_score(age,heart_rate,systolic_bp,temp,glasgow_coma_score,PaO2DivFIO2):
    """
    
    NOT FINISHED YET!
    
    Compute the IGS-II score

    Args:
        Use the worst value for each physiological variable 
        within the past 24 hours.
        
        age (int): Years
        heart_rate (int): BPM
        systolic_bp (int): mmHg
        temp (int): °C
        glasgow_coma_score (int): 
        PaO2DivFIO2 (int) : mmHg

    Returns:
        ret1 (type): description
    """
    
    igs2_score = 0 
    # Age (Years)
    if (age<40): 
        igs2_score+=0
    elif (age<=59) :
        igs2_score+=7
    elif (age<=69) :
        igs2_score+=12
    elif (age<=74) :
        igs2_score+=15
    elif (age<=79) :
        igs2_score+=16
    else:
        igs2_score+=18
        
    # Vitals   
    # Heart Rate
    if (heart_rate<40):  # heart_rate = 0 if cardiac arrest within past 24h
        igs2_score+=11
    elif (heart_rate<=69) :
        igs2_score+=2
    elif (heart_rate<=119) :
        igs2_score+=0
    elif (heart_rate<=159) :
        igs2_score+=4
    else :
        igs2_score+=7
    
    # Systolic BP
    if (systolic_bp<70):  # heart_rate = 0 if cardiac arrest within past 24h
        igs2_score+=13
    elif (systolic_bp<=99) :
        igs2_score+=5
    elif (systolic_bp<=199) :
        igs2_score+=0
    else :
        igs2_score+=2
        
    # Temperature
    if (temp<39):
        igs2_score+=0
    else:
        igs2_score+=3
        
    # Glasgow coma score
    if (glasgow_coma_score<6):
        igs2_score+=26
    elif(glasgow_coma_score<=8) :
        igs2_score+=13   
    elif(glasgow_coma_score<=10) :
        igs2_score+=7
    elif(glasgow_coma_score<=13) :
        igs2_score+=5
    elif(glasgow_coma_score<=15) :
        igs2_score+=0
    else:
        raise ValueError('Glasgow coma score should be lower than 15.')
     
    # Oxygenation   
    # PaO2/FIO2(mmHg)
    if (PaO2DivFIO2<100):  
        igs2_score+=11
    elif (PaO2DivFIO2<=199) :
        igs2_score+=9
    else :
        igs2_score+=6

    
    

    return igs2_score

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

