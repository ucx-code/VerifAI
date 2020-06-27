from subprocess import call
from re import findall
from copy import deepcopy
from grace import grace

def within_confidence_region_spin(patient, X_labels, output):
    #patient: list with data
    #X_labels: ['SEX','Age','Enrl','RF','CCS>II','DEP ST','SBP','HR','KILLIP','TN','Creat','CAA','AAS','Angina','Kn. CAD']
    #output: risk evaluation
    #model: model name (function)

    #add the patient input data to the model
    #print(str(int(patient[X_labels.index("Creat")])))
    call(["spin", "-DAGE=" + str(int(patient[X_labels.index("Age")])), "-DHR="+str(int(patient[X_labels.index("HR")])), "-DSBP="+str(int(patient[X_labels.index("SBP")])), "-DCREAT="+str(int(patient[X_labels.index("Creat")]*10)), "-DKILLIP="+str(int(patient[X_labels.index("KILLIP")])), "-DCAA="+str(int(patient[X_labels.index("CAA")])), "-DDEPST="+str(int(patient[X_labels.index("DEP ST")])), "-DTN="+str(int(patient[X_labels.index("TN")])), "-DRISK="+str(output).lower(),"-a","grace_online.pml"])
    
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

def explain_negative_spin(patient, X_labels, model, output):
    
    #spin -t model.pml
    call(["spin","-t","-DAGE=" + str(int(patient[X_labels.index("Age")])), "-DHR="+str(int(patient[X_labels.index("HR")])), "-DSBP="+str(int(patient[X_labels.index("SBP")])), "-DCREAT="+str(int(patient[X_labels.index("Creat")]*10)), "-DKILLIP="+str(int(patient[X_labels.index("KILLIP")])), "-DCAA="+str(int(patient[X_labels.index("CAA")])), "-DDEPST="+str(int(patient[X_labels.index("DEP ST")])), "-DTN="+str(int(patient[X_labels.index("TN")])), "-DRISK="+str(output).lower(),"-t","grace_online.pml"], stdout=open("explanation.txt",'w'))


def within_confidence_region_python(patient, X_labels, output, model=grace, range_params= [4,4,5,5,3,3,1,1]):
    #patient: list with patient data
    #X_labels: ['SEX','Age','Enrl','RF','CCS>II','DEP ST','SBP','HR','KILLIP','TN','Creat','CAA','AAS','Angina','Kn. CAD']
    #output: patient risk evaluation
    
    #model: model name (function) <- for now only grace
    #range_params: search ranges <-for now only for grace

    p_test=deepcopy(patient)
    for age in range(int(patient[X_labels.index("Age")])-range_params[0],int(patient[X_labels.index("Age")])+range_params[1]+1):
        p_test[X_labels.index("Age")]=age

        for hr in range(int(patient[X_labels.index("HR")])-range_params[2],int(patient[X_labels.index("HR")])+range_params[3]+1):
            p_test[X_labels.index("HR")]=hr
            
            for sbp in range(int(patient[X_labels.index("SBP")])-range_params[4],int(patient[X_labels.index("SBP")])+range_params[5]+1):
                p_test[X_labels.index("SBP")]=sbp

                for creatinine in range(int(patient[X_labels.index("Creat")]*10)-range_params[6],int(patient[X_labels.index("Creat")]*10)+range_params[7]+1):
                    p_test[X_labels.index("Creat")]=creatinine/10
		    
                    risk_=model(p_test,X_labels)
                    
                    if risk_ != output:
                        return False
    return True