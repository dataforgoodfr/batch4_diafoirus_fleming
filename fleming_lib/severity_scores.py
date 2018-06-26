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
        
        'Sodium serum/plasma' (float): mEq/L
        'Potassium serum/plasma' (float) : mEq/L
        'Total Bilirubin serum/plasma' (float) : mg/dL
        'Leukocytes [#/volume] in Blood by Manual count'

    Returns:
        igs2_score (int): score
    """
    
    
    
    igs2_score = 0 
    
    # Components
    age = row['age']
    systolic_bp = row ['BP systolic']
    temp = row['bodyTemperature_C']
    glasgow_coma_score = row['Glasgow coma scale']
    
    PaO2 = row['Oxygen saturation in Arterial blood']
    FIO2 = row['Oxygen concentration breathed']
    if pd.isna(FIO2) or FIO2==0.0:
        PaO2DivFIO2 ='NaN'
    else: 
        PaO2DivFIO2 = PaO2/FIO2
        
    natremie = row['Sodium serum/plasma']
    kaliemie = row['Potassium serum/plasma']
    bilirubin = 10*row['Total Bilirubin serum/plasma'] # convert to mg/L (as in http://www.sfar.org/scores/igs2_expanded.php)
    leukocytes = row['Leukocytes [#/volume] in Blood by Manual count']

    #TODO : Replace each "if ():" by "if .. is null (Nan) : then null"
    
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

    if (type(PaO2DivFIO2) == str):
        igs2_score+=0
    else:
        if (PaO2DivFIO2<100):  
            igs2_score+=11
        elif (PaO2DivFIO2<=199) :
            igs2_score+=9
        else :
            igs2_score+=6
        
    
    
    # Chemistry  
    # ----------
    
    # sodium serum/plasma (en) | natremie (fr)
    if (natremie<125):  
        igs2_score+=5
    elif (natremie<=144) :
        igs2_score+=0
    else :
        igs2_score+=1
    
    
    # potassium serum/plasma (en) | kaliemie (fr)
    
    if (type(kaliemie) == str):
        igs2_score+=0
    else:   
        if (kaliemie<3):  
            igs2_score+=3
        elif (kaliemie<=4.9) :
            igs2_score+=0
        else :
            igs2_score+=3
        
    # bilirubin 
    if (bilirubin<40):  
        igs2_score+=0
    elif (bilirubin<60) :
        igs2_score+=4
    else :
        igs2_score+=9
  
    # Hemato 
    # ----------
    
    # Leukocytes
    if type(leukocytes) == str:
        igs2_score+=0
    else :
        if (leukocytes>=20):  
            igs2_score+=3
        elif (leukocytes > 1.0) :
            igs2_score+=0
        else :
            igs2_score+=12
        
        
    # Chronic diseases and Admission type
    # ----------
    
        

    
    

    return igs2_score

def compute_sofa_score(row):
    """
    Compute the SOFA score

    Args:
        #measurement                concept_id
        paO2/FiO2 (float):          4233883 
        platelets (float):          3024929
        bilirubin (float):          3024128
        map (float):                3027598         
        glasgow-coma_score (float): 3032652
        creatinine (float):         3016723 

        #drugs
        dopamine (float):           1337860
        epinephrine (float):        1343916 / 1344056
        norepinephrine (float):     1321341 / 1321364
        dobutamine (float):         1337720

    Returns:
        sofa_score (int): SOFA score 
    """
   
    sofa_score = 0 

    if 'Oxygen saturation in Arterial blood' in row:

        paO2FiO2= row['Oxygen saturation in Arterial blood']
    
        if(paO2FiO2<100):
            sofa_score+=4 
        elif(paO2FiO2<200):
            sofa_score+=3
        elif(paO2FiO2<300):
            sofa_score+=2
        elif(paO2FiO2<400):
            sofa_score+=1

    if 'Platelets [#/volume] in Blood by Automated count' in row:

        platelets=row['Platelets [#/volume] in Blood by Automated count']

        if(platelets<20):
            sofa_score+=4 
        elif(platelets<50):
            sofa_score+=3
        elif(platelets<100):
            sofa_score+=2
        elif(platelets<150):
            sofa_score+=1  

    if 'Total Bilirubin serum/plasma' in row:

        bilirubin=row['Total Bilirubin serum/plasma']
        
        if(bilirubin>204):
            sofa_score+=4 
        elif(bilirubin>=102):
            sofa_score+=3
        elif(bilirubin>=33):
            sofa_score+=2
        elif(bilirubin>=20):
            sofa_score+=1
            

    if 'Dopamine' in row:

        dopamine=row['Dopamine']      

        if(dopamine>15):
            sofa_score+=4 
        elif(dopamine>5):
            sofa_score+=3
        elif(dopamine<=5):
            sofa_score+=2
    elif 'Norepinephrine' in row:

        norepinephrine=row['Norepinephrine']

        if(norepinephrine>0.1):
            sofa_score+=4
        else:
            sofa_score+=3

    elif 'Epinephrine' in row:

        epinephrine=row['Epinephrine']

        if(epinephrine>0.1):
            sofa_score+=4
        else:
            sofa_score+=3

    elif 'Dobutamine' in row:

        dobutamine=row['Dobutamine']

        if(dobutamine>0):
            sofa_score+=2

    elif 'Mean blood pressure' in row:

        mbp=row['Mean blood pressure']

        if(mbp<70):
            sofa_score+=1

    if 'Glasgow coma scale' in row:

        glasgow_coma_score=row['Glasgow coma scale']    

        if(glasgow_coma_score<6):
            sofa_score+=4 
        elif(glasgow_coma_score>=6 and glasgow_coma_score<=9):
            sofa_score+=3
        elif(glasgow_coma_score>=10 and glasgow_coma_score<=12):
            sofa_score+=2
        elif(glasgow_coma_score>=13 and glasgow_coma_score<=14):
            sofa_score+=1
    

    if 'Creatinine serum/plasma' in row:

        creatinine=row['Creatinine serum/plasma']    

        if(creatinine>50):
            sofa_score+=4 
        elif(creatinine>=35 and creatinine <=49):
            sofa_score+=3
        elif(creatinine>=20 and creatinine <=34):
            sofa_score+=2
        elif(creatinine>=12 and creatinine <=19):
            sofa_score+=1

    

    return sofa_score