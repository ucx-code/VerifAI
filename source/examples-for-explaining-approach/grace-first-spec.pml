#define AGE
//other risk factor values...
#define RISK_THRESHOLD

int age, risk;
bool patient_in_risk;

active proctype Grace() {

    risk=0;

    age= AGE;
    if 
    :: age >= 40 && age <= 49 -> risk = risk + 15
    :: age >= 50 && age <= 59 -> risk = risk + 29
    //other age ranges...
    :: age >= 90 -> risk = risk + 80
    fi;

    //other risk factors...

    if 
    :: risk >= RISK_THRESHOLD -> patient_in_risk = true
    :: else -> patient_in_risk = false
    fi;
}