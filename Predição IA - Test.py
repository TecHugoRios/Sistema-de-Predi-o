import pandas as pd

df = pd.read_excel('plastic-waste-generation-2000-2019.xlsx')

def make_prediction(dfCont):
    print(f"**** Continente: {dfCont.copy()['Entity'].iloc[0]} ****")
    years = list(dfCont['Year'])
    total_waste_str = list(dfCont["Total waste"])

    total_waste = [value for year, value in zip(years,total_waste_str)]
    diff_from_past_year = [current - previous for previous,current in zip(total_waste[:-1],total_waste[1:])]
    print(diff_from_past_year)

    for year, value, diff in zip(years[1:],total_waste[1:], diff_from_past_year):
            print(f"Ano {year}: {value:,.0f} t - Diferenca ao ano anterior: {diff:,.0f} t ")

    delta_total_waste = total_waste[-1] - total_waste[0]
    delta_years = years[-1] - years[0]
    a = delta_total_waste / delta_years

    b = total_waste[0] - a * years[0]
    pred_calc = a * year + b

    future_years = list(range(2020, 2051))
    predictions = [pred_calc for year in future_years]

    for year, prediction in zip(future_years, predictions):
        print(f"Ano {year}: Previsão de plástico = {prediction:,.0f} t")
        #print(prediction)

    



dfAmericas = df[df['Entity'] == 'Americas']
dfAsia = df[df['Entity'] == 'Asia']
dfEurope = df[df['Entity'] == 'Europe']
dfMiddleEast_NorthAfrica = df[df['Entity'] == 'Middle East & North Africa']
dfOceania = df[df['Entity'] == 'Oceania']
dfSubSaharanAfrica = df[df['Entity'] == 'Sub-Saharan Africa']
dfWorld = df[df['Entity'] == 'World']

df_list = [dfAmericas,dfAsia,dfEurope,dfMiddleEast_NorthAfrica,dfOceania,dfSubSaharanAfrica,dfWorld]

for dataframe in df_list:
    make_prediction(dataframe)


'''  years_list = []
total_waste_list =  []
for index,row in dfAmericas.iterrows():
    year = row['Year']
    total_waste = row['Total waste']
    years_list.append(year)

   total_waste_list.append(total_waste)

import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv(".venv\.env")

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[

        {
            "role": "system",
            "content": "You are a system that predict quantity of waste of plastic for future years based in a dictionary of years and respective total_waste(T). Generate a dictionary of future years and the respective prediction.Write in that form '{'year': 2020, 'total_waste(T)': 5,591,629 t}'.Explain to me how you arrived at this prediction.Do not put any other additional information",
        },
        {
            "role": "user",
            "content": f"years: {years_list}, Quantity: {total_waste_list} ",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)    
'''