import streamlit as st
import pandas as pd
from datetime import datetime
from databricks import sql

def get_connection():
    conn = sql.connect(
        server_hostname = "dbc-0b3909c0-ee4a.cloud.databricks.com",
        http_path = "/sql/1.0/warehouses/1106e8b4dc31d18c",
        access_token = "dapid3f46ab4e2b08919d5620cea916003a3"
    )
    return conn

def consulta(query, conn):
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
query = "SELECT distinct nome FROM app_sistema_avaliacao.alunos"

conn = get_connection()
result_query = consulta(query, conn)

lista_nomes_alunos = pd.DataFrame(result_query, columns=["nome"])
#lista_nomes_alunos = pd.read_sql(query, conn)

st.dataframe(lista_nomes_alunos)

st.title("Sistema de Avaliação")

# Lista de nomes
nomes = lista_nomes_alunos["nome"].tolist()

#lista_nomes_alunos

if "etapa" not in st.session_state:
    st.session_state.etapa = 1

if st.session_state.etapa == 1:
    nome = st.selectbox("Selecione seu nome", nomes)
    if st.button("Avaliar"):
        st.session_state.nome = nome
        st.session_state.etapa = 2
        st.rerun()

if st.session_state.etapa == 2:
    st.subheader(f"Avaliando: {st.session_state.nome}")

    categorias = ["Didática", "Domínio do Conteúdo", "Clareza", "Organização"]
    notas = []

    for cat in categorias:
        nota = st.slider(cat, 0.5, 2.5, 0.5, 0.5)
        notas.append(nota)

    if st.button("Enviar"):
        total = sum(notas)

        if total < 2:
            st.error("Você precisa marcar pelo menos 1 estrela em cada categoria.")
        else:
            dados = pd.DataFrame({
                "nome": [st.session_state.nome],
                "didatica": [notas[0]],
                "dominio": [notas[1]],
                "clareza": [notas[2]],
                "organizacao": [notas[3]],
                "nota_total": [total],
                "data": [datetime.now()]
            })

            dados.to_csv("avaliacoes.csv", mode="a", header=False, index=False)

            st.success(f"Avaliação enviada! Nota total: {total}")
            st.session_state.etapa = 1
