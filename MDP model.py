from random import randint,seed

import pandas as pd



excel = pd.ExcelFile("C:\\Users\\Ludwiczek Kroliczek\\PycharmProjects\\Diety\\diety\\diety\\Data\\Copy_of_MyFoodData.xlsx")
dane = pd.read_excel(excel, "SR Legacy and FNDDS")
list_of_columns = [dane["Name"], dane["Calories"]]
dane_testowe = dane[["Name", "Calories"]]
seed(12)
random_list = []
for i in range(0, 30):
    random_list.append(randint(0, 14165))
food_df = dane_testowe.take(random_list)
food_df = food_df.reset_index(drop=True)
print(food_df)
seed()


class Model:
    def __init__(self, dane, target, learning_rate, epsilon):
        self.dane = self.add_qualities(dane)
        self.target = target
        self.learning_rate = learning_rate
        self.epsilon = epsilon

    def add_qualities(self, dane):
        dane["Qualites"] = 0.5
        return dane

    def modelv1(self, dane, target, epsilon):
        list_of_products = []
        e = randint(1, 101)
        while len(list_of_products) < 4:
            list_of_random = []
            for i in range(0, 3):
                list_of_random.append(randint(0, 29))
            list_of_qualites = [dane["Qualites"][i] for i in list_of_random]
            if list_of_qualites[0] == list_of_qualites[1] == list_of_qualites[2] == list_of_qualites[3]:
                index = randint(0, 3)
                list_of_products.append(list_of_random[index])
            elif epsilon > e:
                index = randint(0,3)
                list_of_products.append(list_of_random[index])
            else:
                index = list_of_qualites.index(max(list_of_qualites))
                list_of_products.append(list_of_random[index])
        sum = 0
        for i in list_of_products:
            sum += dane["Calories"][i]
        diff = target - sum
        return diff, list_of_products

    def reward(self, diff):
        if diff <= 0:
            return -1
        else:
            return 1
    def update(self, dane,reward,learning_rate, list_of_products):
        for i in list_of_products:
            dane["Qualites"][i] = dane["Qualites"][i] + learning_rate*(reward - dane["Qualites"][i])









