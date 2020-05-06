from goal_inference import infer_goal
from pddlgym.planning import run_async_value_iteration, vi_finish_helper
from collections import OrderedDict, defaultdict
import gym
import time
import pddlgym
import pickle
import os
import numpy as np
import sys

# Hyperparameters
outdir = 'results'
do_precomputation = True
test_qvals = True
do_goal_inference = True
test_goal_inference = True
vi_maxiters = { True : 10000, False : 10000 } # biased? : max_iters
horizon = 100
gamma = 0.9 # todo optimize
beta = 1. # todo optimize
env_names = [
    "InversePlanningBlocks-v0",
    "InversePlanningIntrusionDetection-v0",
    "InversePlanningGrid-v0",
    "InversePlanningLogistics-v0",
    "InversePlanningCampus-v0",
    "InversePlanningKitchen-v0",
]

def create_headers():
    """headers[env_name][initial_state] -> [goals]"""
    headers = OrderedDict()
    for env_name in env_names:
        headers[env_name] = OrderedDict()
        env = gym.make(env_name)
        # Group the problems that have the same initial state but different goals
        problem_prefix_to_group = defaultdict(list)
        for problem in env.problems:
            fname_alone = os.path.split(problem.problem_fname)[-1]
            split = fname_alone.split("_")
            prefix = "_".join(split[:-1])
            goal = split[-1][:-len(".pddl")]
            problem_prefix_to_group[prefix].append(goal)
        problem_prefixes = sorted(problem_prefix_to_group)

        for initial_state in problem_prefixes:
            headers[env_name][initial_state] = problem_prefix_to_group[initial_state]

    print("All headers:")
    for env_name in headers:
        print(env_name)
        for initial_state in headers[env_name]:
            print("  {}".format(initial_state))
            print("    {}".format(headers[env_name][initial_state]))

    return headers

def get_qval_run_id(env_name, initial_state, goal, biased):
    return "qval_run_{}_{}_{}_{}".format(env_name, initial_state, goal, biased)

def get_goal_inference_run_id(env_name, initial_state, goal, biased):
    return "goal_inference_run_{}_{}_{}_{}".format(env_name, initial_state, goal, biased)

def save_results(run_id, results):
    outfile = os.path.join(outdir, run_id + '.pkl')
    with open(outfile, 'wb') as f:
        pickle.dump(results, f)
    print("Dumped results to {}.".format(outfile))

def load_results(run_id):
    outfile = os.path.join(outdir, run_id + '.pkl')
    with open(outfile, 'rb') as f:
        results = pickle.load(f)
    return results

def create_env(env_name, initial_state, goal):
    env = gym.make(env_name)
    problem_fname = initial_state + '_' + goal + '.pddl'
    found_problems = [os.path.split(p.problem_fname)[-1] == problem_fname for p in env.problems]
    assert sum(found_problems) == 1
    problem_index = np.argwhere(found_problems)[0,0]
    env.fix_problem_index(problem_index)
    env.reset()
    return env

def compute_qvals(env_name, initial_state, goal, biased):
    env = create_env(env_name, initial_state, goal)
    qvals = next(run_async_value_iteration(env, iter_plans=False, use_cache=False,
                gamma=gamma, epsilon=0., vi_maxiters=vi_maxiters[biased], biased=biased, ret_qvals=True))
    return qvals

def run_test_qvals(env_name, initial_state, goal, qvals):
    env = create_env(env_name, initial_state, goal)
    obs, _ = env.reset()
    plan = vi_finish_helper(env, obs, qvals, actions_for_state=None, horizon=horizon)
    total_reward = 0
    for action in plan:
        _, reward, _, _ = env.step(action)
        total_reward += reward
    print("Reward accrued following qvals:", total_reward)

