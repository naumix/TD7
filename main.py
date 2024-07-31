import argparse
import os
import time

import numpy as np
import torch

import TD7
from dmc_gym import make_env_dmc

'''
class Args:
	env: str = 'cheetah-run'
	seed: int = 0
	use_checkpoints: bool = False
	timesteps_before_training: int = 25e2
	eval_freq: int = 5000
	eval_eps: int = 5
	max_timesteps: int = 10000
'''

def maybe_evaluate_and_print(RL_agent, eval_env, evals, t, start_time, args, d4rl=False):
	if t % args.eval_freq == 0:
		print("---------------------------------------")
		print(f"Evaluation at {t} time steps")
		print(f"Total time passed: {round((time.time()-start_time)/60.,2)} min(s)")

		total_reward = np.zeros(args.eval_eps)
		for ep in range(args.eval_eps):
			state, done = eval_env.reset(), False
			while not done:
				action = RL_agent.select_action(np.array(state), args.use_checkpoints, use_exploration=False)
				state, reward, _, done, _ = eval_env.step(action)
				state = state[0]
				reward = reward[0]
				done = done[0]
                
				total_reward[ep] += reward

		print(f"Average total reward over {args.eval_eps} episodes: {total_reward.mean():.3f}")
		print("---------------------------------------")

		evals.append(total_reward)
		np.save(f"./results/{args.file_name}", evals)

def train_online(RL_agent, env, eval_env, args):
	evals = []
	start_time = time.time()
	allow_train = False

	state, ep_finished = env.reset()[0], False
	ep_total_reward, ep_timesteps, ep_num = 0, 0, 1

	for t in range(int(args.max_timesteps+1)):
		maybe_evaluate_and_print(RL_agent, eval_env, evals, t, start_time, args)
		
		if allow_train:
			action = RL_agent.select_action(np.array(state))
		else:
			action = env.action_space.sample()

		next_state, reward, _, ep_finished, _ = env.step(action)
		next_state = next_state[0]
		reward = reward[0]
		ep_finished = ep_finished[0]
		
		ep_total_reward += reward
		ep_timesteps += 1

		done = float(ep_finished) if ep_timesteps < 1000 else 0
		RL_agent.replay_buffer.add(state, action, next_state, reward, done)

		state = next_state

		if allow_train and not args.use_checkpoints:
			RL_agent.train()

		if ep_finished: 
			print(f"Total T: {t+1} Episode Num: {ep_num} Episode T: {ep_timesteps} Reward: {ep_total_reward:.3f}")

			if allow_train and args.use_checkpoints:
				RL_agent.maybe_train_and_checkpoint(ep_timesteps, ep_total_reward)

			if t >= args.timesteps_before_training:
				allow_train = True

			state, done = env.reset(), False
			ep_total_reward, ep_timesteps = 0, 0
			ep_num += 1 
            
            
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	# RL
	parser.add_argument("--env", default="HalfCheetah-v4", type=str)
	parser.add_argument("--seed", default=0, type=int)
	parser.add_argument('--use_checkpoints', default=False, action=argparse.BooleanOptionalAction)
    
	# Evaluation
	parser.add_argument("--timesteps_before_training", default=25e3, type=int)
	parser.add_argument("--eval_freq", default=25000, type=int)
	parser.add_argument("--eval_eps", default=5, type=int)
	parser.add_argument("--max_timesteps", default=1e6, type=int)
	# File
	args = parser.parse_args()
	
	if not os.path.exists("./results"):
		os.makedirs("./results")
	#args = Args()
	args.file_name = f"TD7_{args.env}_{args.seed}"
	env = make_env_dmc('cheetah-run', args.seed, 1)
	eval_env = make_env_dmc('cheetah-run', args.seed+42, 1)

	print("---------------------------------------")
	print(f"Algorithm: TD7, Env: {args.env}, Seed: {args.seed}")
	print("---------------------------------------")

	env.seed(args.seed)
	env.action_space.seed(args.seed)
	eval_env.seed(args.seed+100)
	torch.manual_seed(args.seed)
	np.random.seed(args.seed)
	
	state_dim = env.observation_space.shape[1]
	action_dim = env.action_space.shape[1] 
	max_action = 1

	RL_agent = TD7.Agent(state_dim, action_dim, max_action, False)

	train_online(RL_agent, env, eval_env, args)