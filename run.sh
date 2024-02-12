#!/usr/bin/env bash

PROJECTS=(sso FinCare MediCloud MedRecords Prescriptions)
# PROJECTS=(sso) 

TERM=xterm

for proj in ${PROJECTS[@]}
do
    ($TERM -e "bash run_single.sh $proj") &
done
