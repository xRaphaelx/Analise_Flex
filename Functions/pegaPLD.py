import requests
import pandas as pd
import json
import datetime
from dateutil.relativedelta import relativedelta


def pegaPLD(d):
    d = pd.to_datetime(d,format='%Y-%m-%dT%H:%M:%S')
    pld={}
    hoje = datetime.date.today()

    with open('temp/tmpTxt/tmpPLDControle.txt', 'w') as f:
        f.write(str(hoje))

    dataInicio = d.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    dataFim = (hoje).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    url = f'https://api-safira-on-prisma.safiraenergia.com.br/ccee-dessem-prices?start={dataInicio}&end={dataFim}'

    r = requests.get(url, verify=False)

    pldDict = json.loads(r.text)

    df_pld =  pd.DataFrame(pldDict['series'])
    df_pld['mesAno'] = pd.to_datetime(df_pld['date']).dt.strftime('%m%Y')

    df_pld = df_pld.groupby('mesAno').mean()

    df_pld.to_csv('temp/tmpCsv/tmpPLDDF.csv')

    #pld[str(dataInicio)] = pldDict['summary']['average']

    return df_pld