#!/bin/bash
#SBATCH --mem=20G
#SBATCH -c10 #SBATCH --time=2:0:0

pip3 install virtualenv
python3 -m venv venv_name
source venv_name/bin/activate  #key step
pip3 install -r requirements.txt --no-cache-dir
