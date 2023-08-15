import xlwings as xw
import pandas as pd
import calendar

from Integracao_Dados_Thunder.infoContratos import infoContratosThunders
from Analise_portifolio.Analise_Flex.pegaFWD import pegaFWD
from Analise_portifolio.Analise_Flex.pegaPLD import pegaPLD


def analiseFlex(wb):

    Data_Fwd = pd.to_datetime('2023-06-01',format='%Y-%m-%d')
    numDias = calendar.monthrange(Data_Fwd.year,Data_Fwd.month)[1]
    numHoras = numDias*24

    df = infoContratosThunders(wb)

    df = df[
        (df['billingStatus']=='Autorizado') &
        (df['hasFlexibility']==True) &
        (df['year']==2023) &
        (df['month']==6) &
        (df['operationType']=='Venda')
    ]

    df_fwd = pegaFWD(Data_Fwd)
    r = pegaPLD(Data_Fwd)

    tiposEnergias = pd.unique(df['energySourceDescription'])

    for fonte in tiposEnergias:
        subsistemas = pd.unique(df[df['energySourceDescription']==fonte]['submarketDescription'])
        for sub in subsistemas:
            curva=df_fwd[df_fwd['Fonte_Energia']==fonte.replace('Cogeração Qualificada 50%','CQ5').replace('Incentivada 50%','50% Incent.').replace('Incentivada 100%','100% Incent.').replace('Incentivada 0%','0% Incent.')]
            curva = curva[(curva['Submercado']==sub.replace('Sudeste','SE').replace('Sul','S').replace('Nordeste','NE').replace('Norte','N')) & (curva['Data_Fwd']==Data_Fwd.date())]
            dfAux = df[(df['submarketDescription']==sub) & (df['energySourceDescription']==fonte)]
            for index,row in dfAux.iterrows():
                volContratado = row['contractedVolumeMwm']
                volFinal = row['finalVolumeMwm']
                precoContrato = row['basePrice']
                precoReajustado = row['price']
                flexTeto = row['flexibilityPercentageTop']/100
                flexPiso = row['flexibilityPercentageBottom']/100

                difVol = ((volContratado-volFinal)/volContratado)

                if difVol > 0 :
                    if difVol>flexTeto:
                        flex = flexTeto
                    else:
                        flex = difVol

                    vende = (flex*volContratado)*numHoras*curva['Preco_Energia'].values[0]
                    compra = (flex*volContratado)*numHoras*precoReajustado
                    resultado = vende - compra

                elif difVol < 0 :
                    if difVol<flexPiso:
                        flex = flexPiso
                    else:
                        flex = difVol

                    vende = (flex*volContratado)*numHoras*precoReajustado
                    compra = (flex*volContratado)*numHoras*curva['Preco_Energia'].values[0]

                    resultado = vende - compra
                dict = { 
                    'Codigo':row['code'],
                    'Submercado':sub,
                    'Fonte':fonte,
                    'Volume Contratado':volContratado,
                    'Volume Final':volFinal,
                    'Preço Contrato':precoContrato,
                    'Preço Reajustado':precoReajustado,
                    'Flex Teto':flexTeto,
                    'Flex Piso':flexPiso,
                    'Preço FWD':curva['Preco_Energia'].values[0],
                    'Vendeu':vende,
                    'Comprou':compra,
                    'resultado':resultado
                }
                    

    print('Acabou analiseFlex')


    
