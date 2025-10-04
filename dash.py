import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("googleplaystore.csv")
st.set_page_config(layout="wide")

#FILTRAR POR
    #Categoria   
    #Tipo de App (pago ou free)
    #Rating
    
#COM BASE NO NOSSO OBJETIVO, POSSÍVEIS ANÁLISES
    #APPS com maior quantidade de downloads
    #Apps com crescimento acelerado porém com poucos concorrentes?
    #Apps com maior rating
    #Dsitribuição de Apps por categoria (Gráfico de Barras)
    #Categorias por numero de instalações (Gráfico de barras horizontais)
    #apps por número de downloads (Grafico de Ranking)
    #Media de Rating por categoria (Para ver em quais segmentos os usuários estão mais satisfeitos)
    #Relação entre número de reviews e rating (Scatter plot com reviews no eixo X e rating no eixo Y para ajudar a identificar apps populares e bem avaliados
    #Comparação dos apps free com os pagos (Gráfico de Pizza)
    #Distribuição do tamanho dos apps vs downloads (Scatter plot para mostrar se apps mais leves tendem a ter mais usuários)


#Remove as linhas da coluna type que forem diferentes de Free ou Paid
df = df[df["Type"].isin(["Free", "Paid"])] 

# ========================================================================================================================
# Criando os filtros
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

# Mostrar resultado final
df_filtered
