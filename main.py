import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import createclient 

url = "https://iqeqnsobhcknizaowius.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlxZXFuc29iaGNrbml6YW93aXVzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MjM3NDMsImV4cCI6MjA4NzI5OTc0M30.lq5a232elsZyMxg6qT-LXX_2WTsF790RN0X8S8ulTvY"

supabase = create_client(url, key)

st.dataframe(lista_nomes_alunos)

st.title("Sistema de Avaliação - v2")

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
