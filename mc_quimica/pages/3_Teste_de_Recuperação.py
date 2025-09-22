import sys

import pandas as pd
import streamlit as st

sys.path.append("..")
import calculations as calc
import state_manager as sm

sm.initialize_session_state()

st.header("Etapa 3 — Teste de Recuperação")

if st.session_state.slope is None or st.session_state.intercept is None:
    st.warning(
        "A curva de calibração ainda não foi gerada. Vá para a página 'Ajuste e Resultados' primeiro."
    )
else:
    st.info(
        f"Usando a curva: y = {st.session_state.slope:.4f}x + {st.session_state.intercept:.4f}"
    )

    s_inicial = st.number_input(
        "Sinal da amostra inicial (sem padrão)", format="%.4f", key="s_inicial"
    )
    st.markdown("---")

    st.subheader("Adicionar Pontos de Recuperação")
    st.write("Insira a concentração de padrão adicionada e o sinal final medido.")

    col1, col2 = st.columns(2)
    with col1:
        c_padrao_input = st.number_input(
            "Concentração do padrão adicionado", format="%.2f", min_value=0.0
        )
    with col2:
        s_final_input = st.number_input("Sinal da amostra com padrão", format="%.4f")

    if st.button("Adicionar Ponto de Recuperação"):
        if c_padrao_input > 0:
            st.session_state.recovery_points.append(
                {"c_padrao": c_padrao_input, "s_final": s_final_input}
            )
            st.success("Ponto de recuperação adicionado!")
        else:
            st.error("A concentração do padrão deve ser maior que zero.")

    if st.session_state.recovery_points:
        st.markdown("---")
        st.subheader("Resultados do Teste de Recuperação")

        results_data = calc.calculate_recovery(
            st.session_state.slope,
            st.session_state.intercept,
            s_inicial,
            st.session_state.recovery_points,
        )

        if results_data:
            results_df = pd.DataFrame(results_data)
            st.dataframe(
                results_df.style.format(
                    {
                        "C. Padrão Adicionado": "{:.2f}",
                        "Sinal Final": "{:.4f}",
                        "C. Recuperado": "{:.4f}",
                        "Recuperação (%)": "{:.2f}%",
                    }
                )
            )

        if st.button("Limpar Pontos de Recuperação"):
            st.session_state.recovery_points = []
            st.rerun()
