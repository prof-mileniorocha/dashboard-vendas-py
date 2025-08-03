import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Carrega dados
df = pd.read_csv("dados/dados_vendas_simulados.csv")

st.title("📊 Dashboard de Vendas e Acessos por Horário")

# Filtros
col1, col2 = st.columns(2)
with col1:
    regiao = st.selectbox("Filtrar por região", options=["Todas"] + sorted(df["region"].dropna().unique()))
with col2:
    hora = st.select_slider("Filtrar por horário", options=sorted(df["hour"].unique()))

if regiao != "Todas":
    df = df[df["region"] == regiao]
df_filtrado = df[df["hour"] == hora]

# Gráficos
st.subheader(f"📈 Métricas para o horário: {hora}")
col3, col4, col5 = st.columns(3)

with col3:
    fig_vendas = px.bar(df, x="hour", y="purchases", title="Vendas por Horário", color_discrete_sequence=["#00cc96"])
    st.plotly_chart(fig_vendas, use_container_width=True)

with col4:
    fig_acessos = px.line(df, x="hour", y="access_count", title="Acessos por Horário", markers=True)
    st.plotly_chart(fig_acessos, use_container_width=True)

with col5:
    fig_erros = px.area(df, x="hour", y="errors_500", title="Erros 500 por Horário", color_discrete_sequence=["#ef553b"])
    st.plotly_chart(fig_erros, use_container_width=True)

# Tabela de reclamações
st.subheader("📬 Reclamações por Horário (simuladas)")
reclamacoes = df[df["complaints"] > 0][["hour", "complaints"]]
st.dataframe(reclamacoes, use_container_width=True)

# Texto sobre campanhas
st.subheader("📢 Campanhas de Marketing Ativas")
st.info("⚠️ Nenhuma campanha ativa durante o período da noite.")

# Informações de manutenção
st.subheader("🛠️ Manutenção Técnica")
st.warning("ℹ️ Manutenção programada detectada às 23h - possível causa de erros.")

