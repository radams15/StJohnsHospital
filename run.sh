#!/usr/bin/env bash

PROJECTS=(sso FinCare CareConnect MediCloud MedRecords Prescriptions)
# PROJECTS=(sso) 

SECRET='a-very-long-secret-pls-dont-steal'
# SECRET='the-wrong-secret' 

TERM=xterm

for proj in ${PROJECTS[@]}
do
    ($TERM -T "$proj" -e "bash run_single.sh $proj '$SECRET'") &
done
