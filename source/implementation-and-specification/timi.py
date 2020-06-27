#implemented from the CDV Risk Assessment tool

#online tool
#https://www.mdcalc.com/timi-risk-score-ua-nstemi


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
