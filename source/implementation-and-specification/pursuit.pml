int age,sex,ccsII,hf,DEPST,risk;
bool out;

active proctype Pursuit() {

    select(age : 1 .. 10 );
    age= age*10;
    select(sex : 0 .. 1 );
    select(ccsII : 0 .. 1 );
    select(hf : 0 .. 1 );
    select(DEPST : 0 .. 1 );

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
    :: DEPST == 1 -> risk = risk + 1 
    :: else -> skip
    fi;       
    
    
    if 
    :: risk >= 13 -> out = true
    :: else -> out = false
    fi;
                
}