def get_demonstration(env_name, initial_state, goal):
    env = create_env(env_name, initial_state, goal)
    plan = env.load_demonstration_for_problem()
    states = env.run_demo(plan)
    assert len(states) == len(plan) + 1
    demonstration = list(zip(states[:-1], plan))
    return demonstration
    # Uncomment to get a demonstration using computed qvals
    # demonstration = []
    # env = create_env(env_name, initial_state, goal)
    # obs, _ = env.reset()
    # plan = next(run_async_value_iteration(env, iter_plans=False, use_cache=False, gamma=gamma,
    #     epsilon=0., vi_maxiters=vi_maxiters[True], biased=True, ret_qvals=False, horizon=horizon))
    # for action in plan:
    #     demonstration.append((obs, action))
    # return demonstration

def compute_goal_inference_posteriors(demonstration, goals, goal_qvals, env_name, initial_state, goal):
    env = create_env(env_name, initial_state, goal)  # Just for valid actions
    goal_distribution_per_step = [np.ones(len(goals)) / len(goals)]
    valid_action_time_total = 0
    for t in range(1, len(demonstration)):
        demo_t = demonstration[:t]
        # Run goal inference
        goal_distribution, valid_action_time = infer_goal(demo_t, goal_qvals, env, beta=beta)
        valid_action_time_total += valid_action_time
        goal_distribution_per_step.append(goal_distribution)
    return goal_distribution_per_step, valid_action_time_total

def run_test_goal_inference(goals, goal, posteriors):
    goal_idx = goals.index(goal)
    half_posterior = np.array(posteriors[len(posteriors)//2])
    last_posterior = np.array(posteriors[-1])
    print("Goal is top at half?", goal_idx in np.argwhere(half_posterior == max(half_posterior)))
    print("Goal is top at end?", goal_idx in np.argwhere(last_posterior == max(last_posterior)))


def report_results():
    raise NotImplementedError()    

def run_pipeline(biased):
    """
    Precomputation phase:
    Environments x Initial States x Goals --> { 'qvals' : Value function, 'time' : s }

    Goal inference phase:
    Environments x Initial States x Goals  --> { 'posteriors' : Trajectory Length x Goals --> Float, 'time'  : s }
    """
    headers = create_headers()

    if do_precomputation or do_goal_inference:
        for env_name in env_names:
            for initial_state in headers[env_name]:
                # Value function precomputation
                for goal in headers[env_name][initial_state]:
                    qval_run_id = get_qval_run_id(env_name, initial_state, goal, biased=biased)
                    if do_precomputation:
                        start_time = time.time()
                        qvals = compute_qvals(env_name, initial_state, goal, biased=biased)
                        time_elapsed = time.time() - start_time
                        results = {"qvals" : qvals, "time_elapsed" : time_elapsed}
                        save_results(qval_run_id, results)
                        if test_qvals:
                            run_test_qvals(env_name, initial_state, goal, qvals)

                # Goal inference
                for goal in headers[env_name][initial_state]:
                    gi_run_id = get_goal_inference_run_id(env_name, initial_state, goal, biased=biased)
                    if do_goal_inference:
                        # Get demonstration
                        demonstration = get_demonstration(env_name, initial_state, goal)
                        # Load qvals for all goals
                        goals = headers[env_name][initial_state]
                        goal_qvals = []
                        for g in goals:
                            qval_q_run_id = get_qval_run_id(env_name, initial_state, g, biased=biased)
                            results_g = load_results(qval_q_run_id)
                            qvals_g = results_g["qvals"]
                            goal_qvals.append(qvals_g)
                        start_time = time.time()
                        posteriors, time_to_ignore = compute_goal_inference_posteriors(demonstration, 
                            goals, goal_qvals, env_name, initial_state, goal)
                        time_elapsed = time.time() - start_time - time_to_ignore
                        results = {"posteriors" : posteriors, "time_elapsed" : time_elapsed}
                        save_results(gi_run_id, results)
                        if test_goal_inference:
                            run_test_goal_inference(goals, goal, posteriors)

    # Results summary
    report_results()


def main():
    run_pipeline(biased=True)
    run_pipeline(biased=False)

if __name__ == "__main__":
    main()
