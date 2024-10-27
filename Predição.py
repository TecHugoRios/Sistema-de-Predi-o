import pandas as pd

df = pd.read_excel('plastic-pollution (1).xlsx')

dfAmerica = df[df['Entity'] == 'Americas (excl. USA)']
years = dfAmerica['Year']

print("Americas (excl. USA): ")
years = [2010,2019]
mismanaged_str = list(dfAmerica["Mismanaged(T)"])

mismanaged = [int(value.replace(",", "")) for value in mismanaged_str]
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



