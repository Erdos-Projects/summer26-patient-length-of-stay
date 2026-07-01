#!/bin/bash

mkdir cleaned_data/unzipped_data

for file in cleaned_data/*.zip; do
    echo "Extracting $file..."
    unzip "$file" -d cleaned_data/unzipped_data
done
