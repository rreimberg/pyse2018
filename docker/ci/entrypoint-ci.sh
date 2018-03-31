#!/bin/bash

# Application execution
echo "Checking DB service availability..."
while true; do
    ANSWER=`nmap -sS -O mysql.docker -p 3306 | egrep '^'3306'/tcp' |egrep -v 'close'| wc -c`
    [ $ANSWER -gt 0 ] &&{
        break
    }
    sleep 1
    echo "."
done

echo "Starting development server"

cd /source/ && pytest -vv tests/integration/
