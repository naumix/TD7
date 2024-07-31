#!/bin/bash
# 

source ~/miniconda3/bin/activate
conda init bash
source ~/.bashrc
conda activate td7



python main.py --env='acrobot-swingup' --seed=0 & python main.py --env='acrobot-swingup' --seed=1 & python main.py --env='acrobot-swingup' --seed=2 & python main.py --env='acrobot-swingup' --seed=3 & python main.py --env='acrobot-swingup' --seed=4

wait
