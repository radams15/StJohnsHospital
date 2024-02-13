#!/usr/bin/env bash

PROJECTS=(sso FinCare CareConnect MediCloud MedRecords Prescriptions)
# PROJECTS=(sso) 

# secret='a-very-long-secret-pls-dont-steal' 
read secret

TERM=gnome-terminal

for proj in ${PROJECTS[@]}
do
    ($TERM --title="$proj" -e "bash run_single.sh $proj '$secret'") &
done
