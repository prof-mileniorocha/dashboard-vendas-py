import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Carrega dados
df = pd.read_csv("dados/dados_vendas_simulados.csv")

st.title("📊 Dashboard de Vendas e Acessos por Horário")

st.markdown("""
### 🕵️‍♂️ O Detetive de Dados

A loja notou uma queda de **30% nas vendas entre 18h e 22h**.  
Seu trabalho é investigar **o que está acontecendo** com base nos dados abaixo.
""")

# Filtros
col1, col2 = st.columns(2)
with col1:
    regiao = st.selectbox("Filtrar por região", options=["Todas"] + sorted(df["region"].dropna().unique()))
with col2:
    hora = st.select_slider("Filtrar por horário", options=sorted(df["hour"].unique()))

# Aplica filtros
df_filtrado = df.copy()
if regiao != "Todas":
    df_filtrado = df_filtrado[df_filtrado["region"] == regiao]
df_filtrado = df_filtrado[df_filtrado["hour"] == hora]

# Exibe filtros aplicados
st.markdown(f"### 🔍 Filtros aplicados: Região = `{regiao}` | Hora = `{hora}`")

# Métricas rápidas
colm1, colm2, colm3 = st.columns(3)
colm1.metric("Total de Vendas", int(df_filtrado["purchases"].sum()))
colm2.metric("Total de Acessos", int(df_filtrado["access_count"].sum()))
colm3.metric("Erros 500", int(df_filtrado["errors_500"].sum()))

# Gráficos (mostrando dados filtrados para foco no horário/região)
st.subheader(f"📈 Métricas detalhadas para o horário: {hora}")
col3, col4, col5 = st.columns(3)

with col3:
    fig_vendas = px.bar(
        df_filtrado, x="hour", y="purchases", title="Vendas por Horário",
        color_discrete_sequence=["#00cc96"]
    )
    st.plotly_chart(fig_vendas, use_container_width=True)

with col4:
    fig_acessos = px.line(
        df_filtrado, x="hour", y="access_count", title="Acessos por Horário",
        markers=True
    )
    st.plotly_chart(fig_acessos, use_container_width=True)

with col5:
    fig_erros = px.area(
        df_filtrado, x="hour", y="errors_500", title="Erros 500 por Horário",
        color_discrete_sequence=["#ef553b"]
    )
    st.plotly_chart(fig_erros, use_container_width=True)

# Tabela de reclamações — só se existir a coluna complaints
if "complaints" in df.columns:
    st.subheader("📬 Reclamações por Horário (simuladas)")
    reclamacoes = df_filtrado[df_filtrado["complaints"] > 0][["hour", "complaints"]]
    if not reclamacoes.empty:
        st.dataframe(reclamacoes, use_container_width=True)
    else:
        st.info("Nenhuma reclamação registrada para o filtro aplicado.")
else:
    st.warning("Coluna 'complaints' não encontrada nos dados.")

# Texto sobre campanhas
st.subheader("📢 Campanhas de Marketing Ativas")
st.info("⚠️ Nenhuma campanha ativa durante o período da noite.")

# Informações de manutenção
st.subheader("🛠️ Manutenção Técnica")
st.warning("ℹ️ Manutenção programada detectada às 23h - possível causa de erros.")

# Espaço para interação do usuário (feedback, hipóteses)
st.subheader("📝 Sua hipótese")
hipotese = st.text_area("O que você acha que está impactando as vendas?")

if hipotese:
    st.success("Obrigado por compartilhar sua hipótese! Detetives atentos fazem toda a diferença. 🔍")

