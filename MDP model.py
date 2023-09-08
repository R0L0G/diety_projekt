import random

import pandas as pd

excel = pd.ExcelFile("C:\\Users\\Ludwiczek Kroliczek\\PycharmProjects\\Diety\\diety\\diety\\Data\\Copy_of_MyFoodData.xlsx")
dane = pd.read_excel(excel, "SR Legacy and FNDDS")
dane_testowe = dane.sample(n=30, random_state=12).reset_index(drop=True)


class Model:
    def __init__(self, data, target, learning_rate, epsilon, episodes, num_ingredients, starting_qualities=0):
        self.data = data
        self.target = target
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.episodes = episodes
        self.num_ingredients = num_ingredients
        self.starting_qualities = starting_qualities

    def get_available_data(self, data, picks):
        return data[~data.isin(picks)].dropna()

    def get_highest_value(self, df, column_name):
        return df.filter([df[column_name].idxmax()], axis=0)

    def get_reward(self, calories):
        if self.target - calories <= 0:
            return -1
        else:
            return 1

    def get_update(self, data, prev_episode, reward):
        return data[f"V_{prev_episode}"] + self.learning_rate * (reward - data[f"V_{prev_episode}"])

    def train(self):
        data = self.data.copy()
        data["V_0"] = self.starting_qualities
        for episode in range(1, self.episodes + 1):
            picks = pd.DataFrame()
            if episode > 1:
                for ingredient in range(self.num_ingredients):
                    avails = self.get_available_data(data, picks)
                    if random.random() < self.epsilon:
                        picks = picks.append(avails.sample(1))
                    else:
                        picks = picks.append(self.get_highest_value(avails, f"V_{episode - 1}"))

            else:
                picks = picks.append(data.sample(self.num_ingredients))

            calories = picks.Calories.sum()
            reward = self.get_reward(calories)
            data[f"V_{episode}"] = data[f"V_{episode - 1}"].where(
                cond=~data.index.isin(picks.index),
                other=self.get_update(data, episode - 1, reward)
            )
            data = data.copy()
        return data

