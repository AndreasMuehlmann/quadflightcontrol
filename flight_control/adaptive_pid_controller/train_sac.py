import os
import pygame
import numpy as np
from sac import Agent
from utils import init_changing_plot, draw_plot, plot_learning_curve
from vel_env import VelEnv
from pos_env import PosEnv

if __name__ == '__main__':
    env = PosEnv()
    agent = Agent(env)
    episodes = 500 

    range_avg = 5
    filename = 'learning_curve.png'
    print(os.getcwd())
    figure_file = f'{os.path.dirname(os.path.abspath(__file__))}\\plots\\' + filename

    best_score = env.reward_range[0]
    score_history = []
    avg_score_history = []

    load_checkpoint = False
    save_model = True
    learn = True

    if load_checkpoint:
        agent.load_models()
        env.render(mode='human')
    else:
        init_changing_plot()

    for episode in range(episodes):
        observation = env.reset()
        done = False
        score = 0
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.remember(observation, action, reward, observation_, done)
            env.render()
            if (episode > range_avg or not load_checkpoint) and learn: 
                agent.learn()
            observation = observation_
        score_history.append(score)
        avg_score = np.mean(score_history[-range_avg:])

        avg_score_history.append(avg_score)
        if avg_score > best_score:
            best_score = avg_score
            if (episode > range_avg or not load_checkpoint) and learn and save_model:
                agent.save_models()
                
        draw_plot(episode, avg_score_history)
        print('episode ', episode, 'score %.1f' % score, 'avg_score %.1f' % avg_score)

    if learn and save_model:
        x = [i+1 for i in range(episodes)]
        plot_learning_curve(x, score_history, figure_file)

    pygame.quit()
    input('Press Enter to close')