#implemented from the CDV Risk Assessment tool

#online tool
#https://www.mdcalc.com/grace-acs-risk-mortality-calculator#evidence

def grace(patient_data, risk_factors, risk_threshold=145,debug=False):
    
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
    
    if debug:
        print(risk)
        
    if risk >= risk_threshold:
        patient_in_risk=True
    else:
        patient_in_risk=False
                
    return patient_in_risk

if __name__=='__main__':
    grace()