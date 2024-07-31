#!/bin/bash
# 

source ~/miniconda3/bin/activate
conda init bash
source ~/.bashrc
conda activate td7



python main.py --env='pendulum-swingup' --seed=0 & python main.py --env='pendulum-swingup' --seed=1 & python main.py --env='pendulum-swingup' --seed=2 & python main.py --env='pendulum-swingup' --seed=3 & python main.py --env='pendulum-swingup' --seed=4

wait
