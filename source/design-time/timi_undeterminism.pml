int age,rf,aas,knCAD,angina,depst,tn,risk;
bool out;

active proctype Timi() {

    age = AGE ;
    rf = RF ;
    aas = AAS ;
    knCAD = KNCAD ;
    angina = ANGINA ;
    depst= DEPST ;
    tn= TN ;

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
    :: depst == 1 -> risk = risk + 1 
    :: else -> skip
    fi;       
    if
    :: tn == 1 -> risk = risk + 1
    :: else -> skip
    fi;       
    
    if 
    :: risk >= 4 -> out = true
    :: else -> out = false
    fi;

    assert(out == RISK) 
                
}
