import pandas as pd
import streamlit as st
import plotly.express as px


df = pd.read_csv("googleplaystore.csv")

#FILTRAR POR
    #Categoria
    #Tipo de App (pago ou free)
    #Preço
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


df

