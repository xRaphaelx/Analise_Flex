import datetime
import streamlit as st
from dateutil.relativedelta import relativedelta

from Functions.pegaPLD import pegaPLD


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

pld = pegaPLD(('2019-01-01T00:00:00'))

st.write(pld)