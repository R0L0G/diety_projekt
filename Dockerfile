FROM python:3.11-slim
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py", "-my", "Data/Copy_of_MyFoodData.xlsx", "-mc", "Data/McCance_Widdowsons_Composition_of_Foods_Integrated_Dataset_2021..xlsx"]
