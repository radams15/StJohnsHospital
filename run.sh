#!/usr/bin/env bash

PROJECTS=(sso FinCare CareConnect MediCloud MedRecords Prescriptions)
# PROJECTS=(sso) 

# secret='a-very-long-secret-pls-dont-steal' 
read secret

TERM=xterm

for proj in ${PROJECTS[@]}
do
    ($TERM -T "$proj" -e "bash run_single.sh $proj '$secret'") &
done
