spin -a grace-invalid-state-spec.pml
gcc pan.c -o invalid_end_states -w
./invalid_end_states

spin -t grace-invalid-state-spec.pml
