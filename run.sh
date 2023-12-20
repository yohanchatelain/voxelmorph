#!/bin/bash

mkdir -p inputs outputs stats/sig/{inputs,outputs}

./generate_inputs.sh
./compute_significant_digits_inputs.sh
./run_synthmorph.sh
./compute_significant_digits_outputs.sh

