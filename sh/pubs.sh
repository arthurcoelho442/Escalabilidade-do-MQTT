#!/bin/bash
numPublishers=100;
simTime=1; # customize it
host="localhost";
topic="teste";
attr="temp";
msgTime=100;
for i in $(seq 1 $numPublishers);
 do
    nohup python3 publisher.py "$host" "$topic" "$attr" "$msgTime" > ../resultados/usuarios/pub_$i.log  &    
done 
sleep "$simTime"
killall python3
