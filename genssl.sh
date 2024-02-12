#!/usr/bin/env bash

OUT_FOLDER=.

function gen {
    # hostname, out_name
    openssl req -x509 -newkey rsa:4096 -keyout "$OUT_FOLDER/$2.key" -out "$OUT_FOLDER/$2.pem" -sha256 -days 3650 -nodes -subj "/C=GB/ST=West Midlands/L=Coventry/O=St Johns Hospital/OU=Meditech Solutions/CN=$1"
}

# DOMAINS=('sso.stjohns.local') 
#  
# for i in ${DOMAINS[@]} 
# do 
    # gen $i $i 
# done 

gen localhost localhost
