from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests

link_base = 'https://www.wunderground.com/dashboard/pws/'


def to_dataframe(estacao, date):
    url = link_base + estacao + '/table/' + date + '/' + date + '/daily'
    # Cria uma variável contendo o conteúdo da página
    page = requests.get(url)
    # Interpreta os dados com o BeautifulSoup
    soup = BeautifulSoup(page.text, 'html.parser')

    # Procura a tabela correta no html
    table = soup.find('table', class_='history-table desktop-table')
    # Usa o Pandas pra ler a tabela html
    df = pd.read_html(str(table))[0]
    df = df.dropna(how='all')

    # Tira as strings das unidades para converter para numérico
    df2 = df.replace({'°F': ''}, regex=True)
    df2 = df2.replace({'°%': ''}, regex=True)
    df2 = df2.replace({'°mph': ''}, regex=True)
    df2 = df2.replace({'°in': ''}, regex=True)
    df2 = df2.replace({'w/m²': ''}, regex=True)
    cols = df2.columns.drop(['Time', 'Wind', 'UV'])  # Colunas numéricas
    # Tira os espaços em branco
    for col in cols:
        df2[col] = df2[col].str.strip()
    # Converte para numérico
    df2[cols] = df2[cols].apply(pd.to_numeric)

    # Farenheit para Celsius
    def f(x): return (x - 32) * 5/9
    df2[['Temperature',	'Dew Point']] = df2[[
        'Temperature', 'Dew Point']].applymap(f).round(1)
    # mph para km/h:
    def g(x): return x * 1.60934
    df2[['Speed', 'Gust']] = df2[['Speed', 'Gust']].applymap(g).round(1)
    # Identifica a estação na tabela
    df2['Station'] = estacao

    # Converte o horário para o formato ISO8601
    date = datetime.strptime(date, "%Y-%m-%d")
    x = pd.to_datetime(df2['Time']).apply(lambda dt: dt.replace(
        day=date.day, month=date.month, year=date.year))
    df2['ISO8601'] = x.dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Preenche os valores NaN com 0
    # (p/ evitar erro na hora de exportar para o sheets)
    df2 = df2.fillna(0)

    return df2
