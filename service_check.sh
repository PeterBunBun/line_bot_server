#!/bin/bash

#url='http://100.64.12.14/'
url=$1
attempts=5
timeout=10
online=false

echo "Checking status of $url."

for (( i=1; i<=$attempts; i++ ))
do
  code=`curl -sL --connect-timeout 20 --max-time 30 -w "%{http_code}\\n" "$url" -o /dev/null`

  echo "Found code $code for $url."

  if [ "$code" = "200" ]; then
    echo "Service $url is online."
    online=true
    break
  else
    echo "Service $url seems to be offline. Waiting $timeout seconds."
    sleep $timeout
  fi
done

if $online; then
  echo "Monitor finished, Service is online."
  exit 0
else
  echo "Monitor failed, Service seems to be down."
  exit 1
fi