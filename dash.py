import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("googleplaystore.csv")
st.set_page_config(layout="wide")

st.title("Análise dos Aplicativos da Google Play Store")
st.markdown("---")

# =========================================== LIMPEZA DOS DADOS ======================================================================
#Remove as linhas da coluna type que forem diferentes de Free ou Paid
df = df[df["Type"].isin(["Free", "Paid"])] 


df["Installs"] = df["Installs"].str.replace(",", "", regex=False)   #Ele ta trocando onde tem , por vazio
df["Installs"] = df["Installs"].str.replace("+", "", regex=False).astype(int)   #Tirando o "+" das linhas e convertendo para inteiro

df["Category"] = df["Category"].str.replace("_", " ", regex=False)

df["Genres"] = df["Genres"].str.replace(";", " - ", regex=False)

df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")  #erros = "coerce" transforma valores inválidos em NaT (data nula, que pode ser removida depois).
#Criando uma nova coluna chamada AnoMes
df["AnoMes"] = df["Last Updated"].dt.to_period("M").astype(str)


df["Price"] = df["Price"].str.replace("$", "", regex=False).astype(float)


#PENSAR EM ALGUMA FORMA DE TRATAR A COLUNA SIZE (DE FORMA QUE SE EU TIVER 10G e 100K, quando eu tirar essas letras, ele continue interpretando o 10G como o maior)


# =========================================== FILTROS ======================================================================
st.sidebar.header("Filtros")

# Filtro por categoria
categorys = ["Todos"] + list(df["Category"].unique())
category = st.sidebar.selectbox("Categoria", categorys)

if category != "Todos":
    df_filtered = df[df["Category"] == category]
else:
    df_filtered = df


# Filtro por Método de Pagamento
payment_methods = ["Todos"] + list(df["Type"].unique())
payment_method = st.sidebar.selectbox("Tipo de Pagamento (Free/Paid)", payment_methods)

if payment_method != "Todos":
    df_filtered = df_filtered[df_filtered["Type"] == payment_method]


# Filtro de Rating
rating_apps = st.sidebar.slider("Rating", min_value=0.0, max_value=5.0, value=(0.0, 5.0), step=0.5)
#Separa a tupla que criamos em duas varoáveos de valor max e min
rating_min, rating_max = rating_apps
#Seleciona todas as linhas onde o rating é maior ou igual ao mínimo e onde o rating é menor ou igual ao máximo
df_filtered = df_filtered[(df_filtered["Rating"] >= rating_min) & (df_filtered["Rating"] <= rating_max)]

# ===================================================================================================================
# =========================================== GRÁFICOS ======================================================================

#----------------------- Entendendo o mercado --------------
st.header("Entendendo o mercado")

#Criando as colunas
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)


#Distribuição por tipo (Free vs Paid)
tipo_pagamento = px.pie(df_filtered, title="Distribuição por tipo (Free vs Paid)", names="Type")
col1.plotly_chart(tipo_pagamento)

#Quatidade de apps por categoria
category_counts = df_filtered.groupby("Category")["App"].count().reset_index().sort_values("App", ascending=True) #Pega a quantidade de App por categoria, ordenando da maior quantidade para o menor 
category_quantity = px.bar(category_counts, x="App", y="Category", orientation="h", title="Quantidade de Apps por categoria", labels={"App": "Quantidade", "Category": "Categoria"}) #Labels está mudando o valor do eixo x e y do gráfico
col2.plotly_chart(category_quantity)


#MEDIA DE RATING POR CATEGORIA
rating_filter = df_filtered.groupby("Category")["Rating"].mean().reset_index()
rating_category = px.box(rating_filter, y="Rating", x="Category", title="Dsitribuição de rating por categoria", labels={"Rating": "Média de Rating", "Category": "Categoria"})
col3.plotly_chart(rating_category)


#Relação entre Reviws e Rating
relation_reviewsAndRating = px.scatter(df_filtered, x="Rating", y="Reviews")
col4.plotly_chart(relation_reviewsAndRating)

st.markdown("---")

#--------------- POPULARIDADE DOS APPS ------------
st.header("Popularidade dos APPs")
col5,col6, col7 = st.columns(3)


#QUANTIDADE DE DOWNLOAD por APP (Top20)
top_apps = df_filtered.groupby("App")["Installs"].sum().sort_values(ascending=False).head(20)
downloadquantity = px.bar(top_apps, x=top_apps.index, y=top_apps.values, orientation= "v", title="Top20 Apps mais baixados", labels={"x": "App", "y": "Número de downloads"})
col5.plotly_chart(downloadquantity)


#CATEGORIA POR NUMERO DE Downloads (top10)
top_categorys = df_filtered.groupby("Category")["Installs"].sum().sort_values(ascending=True).head(10)
category_downloads = px.bar(top_categorys, x=top_categorys.values, y=top_categorys.index, title="Downloads por categoria", labels={"x": "Número de Downloads", "y": "Categoria"})
col6.plotly_chart(category_downloads)


#RELAÇÃO ENTRE O SIZE E QUANTIDADE DE DOWNLOADS --> saber se apss mais leves tem mais downloads



#--------------- Análise Financeira (Somente Apps pagos) ------------
st.markdown("---")
st.subheader("Análise Financeira (Apps Pagos)")
apps_pagos = df_filtered[df_filtered["Type"] == "Paid"]

col8, col9, col10 = st.columns(3)

#PREÇO MEDIO POR CATEGORIA
precomedioporcateg = apps_pagos.groupby("Category")["Price"].mean().sort_values(ascending=False).head(20)
precoporcateg = px.bar(precomedioporcateg, x=precomedioporcateg.values, y=precomedioporcateg.index, title="Preço medio por categoria", labels={"x": "Preço médio", "y": "Categoria"})
col8.plotly_chart(precoporcateg)

#Relação entre preço e rating


#Receita potencial

#-------------- Oportunidades e Tendências ---------------
st.markdown("---")
st.subheader("Oportunidades e Tendências")
col11, col12, col13 = st.columns(3)

#Atualizações mais recentes
apps_por_mes = df_filtered.groupby("AnoMes")["App"].count().reset_index().sort_values("AnoMes")

apps_por_mes.rename(columns={"App": "Quantidade de Apps"}, inplace=True)

apps_por_mes["AnoMes"] = pd.to_datetime(apps_por_mes["AnoMes"])
apps_por_mes = apps_por_mes.sort_values("AnoMes")

atualizacoes = px.bar(
    apps_por_mes,
    x="AnoMes",
    y="Quantidade de Apps",
    title="Atualizações de Apps ao Longo do Tempo",
    labels={"AnoMes": "Ano/Mês", "Quantidade de Apps": "Quantidade de Atualizações"},
)
col11.plotly_chart(atualizacoes)

#Relação entre frequência de atualização e rating

#Quais faixas etárias são mais utilizadas?








st.markdown("---")
st.subheader("Dados Filtrados")
st.dataframe(df_filtered)


