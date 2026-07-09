#!/bin/bash

mkdir common_testing_data/unzipped_data

for file in common_testing_data/*.zip; do
    echo "Extracting $file..."
    unzip "$file" -d common_testing_data/unzipped_data
done

mkdir common_training_data/unzipped_data

for file in common_training_data/*.zip; do
    echo "Extracting $file..."
    unzip "$file" -d common_training_data/unzipped_data
done
