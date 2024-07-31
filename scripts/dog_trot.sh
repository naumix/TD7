#!/bin/bash
# 

source ~/miniconda3/bin/activate
conda init bash
source ~/.bashrc
conda activate td7

module load CUDA/12.0.0

python main.py --env='dog-trot' --seed=0 & python main.py --env='dog-trot' --seed=1 & python main.py --env='dog-trot' --seed=2 & python main.py --env='dog-trot' --seed=3 & python main.py --env='dog-trot' --seed=4

wait
