#!/bin/bash

echo "Current directory: $(pwd)"

# 1. Check if mamba is installed; if not, install Miniforge and mamba
if ! command -v mamba &> /dev/null
then
    echo "mamba not found. Installing Miniforge (comes with conda)..."
    
    # Download Miniforge installer
    wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O Miniforge3.sh
    
    # Install Miniforge silently
    chmod +x $(pwd)/config/Miniforge3.sh
    bash $(pwd)/config/Miniforge3.sh -b -p $HOME/miniforge3

    # Add conda to PATH
    export PATH="$HOME/miniforge3/bin:$PATH"

    # Initialize conda
    source $HOME/miniforge3/etc/profile.d/conda.sh
    
    # Install mamba via conda
    conda install -y mamba -n base -c conda-forge

    echo "mamba successfully installed."
else
    echo "mamba is already installed."
fi

# 2. Create a virtual environment using mamba and specify Python 3.10
echo "Creating a virtual environment named 'viper' with Python 3.10..."
mamba create -y -n viper python=3.10

# 3. Activate the virtual environment
echo "Activating the 'viper' virtual environment..."
source $HOME/miniforge3/etc/profile.d/conda.sh  # Ensure conda is initialized in the current shell
mamba activate viper

# 4. Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# 5. Install core dependencies
echo "Installing core dependencies..."
# Make sure the requirements.txt file is executable
chmod +x $(pwd)/config/requirements.txt
pip install -r $(pwd)/config/requirements.txt

echo "Setup complete."