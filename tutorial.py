import random
from collections import defaultdict

import numpy as np
import pandas as pd

DATA_PATH = "C:\\Users\\pawel\\Downloads\\Copy of MyFoodData.xlsx"


class MonteCarloTreeSearchNode():
    def __init__(self, state, target, all_actions, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self.target = target
        self.all_actions = all_actions
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        self._untried_actions = self.get_legal_actions()
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.move(action[1])
        child_node = MonteCarloTreeSearchNode(
            next_state, target=self.target, all_actions=self.all_actions, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.is_game_over(self.state)

    def rollout(self):
        current_rollout_state = self

        while not current_rollout_state.is_game_over(current_rollout_state.state):
            possible_moves = current_rollout_state.get_legal_actions()

            action = self.rollout_policy(possible_moves)
            current_rollout_state.state = current_rollout_state.move(action[1])
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        for state in self.get_legal_actions():
            if not self.is_game_over(state[1]):
                return False
        return True

    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):

        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)

    def get_legal_actions(self):
        '''
        Modify according to your game or
        needs. Constructs a list of all
        possible states from current state.
        Returns a list.
        '''
        df = self.all_actions
        df_values = df[
            [
                "Calories",
                "Fat (g)",
                "Protein (g)",
                "Carbohydrate (g)"
            ]
        ].to_numpy().tolist()
        names = df["Name"].tolist()
        legal_actions = []
        for name, nutritions in zip(names, df_values):
            legal_actions.append((name, self.state + nutritions))
        random.shuffle(legal_actions)
        return legal_actions

    def is_game_over(self, state):
        '''
        Modify according to your game or
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        '''
        if all(state > 0.95 * self.target) or not self._untried_actions:
            return True
        else:
            return False

    def game_result(self):
        '''
        Modify according to your game or
        needs. Returns 1 or 0 or -1 depending
        on your state corresponding to win,
        tie or a loss.
        '''
        if all(self.state > 0.95 * self.target) and all(self.state < 1.05 * self.target):
            return 1
        else:
            return -1

    def move(self, action):
        '''
        Modify according to your game or
        needs. Changes the state of your
        board with a new value. For a normal
        Tic Tac Toe game, it can be a 3 by 3
        array with all the elements of array
        being 0 initially. 0 means the board
        position is empty. If you place x in
        row 2 column 3, then it would be some
        thing like board[2][3] = 1, where 1
        represents that x is placed. Returns
        the new state after making a move.
        '''
        return action


excel = pd.ExcelFile(DATA_PATH)
data = pd.read_excel(excel, "SR Legacy and FNDDS")[
    [
        "Name",
        "Calories",
        "Fat (g)",
        "Protein (g)",
        "Carbohydrate (g)"
    ]
]
test_data = data.sample(n=1000, random_state=12).reset_index(drop=True)

state = np.array([0.0, 0.0, 0.0, 0.0])
root = MonteCarloTreeSearchNode(
    state,
    np.array([1700.0, 100.0, 100.0, 100.0]),
    test_data
)
while not root.is_game_over(state):
    selected_node = root.best_action()
    print(selected_node.parent_action[0], selected_node.parent_action[1]-state)
    state = selected_node.parent_action[1]
    print("state ", state)
    root = MonteCarloTreeSearchNode(
        state,
        np.array([1700.0, 100.0, 100.0, 100.0]),
        test_data
    )
print("target: ", 0.95*np.array([1700.0, 100.0, 100.0, 100.0]), 1.05*np.array([1700.0, 100.0, 100.0, 100.0]))