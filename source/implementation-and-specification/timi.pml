int age,rf,aas,knCAD,angina,DEPST,TN,risk;
bool out;

active proctype Timi() {

    select(age : 1 .. 10 );
    age= age*10;
    select(rf : 0 .. 1 );
    select(aas : 0 .. 1 );
    select(knCAD : 0 .. 1 );
    select(angina : 0 .. 1 );
    select(DEPST : 0 .. 1 );
    select(TN: 0 .. 1 );

    risk=0;

    if 
    :: age >= 65 -> risk = risk + 1
    :: else -> skip
    fi;
    if
    :: rf == 1 -> risk = risk + 1
    :: else -> skip
    fi;
    if
    :: aas == 1 -> risk = risk + 1
    :: else -> skip
    fi;
    if 
    :: knCAD == 1 -> risk = risk + 1  
    :: else -> skip
    fi;
    if 
    :: angina == 1 -> risk = risk + 1
    :: else -> skip
    fi;          
    if 
    :: DEPST == 1 -> risk = risk + 1 
    :: else -> skip
    fi;       
    if
    :: TN == 1 -> risk = risk + 1
    :: else -> skip
    fi;       
    
    if 
    :: risk >= 4 -> out = true
    :: else -> out = false
    fi;
                
}
