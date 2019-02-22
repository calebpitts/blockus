#!/bin/bash

for i in `seq 1 ${1}`;
        do
                echo "Run ${i}"
                python -m blockus.blockus_client
        done 


