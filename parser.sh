#!/bin/bash

# Check if the viper virtual environment is activated
echo "Current VIRTUAL_ENV: $CONDA_DEFAULT_ENV"
if [[ "$CONDA_DEFAULT_ENV" != "" && "$(basename "$CONDA_DEFAULT_ENV")" == "viper" ]]; then
    echo "viper virtual environment is already activated. Running the module..."
    # Run the pipeline
    python3 run_viper.py
else
    echo "viper virtual environment is not activated. Running setup.sh..."
    # Run the setup script
    source ./setup.sh
    # After setup, run the pipeline
    python3 run_viper.py
fi