import pandas as pd

Copy_of_MyFoodData = pd.ExcelFile(".\Projekt_Diety\\Copy_of_MyFoodData.xlsx")
Copy_of_MyFoodData_DF = pd.read_excel(Copy_of_MyFoodData, "SR Legacy and FNDDS")

Composition_of_Foods_Dataset = pd.ExcelFile(".\Projekt_Diety\\McCance_Widdowsons_Composition_of_Foods_Integrated_Dataset_2021..xlsx")
ToMargeDF1 = pd.read_excel(Composition_of_Foods_Dataset, "1.3 Proximates")
ToMargeDF1 = ToMargeDF1.drop([0, 1])
ToMargeDF2 = pd.read_excel(Composition_of_Foods_Dataset, "1.4 Inorganics")
ToMargeDF2 = ToMargeDF2.drop([0, 1])
ToMargeDF3 = pd.read_excel(Composition_of_Foods_Dataset, "1.5 Vitamins")
ToMargeDF3 = ToMargeDF3.drop([0, 1])
Composition_of_Foods_Dataset_DF = pd.merge(ToMargeDF1, ToMargeDF2, left_on=ToMargeDF1.columns[0], right_on=ToMargeDF2.columns[0])
Composition_of_Foods_Dataset_DF = pd.merge(Composition_of_Foods_Dataset_DF, ToMargeDF3, left_on=ToMargeDF2.columns[0], right_on=ToMargeDF3.columns[0])
print(Composition_of_Foods_Dataset_DF)

