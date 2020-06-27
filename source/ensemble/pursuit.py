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
        
        #currently not tested!
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