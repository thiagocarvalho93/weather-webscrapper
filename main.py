import pandas as pd
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import scraper
import requests

# Definindo a data de ontem
# Fuso horário
timezone_offset = -3.0
tzinfo = timezone(timedelta(hours=timezone_offset))
# Ontem no formato usado no link:
ontem = (datetime.now(tzinfo) - relativedelta(days=1)).strftime("%Y-%m-%d")

df = pd.DataFrame()

# Definindo as estações
stations = ['IMACA7', 'IMACA13', 'ICAMPO96', 'IMACA15', 'IRIODA1', 'IRJSANTA2']
# Definindo a data
date = ontem

# Aplicando as funções e coletando os dados
for station in stations:
    print(station)
    df_temp = scraper.to_dataframe(station, date)
    df = df.append(df_temp)

# Preparando o Request Body
df = df.astype(str)
df.rename(columns={'ISO8601': 'timeStamp', 'Station': 'station', 'Temperature': 'temperature','Dew Point': 'dewPoint',
                'Humidity': 'humidity','Wind': 'windDirection','Speed': 'windSpeed',
                'Gust': 'gust','Pressure': 'pressure','Precip. Rate.': 'precipitationRate',
                'Precip. Accum.': 'precipitationAcc','UV': 'uv','Solar': 'solarIrradiation'},inplace=True)

list_dict = []
for index, row in list(df.iterrows()):
    list_dict.append(dict(row))

body = { 'data': list_dict }



# Enviar dados via API
# TODO
api_url = "http://localhost:5000/data/"

# Limpa os dados anteriores
response = requests.delete(api_url)

# Adiciona os dados atualizados
if(response.status_code == 204):
    response = requests.post(api_url, json=body)
    print(response.status_code)

