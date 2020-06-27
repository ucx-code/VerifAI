int age,hr,sbp,creatinine,killip,caa,DEPST,TN,risk;
bool out;

active proctype Grace() {
	select(age : 2 .. 10 );
    age= age * 10; //for faster verification
  
    select(hr : 3 .. 25 );
    hr = hr * 10;
  
    select(sbp : 5 .. 25 );
    sbp = sbp * 10;
    
    select(creatinine : 0 .. (40) );

    select(killip : 1 .. 4 );

    select(caa : 0 .. 1 );

    select(DEPST : 0 .. 1 );

    select(TN : 0 .. 1 );

    risk=0;

    if 
    :: age >= 40 && age <= 49 -> risk = risk + 15
    :: age >= 50 && age <= 59 -> risk = risk + 29
    :: age >= 60 && age <= 69 -> risk = risk + 44
    :: age >= 70 && age <= 79 -> risk = risk + 59
    :: age >= 80 && age <= 89 -> risk = risk + 73
    :: age >= 90 -> risk = risk + 80
    :: else -> skip
    fi;

    if
    :: hr >= 70  && hr <= 89  -> risk = risk + 6
    :: hr >= 90  && hr <= 109 -> risk = risk + 12
    :: hr >= 110 && hr <= 149 -> risk = risk + 29
    :: hr >= 150 && hr <= 199 -> risk = risk + 32
    :: hr >= 200 -> risk = risk + 41
    :: else -> skip
    fi;

    if
    :: sbp <  80 -> risk = risk + 57
    :: sbp >= 80  && sbp <= 99  -> risk = risk + 53
    :: sbp >= 100 && sbp <= 119 -> risk = risk + 43
    :: sbp >= 120 && sbp <= 139 -> risk = risk + 34
    :: sbp >= 140 && sbp <= 159 -> risk = risk + 24
    :: sbp >= 160 && sbp <= 199 -> risk = risk + 10
    :: else -> skip
    fi;

    if
    :: creatinine >= 0  && creatinine <= 3 -> risk = risk + 2
    :: creatinine >= 4 && creatinine <= 7 -> risk = risk + 5
    :: creatinine >= 8 && creatinine <= 11 -> risk = risk + 8
    :: creatinine >= 12 && creatinine <= 15 -> risk = risk + 11
    :: creatinine >= 16 && creatinine <= 19 -> risk = risk + 14
    :: creatinine >= 20 && creatinine <= 39 -> risk = risk + 23
    :: creatinine >= 40 -> risk = risk + 31
    :: else -> skip
    fi;

    if
    :: killip == 2 -> risk = risk + 33
    :: killip == 3 -> risk = risk + 67
    :: killip == 4 -> risk = risk + 100
    :: else -> skip
    fi;

    if
    :: caa == 1 -> risk = risk + 98
    :: else -> skip
    fi;

    if 
    :: TN == 1 -> risk = risk + 54  
    :: else -> skip
    fi;         

    if 
    :: DEPST == 1 -> risk = risk + 67
    :: else -> skip
    fi;       
     
    
    if 
    :: risk >= 145 -> out = true
    :: else -> out = false
    fi;

               
}
