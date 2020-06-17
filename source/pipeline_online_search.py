import pandas as pd 
from re import findall
from pickle import dump
from timeit import default_timer as timer

from confidence import within_confidence_region, explain_negative
from grace import grace
from results_online_verification import print_results


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
    
    #drop KILLIP or HF(signs) because they have .94 correlation
    data= data.drop(columns='HF (signs)')
    
    #X and y
    X_data= data.drop(columns='Event').values.tolist()
    y_data= data['Event'].tolist() #also works .to_numpy()
    print(sum(y_data))
    
    X_labels=['SEX','Age','Enrl','RF','CCS>II','DEP ST','SBP','HR','KILLIP','TN','Creat','CAA','AAS','Angina','Kn. CAD']
    
    model=grace

    set_=[4,4,5,5,3,3,1,1]

    i=1    
    print("===START=== for", end=' ')
    print('age=+-'+str(set_[0])+",hr=+-"+str(set_[2])+",sbp=+-"+str(set_[4])+",creat=+-"+str(set_[6]))
    
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
        
        #call online verification
        assess=within_confidence_region(patient, X_labels, model, risk)
    
        if assess:
            #update confident metrics
            confident+=1
            y_c.append(y)
            y_c_p.append(int(risk))
            if y == risk:
                confident_right+=1
            
        else:
            #explain why it is not confident
            #explain_negative(patient, X_labels,model, risk)

            #update negative metrics
            not_confident+=1
            y_nc.append(y)
            y_nc_p.append(int(risk))                
            if y == risk:
                not_confident_right+=1  

            #print('\n',X_labels,'\n',patient,y, risk)

            #break

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

    print("\n===RESULTS===\nConfident")
    print(confident_right,"right out of ", end='')
    print(confident)
    print_results(y_c,y_c_p)
    print("Not confident")
    print(not_confident_right,"right out of ", end='')
    print(not_confident)
    print_results(y_nc,y_nc_p)
    print()

    print("AVG states:",sum(states_all)/len(states_all))
    print("MAX states:",max(states_all))
    print("AVG memory:",sum(memory_all)/len(memory_all))
    print("MAX memory:",max(memory_all))
    print("AVG time:",round(sum(time_all)/len(time_all),6), end=' ')
    print("|| MAX time:",round(max(time_all),6))     
    print("===END RESULTS===\n")  