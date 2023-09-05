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


class Model:
    def __init__(self, dane):
        self.dane = self.add_qualities(dane)

    def add_qualities(self, dane):
        dane["Qualites"] = 0
        return dane

    def modelv1(dane, target, epsilon, learning_rate):
        pass




