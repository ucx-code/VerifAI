from subprocess import call
from re import findall
from copy import deepcopy

def within_confidence_region(patient, X_labels, model, output):
    #patient: list with data
    #X_labels: ['SEX','Age','Enrl','RF','CCS>II','DEP ST','SBP','HR','KILLIP','TN','Creat','CAA','AAS','Angina','Kn. CAD']
	#model: model name (function)
    #output: risk evaluation

    #add the patient input data to the model
    call(["spin", "-DAGE=" + str(int(patient[X_labels.index("Age")])), "-DHR="+str(int(patient[X_labels.index("HR")])), "-DSBP="+str(int(patient[X_labels.index("SBP")])), "-DCREAT="+str(int(patient[X_labels.index("Creat")]*10)), "-DKILLIP="+str(int(patient[X_labels.index("KILLIP")])), "-DCAA="+str(int(patient[X_labels.index("CAA")])), "-DDEPST="+str(int(patient[X_labels.index("DEP ST")])), "-DTN="+str(int(patient[X_labels.index("TN")])), "-DRISK="+str(output).lower(),"-a","grace_online.pml"])
    
    #compile
    call(["gcc","pan.c", "-o", "pan",'-Wno-overlength-strings','-Wno-format-overflow','-w'])
    
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


def explain_negative(patient, X_labels, model, output):
    
    #spin -t model.pml
    call(["spin","-t","-DAGE=" + str(int(patient[X_labels.index("Age")])), "-DHR="+str(int(patient[X_labels.index("HR")])), "-DSBP="+str(int(patient[X_labels.index("SBP")])), "-DCREAT="+str(int(patient[X_labels.index("Creat")]*10)), "-DKILLIP="+str(int(patient[X_labels.index("KILLIP")])), "-DCAA="+str(int(patient[X_labels.index("CAA")])), "-DDEPST="+str(int(patient[X_labels.index("DEP ST")])), "-DTN="+str(int(patient[X_labels.index("TN")])), "-DRISK="+str(output).lower(),"-t","grace_online.pml"], stdout=open("explanation.txt",'w'))