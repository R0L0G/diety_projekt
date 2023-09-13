from random import randint, seed, sample
from collections import defaultdict

import numpy as np

import pandas as pd


excel = pd.ExcelFile("C:\\Users\\Ludwiczek Kroliczek\\PycharmProjects\\Diety\\diety\\diety\\Data\\Copy_of_MyFoodData.xlsx")
dane = pd.read_excel(excel, "SR Legacy and FNDDS")
list_of_columns = [dane["Name"], dane["Calories"],dane["Fat (g)"], dane["Protein (g)"], dane["Carbohydrate (g)"]]
dane_testowe = dane[["Name", "Calories", "Fat (g)", "Protein (g)", "Carbohydrate (g)"]]
dane_testowe.columns = ["Name", "Calories", "Fat", "Protein", "Carbohydrate"]
seed(14)
random_list = []
for i in range(0, 30):
    random_list.append(randint(0, 14165))
food_df = dane_testowe.take(random_list)
food_df = food_df.reset_index(drop=True)
print(food_df["Calories"])
seed()

class mcts:
    def __init__(self, value,target_value,state=None, parent=None, parent_action=None):
        if state is None:
            self.state = self
        else:
            self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        self.target_value = target_value
        self.value = value
        self.list_of_index = []
        return

    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = mcts(value=self.value,target_value=np.array([1700, 100, 100, 100]), parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()


    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):

        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):

        next_move = possible_moves[np.random.randint(len(possible_moves))]
        self.list_of_index.append(next_move)
        return next_move

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
        possible actions from current state.
        Returns a list.
        '''
        products = [food_df.iloc[i, :] for i in sample(range(0, 29), 4)]
        return products
        '''Trzeba zaimplementować metodę jak w backpropagation żeby nie były wybierane produkty znajdujące się w parent_node'''

    def is_game_over(self):
        '''
        Modify according to your game or
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        '''
        if all(self.value >= self.target_value):
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
        if all(self.value <= self.target_value + self.target_value/10) and all(self.value >= self.target_value - self.target_value/10):
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
            !dodaje po każdym movie
            !is_game_over sprawdza value jeżeli jest w przedziale win koniec gry, jezeli jest za przedziałem loss koniec gry
            !game_resault sprawdza value i zwraca 1 lub -1
        '''
        self.value += action[["Calories", "Fat", "Protein", "Carbohydrate"]]
        return self


def main():
    root = mcts(value=np.array([0, 0, 0, 0]), target_value=np.array([1700, 100, 100, 100]))
    selected_node = root.best_action()
    print("działa")
    print(root.children, "tu print")
    return

if __name__ == "__main__":
    main()



