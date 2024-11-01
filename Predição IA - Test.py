import pandas as pd

df = pd.read_excel('plastic-pollution (1).xlsx')

dfAmerica = df[df['Entity'] == 'Americas (excl. USA)']
#years = dfAmerica['Year']

print(dfAmerica)

print("Americas (excl. USA): ")
years = [2010,2019]
mismanaged_str = list(dfAmerica["Mismanaged(T)"])

mismanaged_transform = [int(value.replace(",", "")) for value in mismanaged_str]

mismanaged = [value for year, value in zip(years,mismanaged_transform)]

for year, value in zip(years,mismanaged):
    print(f"Ano {year}: {value:,.0f} t")

delta_mismanaged = mismanaged[-1] - mismanaged[0]
delta_years = years[-1] - years[0]
a = delta_mismanaged / delta_years

b = mismanaged[0] - a * years[0]

future_years = list(range(2020, 2050))
predictions = [a * year + b for year in future_years]

for year, prediction in zip(future_years, predictions):
    print(f"Ano {year}: Previsão de plástico = {prediction:,.0f} t")
    #print(prediction)

years_list = []
mismanaged_list =  []
for index,row in dfAmerica.iterrows():
    year = row['Year']
    mismanaged = row['Mismanaged(T)']
    years_list.append(year)
    mismanaged_list.append(mismanaged)

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
            "content": "You are a system that predict quantity of waste of plastic for future years based in a dictionary of years and respective Mismanaged(T). Generate a dictionary of future years and the respective prediction.Write in that form '{'year': 2020, 'mismanaged(T)': 5,591,629 t}'.Explain to me how you arrived at this prediction.Do not put any other additional information",
        },
        {
            "role": "user",
            "content": f"years: {years_list}, Quantity: {mismanaged_list} ",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)    
