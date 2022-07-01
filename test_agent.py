import gym
import numpy as np
from stable_baselines.common.policies import MlpPolicy, CnnPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2, A2C
import random


class TestEnv(gym.Env):
    def __init__(self):
        super().__init__()

        self.observation_space = gym.spaces.Discrete(50)

        self.action_space = gym.spaces.Discrete(2)
        self.state = np.array([0])

        self.rounds = 50

        self.future_state_delta = 0
        self.future_state_delta_2 = 0

    def step(self, action):
        old_state = self.state[0]

        self.state += self.future_state_delta_2
        if self.state[0] < 0:
            self.state[0] = 0
        elif self.state[0] > 50:
            self.state[0] = 50

        self.future_state_delta_2 = self.future_state_delta
        self.future_state_delta = 0

        done = False

        self.rounds -= 1

        if action == 1:
            self.future_state_delta += 10

        else:
            self.future_state_delta -= random.randint(3, 4)


        if 0 < self.state[0] <= 25:
            reward = 1 - self.state[0]/25
        else:
            reward = -5

        if self.rounds == 0:
            done = True

        info = {"old_state: ": self.state[0], "action: ": action, "reward: ": round(reward, 2), "rounds left: ": self.rounds}

        return self.state[0], reward, done, info

    def reset(self):
        self.state = np.array([random.randint(0, 15)])
        self.rounds = 50
        return self.state[0]


env = TestEnv()

"""
action_space_size = env.action_space.n
state_space_size = env.observation_space.n
q_table = np.zeros((state_space_size, action_space_size))
print(q_table)
"""

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(50000)

done = False
state = env.reset()
while not done:
    # action = env.action_space.sample()
    action, _states = model.predict(state)
    state, reward, done, info = env.step(action)
    print(info)