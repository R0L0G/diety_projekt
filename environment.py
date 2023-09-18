import numpy as np
import gymnasium as gym

from gymnasium import spaces


class DietyWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, actions, render_mode=None):
        self.obervation_space = spaces.Dict(
            {
                "agent": spaces.Box([0, 0, 0, 0], [5000, 500, 500, 250], dtype=np.float32),
                "target": spaces.Box([0, 0, 0, 0], [5000, 500, 500, 250], dtype=np.float32),
            }
        )

        self.action_space = spaces.Discrete(100)

        self._action_to_direction = {
            i: actions.iloc[i][""].to_numpy for i in actions.index
        }

    def _get_obs(self):
        return {"agent": self._agent_location, "target": self._target_location}

    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=2
            )
        }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self._agent_location = np.array([0, 0, 0, 0])
        self._target_location = np.array([1700, 100, 100, 100])

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        direction = self._action_to_direction[action]

        self._agent_location += direction
        terminated = all(self._agent_location >= 0.9*self._target_location)
        too_much = any(self._agent_location >= 1.1*self._target_location)
        if terminated and not too_much:
            reward = 1
        elif too_much:
            reward = -1
        else:
            reward = 0
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info


