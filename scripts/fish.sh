#!/bin/bash
# 

source ~/miniconda3/bin/activate
conda init bash
source ~/.bashrc
conda activate td7



python main.py --env='fish-swim' --seed=0 & python main.py --env='fish-swim' --seed=1 & python main.py --env='fish-swim' --seed=2 & python main.py --env='fish-swim' --seed=3 & python main.py --env='fish-swim' --seed=4

wait
