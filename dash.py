import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("googleplaystore.csv")
st.set_page_config(layout="wide")



# =========================================== LIMPEZA DOS DADOS ======================================================================
#Remove as linhas da coluna type que forem diferentes de Free ou Paid
df = df[df["Type"].isin(["Free", "Paid"])] 

df["Installs"] = df["Installs"].str.replace(",", "", regex=False)   #Ele ta trocando onde tem , por vazio
df["Installs"] = df["Installs"].str.replace("+", "", regex=False).astype(int)   #Tirando o "+" das linhas e convertendo para inteiro

df["Category"] = df["Category"].str.replace("_", " ", regex=False)

df["Genres"] = df["Genres"].str.replace(";", " - ", regex=False)

df["Last Updated"] = pd.to_datetime(df["Last Updated"])
df["Last Updated"] = df["Last Updated"].dt.strftime("%d/%m/%Y")


#PENSAR EM ALGUMA FORMA DE TRATAR A COLUNA SIZE (DE FORMA QUE SE EU TIVER 10G e 100K, quando eu tirar essas letras, ele continue interpretando o 10G como o maior)

# =========================================== FILTROS ======================================================================
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
#Criando as colunas
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)



#QUANTIDADE DE DOWNLOAD por APP (Top20)
top_apps = df_filtered.groupby("App")["Installs"].sum().sort_values(ascending=False).head(20)
downloadquantity = px.bar(top_apps, x=top_apps.index, y=top_apps.values, orientation= "v", title="Top20 Apps mais baixados", labels={"x": "App", "y": "Número de downloads"})
col1.plotly_chart(downloadquantity)

#Quatidade de apps por categoria
category_counts = df_filtered.groupby("Category")["App"].count().reset_index().sort_values("App", ascending=True) #Pega a quantidade de App por categoria, ordenando da maior quantidade para o menor 
category_quantity = px.bar(category_counts, x="App", y="Category", orientation="h", title="Quantidade de Apps por categoria", labels={"App": "Quantidade", "Category": "Categoria"}) #Labels está mudando o valor do eixo x e y do gráfico
col2.plotly_chart(category_quantity)


#CATEGORIA POR NUMERO DE Downloads (top10)
top_categorys = df_filtered.groupby("Category")["Installs"].sum().sort_values(ascending=True).head(10)
category_downloads = px.bar(top_categorys, x=top_categorys.values, y=top_categorys.index, title="Downloads por categoria", labels={"x": "Número de Downloads", "y": "Categoria"})
col3.plotly_chart(category_downloads)

#MEDIA DE RATING POR CATEGORIA
rating_filter = df_filtered.groupby("Category")["Rating"].mean().reset_index()
rating_category = px.box(rating_filter, y="Rating", x="Category", title="Dsitribuição de rating por categoria", labels={"Rating": "Média de Rating", "Category": "Categoria"})
col4.plotly_chart(rating_category)

#Distribuição por tipo (Free vs Paid)
custo_app = px.pie(df_filtered, title="Distribuição por tipo (Free vs Paid)", names="Type")
col5.plotly_chart(custo_app)




# Mostrar resultado final com os filtros aplicados
df_filtered
