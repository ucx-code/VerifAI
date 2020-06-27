import pandas as pd 
from re import findall
from pickle import dump
from timeit import default_timer as timer
from subprocess import call

def grace(patient_data, risk_factors, risk_threshold=145):
    
    risk=0
    
    for i in range(0, len(risk_factors)):
        factor = risk_factors[i]
        
        if factor == 'Age':
            age = patient_data[i]
            if age >= 40 and age <= 49:
                risk += 15
            elif age >= 50 and age <= 59:
                risk += 29
            elif age >= 60 and age <= 69:
                risk += 44
            elif age >= 70 and age <= 79:
                risk += 59
            elif age >= 80 and age <= 89:
                risk += 73
            elif age >= 90:
                risk += 80
                    
        elif factor == 'HR':
            hr = patient_data[i]
            if hr >= 70 and hr <= 89:
                risk += 6
            elif hr >= 90 and hr <= 109:
                risk  += 12
            elif hr >= 110 and hr <= 149:
                risk += 21
            elif hr >= 150 and hr <= 199:
                risk += 32
            elif hr >= 200:
                risk += 41

        elif factor == 'SBP': 
            sbp = patient_data[i]
            if sbp < 80:
                risk += 57
            elif sbp >= 80 and sbp <= 99: 
                risk += 53
            elif sbp >= 100 and sbp <= 119: 
                risk += 43
            elif sbp >= 120 and sbp <= 139: 
                risk += 34
            elif sbp >= 140 and sbp <= 159: 
                risk += 24
            elif sbp >= 160 and sbp <= 199: 
                risk += 10
        
        elif factor == 'Creat':
            creatinine = patient_data[i]
            if creatinine >= 0 and creatinine <= 0.39:
                risk += 2
            elif creatinine >= 0.4 and creatinine <= 0.79:
                risk += 5
            elif creatinine >= 0.8 and creatinine <= 1.19:
                risk += 8
            elif creatinine >= 1.2 and creatinine <= 1.59:
                risk += 11
            elif creatinine >= 1.6 and creatinine <= 1.99:
                risk += 14
            elif creatinine >= 2 and creatinine <= 3.99:
                risk += 23
            elif creatinine >= 4:
                risk += 31
        
        elif factor == 'KILLIP':
            killip = patient_data[i]
            if killip == 2:
                risk += 33
            elif killip == 3:
                risk += 67
            elif killip == 4:
                risk += 100
            
        elif factor == 'CAA':
            if patient_data[i] == 1:
                risk += 98
            
        elif factor == 'TN':
            if patient_data[i] == 1:
                risk += 54
            
        elif factor == 'DEP ST':
            if patient_data[i] == 1:
                risk += 67

    
    if risk >= risk_threshold:
        patient_in_risk=True
    else:
        patient_in_risk=False
                
    return patient_in_risk

def pursuit(patient_data, risk_factors, risk_threshold=13):    
    
    risk=0
    
    for i in range(0, len(risk_factors)):
        factor = risk_factors[i]    
        
        if factor == 'Age':
            age = patient_data[i]
            if age >= 50 and age <= 59:
                risk += 8
            elif age >= 60 and age <= 69:
                risk += 9
            elif age >= 70 and age <= 79:
                risk += 11
            elif age >= 80:         
                risk += 12
                
        elif factor == 'SEX':
            if patient_data[i] == 1:
                risk += 1
            
        elif factor == 'CCS>II':
            if patient_data[i] == 1:
                risk += 2
        
        elif factor == 'hf':
            if patient_data[i] == 1:
                risk += 2
    
        elif factor == 'DEP ST':
            if patient_data[i] == 1:
                risk += 1      
                
    
    if risk >= risk_threshold:
        patient_in_risk=True
    else:
        patient_in_risk=False
                
    return patient_in_risk

def timi( patient_data, risk_factors, risk_threshold=4):
    
    risk=0
    
    for i in range(0, len(risk_factors)):
        factor = risk_factors[i]    
        
        if factor == 'Age':
            if patient_data[i] >= 65:
                risk += 1
        
        elif factor == 'RF':
            if patient_data[i] == 1:
                risk += 1
            
        elif factor == 'AAS':
            if patient_data[i] == 1:
                risk += 1
            
        elif factor == 'Kn. CAD':
            if patient_data[i] == 1:
                risk += 1
            
        elif factor == 'Angina':
            if patient_data[i] == 1:
                risk += 1
            
        elif factor == 'DEP ST':
            if patient_data[i] == 1:
                risk += 1
            
        elif factor == 'TN':
            if patient_data[i] == 1:
                risk += 1
    
    
    if risk >= risk_threshold:
        patient_in_risk=True
    else:
        patient_in_risk=False
                
    return patient_in_risk


