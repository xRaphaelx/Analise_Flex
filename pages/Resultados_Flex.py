import streamlit as st
import datetime
import math
from PIL import Image
import os
import pandas as pd
from dateutil.relativedelta import relativedelta

from Analise_Flex.pegaThunders import infoContratosThunders
from Functions.graficoResultadoFlex import geraGraficoResultadoFlex
from Functions.pegaPLD import pegaPLD

def applyResultado(volumeContratado,volumeFinal,flexMax,flexMin,precoBase,precoReajuste,sub,pld,month,year):
    if volumeFinal <= flexMin:
        volumeFinal = flexMin
    elif volumeFinal >= flexMax:
        volumeFinal = flexMax
    
    data = pd.to_datetime(f'{month}{year}',format='%m%Y').strftime('%m%Y')
    if math.isnan(precoReajuste):
        precoReajuste = precoBase

    # st.write(data)
    # st.table(pld)
    saldo = volumeContratado - volumeFinal
    resultadoFinal = saldo*(pld[sub.replace('Sudeste','southeast').replace('Sul','south').replace('Nordeste','northeast').replace('Norte','north')].loc[int(data)] - precoReajuste)

    # # st.write(precoReajuste)
    
    # resultadoPrevisto = volumeContratado*precoBase
    # resultadoPrevistoReajuste = volumeContratado*precoReajuste
    # resultadoFinal = volumeFinal * precoReajuste

    return resultadoFinal

def applyDatetime(month,year):
    x = pd.to_datetime(f'{month}{year}',format='%m%Y')
    # st.write(x)

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

# Controle para não rodar o script desnecessariamente
# Testa se o arquivo de controle existe, se existe ele tenta abrir e verificar a data
if os.path.isfile('temp/tmpTxt/tmpPLDControle.txt'):
    with open('temp/tmpTxt/tmpPLDControle.txt') as f:
        line = f.readline()
# Se a data não for igual, significa que o script tem que rodar de novo 
    if line != str(hoje):
        pld = pegaPLD('2019-01-01T00:00:00')
        # st.write('Mudou a data')
# Se for igual, não tem que rodar e pode usar o dataframe que ja foi usado
    else:
        pld = pd.read_csv('temp/tmpCsv/tmpPLDDF.csv',index_col=0)
        # st.write('Não mudou a data')
# Se o arquivo não existir, significa que o script tem que rodar denovo e gerar o arquivo
else:
    pld = pegaPLD('2019-01-01T00:00:00')
    # st.write('Arquivo não existia')

# Controle para não rodar o script desnecessariamente
# Testa se o arquivo de controle existe, se existe ele tenta abrir e verificar a data
if os.path.isfile('temp/tmpTxt/tmpControle.txt'):
    with open('temp/tmpTxt/tmpControle.txt') as f:
        line = f.readline()
# Se a data não for igual, significa que o script tem que rodar de novo 
    if line != str(d):
        df = infoContratosThunders(d)
        df = df[(df['billingStatus']=='Autorizado') & (df['hasFlexibility']==True)]
        df['maxFlexVolumeMwm'] = df['contractedVolumeMwm']*(100+df['flexibilityPercentageTop'])/100
        df['minFlexVolumeMwm'] = df['contractedVolumeMwm']*(100-df['flexibilityPercentageBottom'])/100
        df['maxFlexVolumeMwh'] = df['contractedVolumeMwh']*(100+df['flexibilityPercentageTop'])/100
        df['minFlexVolumeMwh'] = df['contractedVolumeMwh']*(100-df['flexibilityPercentageBottom'])/100
        df['mesAno'] = df.apply(lambda x: applyDatetime(x.month,x.year), axis=1)
        # st.write(df)
        df['resultado'] = df.apply(lambda x: applyResultado(x.contractedVolumeMwh,x.finalVolumeMwh,x.maxFlexVolumeMwh,x.minFlexVolumeMwh,x.basePrice,x.basePriceWithReadjustment,x.submarketDescription,pld,x.month,x.year), axis=1)
        df.to_csv('temp/tmpCsv/tmpDFResultado.csv',index=False)
        # st.write('Mudou a data')
