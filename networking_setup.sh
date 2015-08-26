#!/usr/bin/env bash

# Generate SSH Key
echo "Enter calvr user password"
read -s calvrPassword

ssh-keygen -q -t rsa -f ~/.ssh/id_rsa -N ""

thisHost=$(hostname)
hostsArray=( "headnode" "CNEA-0" "CNEA-1" "CNEA-2" "CNEA-3" "CNEA-4" )

for host in "${hostsArray[@]}"
do
  if [[ $(hostname) == $host ]]; then
    echo "This host, nothing to do"
  else
    echo "Copying key to $host"
    echo $calvrPassword | ssh-copy-id $host
  fi
done
