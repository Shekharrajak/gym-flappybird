import gym
import gym_flappybird
env = gym.make('flappybird-v0')
import time

# env.reset()

# time.sleep(5)
import random

ACTIONS = [0 ,1]
# time.sleep(5)
for i in range(100):
    a = random.choice(ACTIONS)
    # print(a)
    obs, rewards, done, info = env.step(a)
    print(obs, ' - ', rewards , ' - ', done , ' - ', info)
    # env.render()


