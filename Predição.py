import pandas as pd
import requests

df = pd.read_excel('plastic-waste-generation-2000-2019.xlsx')

def make_prediction(dfCont): 
    print(f"**** Entidade: {dfCont.copy()['Entity'].iloc[0]} ****") 
    years = list(dfCont['Year']) 
    total_waste_str = list(dfCont["Total waste"])

    total_waste = [value for year, value in zip(years, total_waste_str)]
    
    data_2000_2019 = []
    for year, value in zip(years, total_waste ):
        print(f"Ano {year}: {value:,.0f}")
        data = {
            'entity': dfCont['Entity'].iloc[0],
            'year': year,
            'quantity': value,
            'population': 0
        }
        data_2000_2019.append(data)


    delta_total_waste = total_waste[-1] - total_waste[0]
    delta_years = years[-1] - years[0]
    a = delta_total_waste / delta_years

    b = total_waste[0] - a * years[0]

    future_years = list(range(2020, 2051))
    predictions = [(year, a * year + b) for year in future_years]

    items = []
    for year, prediction in predictions:
        print(f"Ano {year}: Previsão de plástico = {prediction:,.0f} t")
        item = {
            'entity': dfCont['Entity'].iloc[0],
            'year': year,
            'quantity': prediction,
            'population': 0
        }
        items.append(item)


    return items,data_2000_2019

def send_to_db(items, data_2000_2019):
    url = "http://moon:4000"
    route_pred = "/waste-prediction"
    route_2000_2019 = "/waste-data-2000-2019"

    for item in data_2000_2019:
        try:
            response = requests.post(url + route_2000_2019, json=item)
            response.raise_for_status()
            print(f"Envio bem sucedido na rota {route_2000_2019}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar dados para o banco: {e}")

    for item in items:
        try:
            response = requests.post(url + route_pred, json=item)
            response.raise_for_status()
            print(f"Envio bem sucedido na rota {route_pred}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar dados para o banco: {e}")


dfAmericas = df[df['Entity'] == 'Americas']
dfAsia = df[df['Entity'] == 'Asia']
dfEurope = df[df['Entity'] == 'Europe']
dfMiddleEast_NorthAfrica = df[df['Entity'] == 'Middle East & North Africa']
dfOceania = df[df['Entity'] == 'Oceania']
dfSubSaharanAfrica = df[df['Entity'] == 'Sub-Saharan Africa']
dfWorld = df[df['Entity'] == 'World']

df_list = [dfAmericas, dfAsia, dfEurope, dfMiddleEast_NorthAfrica, dfOceania, dfSubSaharanAfrica, dfWorld]

for dataframe in df_list:
    predictions, hist_data = make_prediction(dataframe)
    send_to_db(predictions,hist_data)

