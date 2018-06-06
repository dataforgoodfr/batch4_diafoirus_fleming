'''Severity Scores'''

import pandas as pd
import numpy as np


def compute_sapsii_score(row):
    """
    
    Compute the SAPS-II score

    Args:
    
    row (pd.DataFrame) : each column being :
       
        #Use the worst value for each physiological variable within the past 24 hours.
        #Not the case yet !
        
        'age' (int): Years
        'heart_rate' (int): BPM
        'systolic_bp' (int): mmHg
        'temp' (int): °C
        'Glasgow coma scale' (int): ?
        'Oxygen saturation in Arterial blood' or PaO2 (int) : mmHg 
        'Oxygen concentration breathed' or FIO2 : %

    Returns:
        ret1 (type): description
    """
    
    
    
    igs2_score = 0 
    
    # Components
    age = row['age']
    systolic_bp = row ['BP systolic']
    temp = row['bodyTemperature_C']
    glasgow_coma_score = row['Glasgow coma scale']
    #PaO2DivFIO2 = row['Oxygen saturation in Arterial blood']/row['Oxygen concentration breathed']
    #....
    
    
    #---------------------------
    
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
    # ----------
    
    # Heart rate 
    
    
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
    else:
        igs2_score+=0
    #elif(glasgow_coma_score<=15) :
    #    igs2_score+=0
    #else:
    #    raise ValueError('Glasgow coma score should be lower than 15.')
    
    
    # Oxygenation 
    # ----------
    
    # PaO2/FIO2(mmHg)
    '''
    if (PaO2DivFIO2<100):  
        igs2_score+=11
    elif (PaO2DivFIO2<=199) :
        igs2_score+=9
    else :
        igs2_score+=6
    '''    

    
    # Chemistry  
    # ----------
    
    
    # Chronic diseases and Admission type
    # ----------
    
        

    
    

    return igs2_score

def compute_sofa_score(paO2, platelets, bilirubin, map, dopamine, glasgow_coma_score, creatinine):
    """
    Compute the SOFA score

    Args:
        paO2 (int): 
        platelets (int): 3024929
        bilirubin (int): 3024128
        map (int): 3027598 (got it from map_bp in Pancarte)
        dopamine (int): 1337860
        epinephrine (int):
        norepinephrine (int):
        glasgow-coma_score (int): 3032652
        creatinine (int): 3016723 

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
        
           
    if(dopamine>15):
        sofa_score+=4 
    elif(dopamine>5):
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

