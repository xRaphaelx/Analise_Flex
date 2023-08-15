from Functions.ConexaoBancoDados import conexao_banco_Dados

import pandas as pd

def infoContratosThunders(d):


    dataInicio = d[0]
    dataFim = d[1]

    conn = conexao_banco_Dados()

    with open('temp/tmpTxt/tmpControle.txt', 'w') as f:
        f.write(str(d))

    query = f"SELECT * FROM [Book].[dbo].[operation] where startDate <= '{dataInicio.strftime('%Y-%m-%dT00:00:00')}' and endDate >= '{dataFim.strftime('%Y-%m-%dT00:00:00')}'"
    df_adm = pd.read_sql(query,conn)

    query = f"SELECT * FROM [BookComercial].[dbo].[operation] where startDate <= '{dataInicio.strftime('%Y-%m-%dT00:00:00')}' and endDate >= '{dataFim.strftime('%Y-%m-%dT00:00:00')}'"
    df_varejo = pd.read_sql(query,conn)

    df = pd.concat([df_adm,df_varejo])

    # ws = wb.sheets('Thunders-InfosContratos')
    # ws.range("A1").clear_contents()
    # ws.range('A1').options(header=True, chunksize=10_000).value = df
    df.to_csv('temp/tmpCsv/tmpDF.csv',index=False)
    return df

    print()