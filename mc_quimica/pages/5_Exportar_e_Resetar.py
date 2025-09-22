import sys

import pandas as pd
import streamlit as st

sys.path.append("..")
import state_manager as sm

sm.initialize_session_state()

st.header("Etapa 4 — Exportar Dados e Resetar")

st.subheader("Exportar Pontos de Calibração")
if st.session_state.points:
    df = pd.DataFrame(st.session_state.points, columns=["X_Concentracao", "Y_Sinal"])
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar pontos (CSV)",
        data=csv,
        file_name="pontos_calibracao.csv",
        mime="text/csv",
    )
else:
    st.info("Não há pontos de calibração para exportar.")

st.markdown("---")

st.subheader("Resetar Aplicação")
st.warning(
    "Atenção: A ação abaixo limpará todos os dados inseridos (calibração e recuperação)."
)
if st.button("Limpar Tudo e Recomeçar"):
    sm.reset_all_states()
