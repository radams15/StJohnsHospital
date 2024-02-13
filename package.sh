#!/usr/bin/env bash

DIRS=(CareConnect FinCare MediCloud sso MedRecords Prescriptions shared)
FILES=(gen_otp.py genssl.sh localhost.key localhost.pem readme.pdf requirements.txt run.py .env)

find . -name __pycache__ -exec rm -rf {} \;

zip -r submission.zip ${DIRS[@]} ${FILES[@]} -x '*.idea*' '*.envrc*'