def check_undetermininsm(patient, X_labels, model, output):
    #patient: list with data
    #X_labels: X_labels=['SEX','Age','Enrl','RF','CCS>II','DEP ST','SBP','HR','KILLIP','hf','TN','Creat','CAA','AAS','Angina','Kn. CAD']
    #model: model name (function)
    #output: risk evaluation
    if model==grace:
        #add the patient input data to the model
        call(["spin", "-DAGE=" + str(int(patient[X_labels.index("Age")])), "-DHR="+str(int(patient[X_labels.index("HR")])), "-DSBP="+str(int(patient[X_labels.index("SBP")])), "-DCREAT="+str(int(patient[X_labels.index("Creat")]*10)), "-DKILLIP="+str(int(patient[X_labels.index("KILLIP")])), "-DCAA="+str(int(patient[X_labels.index("CAA")])), "-DDEPST="+str(int(patient[X_labels.index("DEP ST")])), "-DTN="+str(int(patient[X_labels.index("TN")])), "-DRISK="+str(output).lower(),"-a","grace_undeterminism.pml"])
    elif model== pursuit:
        call(["spin", "-DAGE=" + str(int(patient[X_labels.index("Age")])), "-DSEX="+str(int(patient[X_labels.index("SEX")])), "-DCCSII="+str(int(patient[X_labels.index("CCS>II")])), "-DHF="+str(int(patient[X_labels.index("hf")])), "-DDEPST="+str(int(patient[X_labels.index("DEP ST")])), "-DRISK="+str(output).lower(),"-a","pursuit_undeterminism.pml"])
    elif model== timi:
        call(["spin", "-DAGE=" + str(int(patient[X_labels.index("Age")])), "-DRF="+str(int(patient[X_labels.index("RF")])), "-DAAS="+str(int(patient[X_labels.index("AAS")])), "-DKNCAD="+str(int(patient[X_labels.index("Kn. CAD")])), "-DDEPST="+str(int(patient[X_labels.index("DEP ST")])),"-DTN="+str(int(patient[X_labels.index("TN")])),"-DANGINA="+str(int(patient[X_labels.index("Angina")])), "-DRISK="+str(output).lower(),"-a","timi_undeterminism.pml"])

    #compile
    call(["gcc","pan.c", "-o", "pan"])
    
    #call the executer
    call(["./pan"], stdout=open("data_out.txt",'w'))
    
    #read the output
    file=open("data_out.txt",'r')
    filetext=file.read()
    file.close()    
    
    #search for keyword "errors:"
    errors = int(findall("errors:.*\\n",filetext)[0].split()[1])
    
    if errors:
        return False
    
    return True



if __name__=='__main__':
    
    #define the conditions
    event_threshold=40 #days 
    
    #load data
    #file only has relevant data -> feature columns and Event days
    raw_data = pd.read_csv('data_raw_santa_cruz.csv', sep=';')    
    
    #handle missing data -> substitute NaN for the median of the feature
    data = raw_data.fillna(raw_data.median().to_dict())
    
    #change event days to event class -> applying a mask to convert into a Binary classification problem
    data['Event'] = (data['Event'] < event_threshold).astype(int)
    
    #X and y
    X_data= data.drop(columns='Event').values.tolist()
    y_data= data['Event'].tolist() #also works .to_numpy()
    print(sum(y_data))
    
    X_labels=['SEX','Age','Enrl','RF','CCS>II','DEP ST','SBP','HR','KILLIP','hf','TN','Creat','CAA','AAS','Angina','Kn. CAD']
    
    model=timi

    i=1    
    print("===START===")
    
    states_all=[]
    memory_all=[]
    time_all=[]

    t=[]

    y_c=[]
    y_c_p=[]

    y_nc=[]
    y_nc_p=[]

    confident=0
    confident_right=0

    not_confident=0
    not_confident_right=0

    #run for each patient
    for patient, y in zip(X_data,y_data):
        print('\r|Patient: %d/%d|' % (i, len(y_data)),end='')
        i+=1
        
        #apply rs
        risk = model(patient,X_labels)
        t.append(int(risk))
        
        #call
        assess=check_undetermininsm(patient, X_labels, model, risk)
    
        if assess:
            #update confident metrics
            confident+=1
            y_c.append(y)
            y_c_p.append(int(risk))
            if y == risk:
                confident_right+=1
            
        else:
            #update negative metrics
            not_confident+=1
            y_nc.append(y)
            y_nc_p.append(int(risk))                
            if y == risk:
                not_confident_right+=1  

            print('\n',X_labels,'\n',patient,y, risk)

            break

        #read the output for stats
        file=open("data_out.txt",'r')
        filetext=file.read()
        file.close()
        states= int(findall("[0-9]+ transitions",filetext)[0].split()[0])
        memory= float(findall("[0-9]+\.?[0-9]+\ttotal actual memory usage",filetext)[0].split()[0])
        time_elapsed=float(findall("pan: elapsed time.*\\n",filetext)[0].split()[3])
    
        states_all.append(states)
        memory_all.append(memory)
        time_all.append(time_elapsed)

    print("\n===RESULTS===\Deterministic")
    print(confident_right,"right out of ", end='')
    print(confident)
    #print_results(y_c,y_c_p)
    print("Not Deterministic")
    print(not_confident_right,"right out of ", end='')
    print(not_confident)
    #print_results(y_nc,y_nc_p)
    print()

    print("AVG states:",sum(states_all)/len(states_all))
    print("MAX states:",max(states_all))
    print("AVG memory:",sum(memory_all)/len(memory_all))
    print("MAX memory:",max(memory_all))
    print("AVG time:",round(sum(time_all)/len(time_all),6), end=' ')
    print("|| MAX time:",round(max(time_all),6))     
    print("===END RESULTS===\n")  