#!/bin/bash

mkdir cleaned_data/untarred_data

for file in cleaned_data/*.tar.gz; do
    echo "Extracting $file..."
    tar -xzf "$file" -C cleaned_data/untarred_data
done