# Se for igual, não tem que rodar e pode usar o dataframe que ja foi usado
    else:
        df = pd.read_csv('temp/tmpCsv/tmpDFResultado.csv')
        # st.write('Não mudou a data')
# Se o arquivo não existir, significa que o script tem que rodar denovo e gerar o arquivo
else:
    df = infoContratosThunders(d)
    df = df[(df['billingStatus']=='Autorizado') & (df['hasFlexibility']==True)]
    df['maxFlexVolumeMwm'] = df['contractedVolumeMwm']*(100+df['flexibilityPercentageTop'])/100
    df['minFlexVolumeMwm'] = df['contractedVolumeMwm']*(100-df['flexibilityPercentageBottom'])/100
    df['maxFlexVolumeMwh'] = df['contractedVolumeMwh']*(100+df['flexibilityPercentageTop'])/100
    df['minFlexVolumeMwh'] = df['contractedVolumeMwh']*(100-df['flexibilityPercentageBottom'])/100
    df['mesAno'] = df.apply(lambda x: applyDatetime(x.month,x.year), axis=1)
    # st.write(df)
    df['resultado'] = df.apply(lambda x: applyResultado(x.contractedVolumeMwh,x.finalVolumeMwh,x.maxFlexVolumeMwh,x.minFlexVolumeMwh,x.basePrice,x.basePriceWithReadjustment,x.submarketDescription,pld,x.month,x.year), axis=1)
    # st.write('Arquivo não existia')
    df.to_csv('temp/tmpCsv/tmpDFResultado.csv',index=False)


# st.write(df['startDate'].min())


# st.write(pld)

st.markdown("""---""")
df_media = df.groupby('code')['resultado'].agg(['sum','count'])
df_media['media'] = df_media['sum']/df_media['count']
df_media = df_media.rename(columns={"sum": "Resultado Flex Acumulado", "count": "Nº Meses"})

# st.write(df.groupby('code')['resultado'].agg(['sum','count']).sort_values(['count','sum']).head(5))

# st.write(df[df['code']=='VI5022-22'])
# st.write(df_media.sort_values('media',ascending=False))

menorResultado = df_media.sort_values('media').head(10)
maiorResultado = df_media.sort_values('media',ascending=False).head(10)

st.write('Boletas com melhor resultado flex:')
st.write(df_media.sort_values('media',ascending=False).head(10).transpose())
optionMaior = st.selectbox(
    '.',
    (pd.unique(maiorResultado.index)),
    label_visibility="collapsed")

if os.path.isfile('temp/tmpTxt/tmpControleOptionMaior.txt'):
    with open('temp/tmpTxt/tmpControleOptionMaior.txt') as f:
        line = f.readline()
    if line != optionMaior:
        dfMaior = df[df['code']==optionMaior]
        dfMaior['mesAno'] = dfMaior.apply(lambda x: applyDatetime(x.month,x.year), axis=1)
        dfMaior.to_csv('temp/tmpCsv/tmpDFOptionMaior.csv')
        # st.write(dfMaior)
        geraGraficoResultadoFlex(dfMaior,'Maior')
    else:
        dfMaior = pd.read_csv('temp/tmpCsv/tmpDFOptionMaior.csv')
    dfMaior = df[df['code']==optionMaior]
    dfMaior['mesAno'] = dfMaior.apply(lambda x: applyDatetime(x.month,x.year), axis=1)
    dfMaior.to_csv('temp/tmpCsv/tmpDFOptionMaior.csv')
    # st.write(dfMaior)
    geraGraficoResultadoFlex(dfMaior,'Maior')

with open('temp/tmpTxt/tmpControleOptionMaior.txt', 'w') as f:
    f.write(str(optionMaior))
fig = Image.open('temp/tmpFig/OpcaoMaior.jpg')


