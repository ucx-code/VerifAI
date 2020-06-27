
int age,sex,ccsII,hf,depst,risk;
bool out;

active proctype Pursuit() {

    age = AGE;
    sex = SEX;
    ccsII = CCSII;
    hf = HF;
    depst = DEPST;

    risk=0;

    if 
    :: age >= 50 && age <= 59 -> risk = risk + 8
    :: age >= 60 && age <= 69 -> risk = risk + 9
    :: age >= 70 && age <= 79 -> risk = risk + 11
    :: age >= 80 -> risk = risk + 12
    :: else -> skip
    fi;

    if
    :: sex == 1 -> risk = risk + 1
    :: else -> skip
    fi;
    if
    :: ccsII == 1 -> risk = risk + 2
    :: else -> skip
    fi;
    if 
    :: hf == 1 -> risk = risk + 2  
    :: else -> skip
    fi;       
    if 
    :: depst == 1 -> risk = risk + 1 
    :: else -> skip
    fi;       
    
    
    if 
    :: risk >= 13 -> out = true
    :: else -> out = false
    fi;

    assert(out == RISK) 
                
}
