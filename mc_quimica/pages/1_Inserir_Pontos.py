import sys

import pandas as pd
import streamlit as st

sys.path.append("..")
import state_manager as sm

sm.initialize_session_state()

st.header("Etapa 1 — Inserir Pontos de Calibração")
st.write("Insira os pares de dados (X, Y) para construir a curva de calibração.")

col1, col2 = st.columns(2)
with col1:
    x_input = st.number_input("Valor de X (Concentração)", format="%.4f", key="cal_x")
with col2:
    y_input = st.number_input("Valor de Y (Sinal)", format="%.4f", key="cal_y")

if st.button("Adicionar Ponto"):
    st.session_state.points.append((float(x_input), float(y_input)))
    st.success(f"Ponto ({x_input:.4f}, {y_input:.4f}) adicionado com sucesso.")

st.markdown("---")

if st.session_state.points:
    st.subheader("Pontos Adicionados")
    df = pd.DataFrame(
        st.session_state.points, columns=["X (Concentração)", "Y (Sinal)"]
    )
    st.dataframe(df)

    if st.button("Limpar Pontos de Calibração"):
        st.session_state.points = []
        st.rerun()
else:
    st.info("Ainda não há pontos na curva. Adicione pelo menos dois para continuar.")