# st.pyplot(fig)
# st.write(dfMaior)
data_container = st.container()
with data_container:
    infos, plot = st.columns(2)
    with infos:
        string= f"""
            Parte: {dfMaior['partyAlias'].values[0]}\n
            ContraParte: {dfMaior['counterpartyName'].values[0]}\n
            Tipo Energia: {dfMaior['energySourceDescription'].values[0]}\n
            Submercado: {dfMaior['submarketDescription'].values[0]}\n
            Inicio Fornecimento: {dfMaior['startDate'].values[0][:10]}\n
            Fim Fornecimento: {dfMaior['endDate'].values[0][:10]}\n
            Preço Contrato: {dfMaior['basePrice'].values[0]}\n
            Preço Reajuste: {dfMaior['basePriceWithReadjustment'].values[0]}\n
            Fator Reajuste: {dfMaior['reajustmentIndex'].values[0]}\n
            Flex Max: {dfMaior['flexibilityPercentageBottom'].values[0]}\n
            Flex Min: {dfMaior['flexibilityPercentageTop'].values[0]}
"""
        # st.table(df_media.sort_values('media',ascending=False).head(10).transpose())
        st.write(string)
    with plot:
        st.image(fig)

st.markdown("""---""")
st.write('Boletas com pior resultado flex')
st.write(df_media.sort_values('media').head(10).transpose())
optionMenor = st.selectbox(
    '.',
    (pd.unique(menorResultado.index)),
    label_visibility="collapsed")


if os.path.isfile('temp/tmpTxt/tmpControleOptionMenor.txt'):
    with open('temp/tmpTxt/tmpControleOptionMenor.txt') as f:
        line = f.readline()
    if line != optionMenor:
        dfMenor = df[df['code']==optionMenor]
        dfMenor['mesAno'] = dfMenor.apply(lambda x: applyDatetime(x.month,x.year), axis=1)
        dfMenor.to_csv('temp/tmpCsv/tmpDFOptionMenor.csv',index=False)
        # st.write(dfMenor)
        geraGraficoResultadoFlex(dfMenor,'Menor')
    else:
        dfMenor = pd.read_csv('temp/tmpCsv/tmpDFOptionMenor.csv')
else:
    dfMenor = df[df['code']==optionMenor]
    dfMenor['mesAno'] = dfMenor.apply(lambda x: applyDatetime(x.month,x.year), axis=1)
    dfMenor.to_csv('temp/tmpCsv/tmpDFOptionMenor.csv',index=False)
    # st.write(dfMenor)
    geraGraficoResultadoFlex(dfMenor,'Menor')

with open('temp/tmpTxt/tmpControleOptionMenor.txt', 'w') as f:
    f.write(str(optionMenor))
fig = Image.open('temp/tmpFig/OpcaoMenor.jpg')


# st.pyplot(fig)
data_container = st.container()
with data_container:
    infos, plot = st.columns(2)
    with infos:
        string= f"""
            Parte: {dfMenor['partyAlias'].values[0]}\n
            ContraParte: {dfMenor['counterpartyName'].values[0]}\n
            Tipo Energia: {dfMenor['energySourceDescription'].values[0]}\n
            Submercado: {dfMenor['submarketDescription'].values[0]}\n
            Inicio Fornecimento: {dfMenor['startDate'].values[0][:10]}\n
            Fim Fornecimento: {dfMenor['endDate'].values[0][:10]}\n
            Preço Contrato: {dfMenor['basePrice'].values[0]}\n
            Preço Reajuste: {dfMenor['basePriceWithReadjustment'].values[0]}\n
            Fator Reajuste: {dfMenor['reajustmentIndex'].values[0]}\n
            Flex Max: {dfMenor['flexibilityPercentageBottom'].values[0]}\n
            Flex Min: {dfMenor['flexibilityPercentageTop'].values[0]}
"""
        # st.table(df_media.sort_values('media',ascending=False).head(10).transpose())
        st.write(string)
    with plot:
        st.image(fig)