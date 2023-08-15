import streamlit as st
import datetime
import os
import pandas as pd
from dateutil.relativedelta import relativedelta

from Analise_Flex.pegaThunders import infoContratosThunders
from Functions.graficoFlex import geraGraficoFlex

def applyDatetime(month,year):
    x = pd.to_datetime(f'{month}{year}',format='%m%Y')

    return x

hoje = datetime.date.today()

atualMes = datetime.date(hoje.year, hoje.month, 1)

proximoMes = atualMes + relativedelta(months=1)

primeiro_d = (atualMes, proximoMes)

d = st.date_input(
    "Selecione o mês desejado",
    (atualMes, proximoMes),
    datetime.date(2018,1,1),
    atualMes + relativedelta(years=10),
    format="DD.MM.YYYY",
)

# st.write(d)

if os.path.isfile('temp/tmpTxt/tmpControle.txt'):
    with open('temp/tmpTxt/tmpControle.txt') as f:
        line = f.readline()
    if line != str(d):
        df = infoContratosThunders(d)
        # st.write('Mudou a data')
    else:
        df = pd.read_csv('temp/tmpCsv/tmpDF.csv')
        # st.write('Não mudou a data')
else:
    df = infoContratosThunders(d)
    # st.write('Arquivo não existia')


option = st.selectbox(
    'Selecione o tipo de energia',
    (pd.unique(df['energySourceDescription'])))

df = df[(df['energySourceDescription']==option) & (df['hasFlexibility']==True)]

option = st.selectbox(
    'Selecione a ContraParte',
    (pd.unique(df['counterpartyName'].sort_values())))

df = df[df['counterpartyName']==option]

option = st.selectbox(
    'Selecione o Submercado',
    (pd.unique(df['submarketDescription'].sort_values())))

df = df[df['submarketDescription']==option]


df['maxFlexVolumeMwm'] = df['contractedVolumeMwm']*(100+df['flexibilityPercentageTop'])/100
df['minFlexVolumeMwm'] = df['contractedVolumeMwm']*(100-df['flexibilityPercentageBottom'])/100
df['maxFlexVolumeMwh'] = df['contractedVolumeMwh']*(100+df['flexibilityPercentageTop'])/100
df['minFlexVolumeMwh'] = df['contractedVolumeMwh']*(100-df['flexibilityPercentageBottom'])/100

df['mesAno'] = df.apply(lambda x: applyDatetime(x.month,x.year), axis=1)

df = df.sort_values('mesAno')

dfRealizado = df[df['billingStatus']=='Autorizado']

# st.write(df[['month','contractedVolumeMwm']])
# st.write(df[['month','maxFlexVolumeMwm']])
# st.write(df[['month','minFlexVolumeMwm']])
# st.write(dfRealizado[['month','finalVolumeMwm']])

# st.line_chart(df[['mesAno','contractedVolumeMwm']],x='mesAno',y='contractedVolumeMwm')

fig = geraGraficoFlex(df,dfRealizado)

st.pyplot(fig)

st.write(df)