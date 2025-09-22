import sys

import pandas as pd
import streamlit as st

sys.path.append("..")
import state_manager as sm

sm.initialize_session_state()

st.header("Etapa 5 — Exportar Resultados de Recuperação")

st.subheader("Exportar Dados de Recuperação")
if st.session_state.amostra:
    df = pd.DataFrame(st.session_state.amostra)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar dados de recuperação (CSV)",
        data=csv,
        file_name="dados_recuperacao.csv",
        mime="text/csv",
    )
else:
    st.info("Não há dados de recuperação para exportar.")

st.markdown("---")

st.subheader("Resetar Apenas Recuperação")
st.warning("A ação abaixo limpará somente os dados da etapa de recuperação.")
if st.button("Limpar Recuperação"):
    st.session_state.amostra = []
    st.success("Dados de recuperação limpos com sucesso!")
