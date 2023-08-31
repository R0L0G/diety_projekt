import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Possible Arguments!!!", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-my", "--MyFoodData")
parser.add_argument("-mc", "--McCanceDataSet")
args = vars(parser.parse_args())
print("Działa?")

Copy_of_MyFoodData = pd.ExcelFile(args["MyFoodData"])
Copy_of_MyFoodData_DF = pd.read_excel(Copy_of_MyFoodData, "SR Legacy and FNDDS")

Composition_of_Foods_Dataset = pd.ExcelFile(args["McCanceDataSet"])
ToMargeDF1 = pd.read_excel(Composition_of_Foods_Dataset, "1.3 Proximates")
ToMargeDF1 = ToMargeDF1.drop([0, 1])
ToMargeDF2 = pd.read_excel(Composition_of_Foods_Dataset, "1.4 Inorganics")
ToMargeDF2 = ToMargeDF2.drop([0, 1])
ToMargeDF3 = pd.read_excel(Composition_of_Foods_Dataset, "1.5 Vitamins")
ToMargeDF3 = ToMargeDF3.drop([0, 1])
Composition_of_Foods_Dataset_DF = pd.merge(ToMargeDF1, ToMargeDF2, left_on=ToMargeDF1.columns[0], right_on=ToMargeDF2.columns[0])
Composition_of_Foods_Dataset_DF = pd.merge(Composition_of_Foods_Dataset_DF, ToMargeDF3, left_on=ToMargeDF2.columns[0], right_on=ToMargeDF3.columns[0])
print(Composition_of_Foods_Dataset_DF)

