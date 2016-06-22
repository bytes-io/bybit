#!/bin/bash

while read line
do
    echo "commande avec argument:  $line est executee"
done < file.txt
