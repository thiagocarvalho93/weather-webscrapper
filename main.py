import pandas as pd
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import scraper

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

print(df)

# Enviar dados via API
# TODO
