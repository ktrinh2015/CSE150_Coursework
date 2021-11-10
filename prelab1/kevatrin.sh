#!/bin/bash

i=0
num=0

for file in "$search_dir"*; do
    if[ "$file" != *"kevatrin"* ]
    then
       while IFS= read -r line  
       do
          i=$((i+1))
          num=$(($i%2))
          if[ $num -ne 1 ]
          then
             echo "line $i" 
       done <"$file" 
    i=0
done 
