#!/usr/bin/env bash

CERT=`pwd`/localhost.pem
KEY=`pwd`/localhost.key

function run {
    # project_name, host, port
    echo "Running $1 at $2:$3"
    cd $1 && python3 -m flask run --host=$2 --port=$3 --cert=$CERT --key=$KEY && cd ..
}

source ./MediCloud/venv/bin/activate

port=0
case $1 in
    FinCare)
        port=3333
        ;;
    MediCloud)
        port=5555
        ;;

    MedRecords)
        port=2222
        ;;

    Prescriptions)
        port=4444
        ;;

    CareConnect)
        port=3355
        ;;

    sso)
        port=1111
        ;;
esac

run $1 0.0.0.0 $port
