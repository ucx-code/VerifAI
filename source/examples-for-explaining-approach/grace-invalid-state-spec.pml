#define AGE_MIN 25
#define AGE_MAX 100
//other risk factor range values...
#define RISK_THRESHOLD 145

int age, risk;
bool patient_in_risk;

active proctype Grace() {

    risk=0;

    select(age : (AGE_MIN) .. (AGE_MAX) );
    if 
    :: age >= 40 && age <= 49 -> risk = risk + 15
    :: age >= 50 && age <= 59 -> risk = risk + 29
    //other age ranges...
    :: age >= 90 -> risk = risk + 80
    fi;

    //other risk factors...

    if 
    :: risk >= (RISK_THRESHOLD) -> patient_in_risk = true
    :: else -> patient_in_risk = false
    fi;
}
