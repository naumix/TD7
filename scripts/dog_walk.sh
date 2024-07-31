#!/bin/bash
# 

source ~/miniconda3/bin/activate
conda init bash
source ~/.bashrc
conda activate td7



python main.py --env='dog-walk' --seed=0 & python main.py --env='dog-walk' --seed=1 & python main.py --env='dog-walk' --seed=2 & python main.py --env='dog-walk' --seed=3 & python main.py --env='dog-walk' --seed=4

wait
