import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Carrega dados
df = pd.read_csv("dados/dados_vendas_simulados.csv")

# Renomear colunas para português
df = df.rename(columns={
    "purchases": "vendas",
    "access_count": "acessos",
    "errors_500": "erros_500",
    "complaints": "reclamacoes",
    "hour": "hora",
    "region": "regiao"
})

st.title("📊 Dashboard de Vendas e Acessos por Horário")

# Filtros
col1, col2 = st.columns(2)
with col1:
    regiao = st.selectbox("Filtrar por região", options=["Todas"] + sorted(df["regiao"].dropna().unique()))
with col2:
    hora = st.select_slider("Filtrar por horário (opcional)", options=["Todos"] + sorted(df["hora"].unique()), value="Todos")

# Aplica filtro de região
if regiao != "Todas":
    df = df[df["regiao"] == regiao]

# Aplica filtro de hora apenas se selecionado diferente de "Todos"
if hora != "Todos":
    df_filtrado = df[df["hora"] == hora]
else:
    df_filtrado = df

# Gráficos
st.subheader(f"📈 Métricas para o horário: {hora if hora != 'Todos' else 'Todos os horários'}")
col3, col4, col5 = st.columns(3)

with col3:
    fig_vendas = px.bar(
        df_filtrado, x="hora", y="vendas",
        title="Vendas por Horário",
        color_discrete_sequence=["#00cc96"]
    )
    st.plotly_chart(fig_vendas, use_container_width=True)

with col4:
    fig_acessos = px.line(
        df_filtrado, x="hora", y="acessos",
        title="Acessos por Horário", markers=True
    )
    st.plotly_chart(fig_acessos, use_container_width=True)

with col5:
    fig_erros = px.area(
        df_filtrado, x="hora", y="erros_500",
        title="Erros 500 por Horário",
        color_discrete_sequence=["#ef553b"]
    )
    st.plotly_chart(fig_erros, use_container_width=True)

# Tabela de reclamações
st.subheader("📬 Reclamações por Horário (simuladas)")
reclamacoes = df_filtrado[df_filtrado["reclamacoes"] > 0][["hora", "reclamacoes"]]
st.dataframe(reclamacoes, use_container_width=True)

# Texto sobre campanhas
st.subheader("📢 Campanhas de Marketing Ativas")
st.info("⚠️ Nenhuma campanha ativa durante o período da noite.")

# Informações de manutenção
st.subheader("🛠️ Manutenção Técnica")
st.warning("ℹ️ Manutenção programada detectada às 23h - possível causa de erros.")