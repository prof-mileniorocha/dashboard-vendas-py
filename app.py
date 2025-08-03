import streamlit as st
import pandas as pd
import plotly.express as px

# Carrega os dados
df = pd.read_csv("dados/dados_vendas_simulados.csv")

# Título
st.title("Dashboard de Vendas")

# Filtro por região
regioes = df['region'].dropna().unique()
regiao = st.selectbox("Filtrar por região:", options=["Todas"] + list(regioes))

if regiao != "Todas":
    df = df[df['region'] == regiao]

# Gráfico de linha: Compras, Acessos, Erros por hora
fig = px.line(df, x="hour", y=["purchases", "access_count", "errors_500"], markers=True,
              labels={"value": "Contagem", "hour": "Hora", "variable": "Métrica"},
              title="Métricas por Hora")

st.plotly_chart(fig, use_container_width=True)

# Tabela com dados filtrados
st.subheader("Dados brutos")
st.dataframe(df)
