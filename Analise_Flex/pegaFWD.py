from Integracao_Dados_Thunder.Functions.ConexaoBancoDados import conexao_banco_Dados

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

def pegaFWD(Data_Fwd):
    conn = conexao_banco_Dados()
    today = datetime.today().date() - relativedelta(days=1)

    ultimoDia = calendar.monthrange(Data_Fwd.year,Data_Fwd.month)[1]

    data = f'{Data_Fwd.year}-{Data_Fwd.month}-{ultimoDia}'
    data = pd.to_datetime(data,format='%Y-%m-%d').date()

    if today < data:
        data=today

    sql = f"SELECT * FROM Book.Curva.VW_Curva_Fwd WHERE Data = '{data}' and Curva = 'Oficial'"
    df = pd.read_sql(sql,conn)

    return df