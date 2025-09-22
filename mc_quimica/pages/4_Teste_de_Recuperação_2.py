import pandas as pd
import streamlit as st


def initialize_session_state():
    if "slope" not in st.session_state:
        st.session_state.slope = None
    if "intercept" not in st.session_state:
        st.session_state.intercept = None
    if "recovery_points" not in st.session_state:
        st.session_state.recovery_points = []


initialize_session_state()


def calcular_recuperacao_padrao(slope, intercept, s_inicial, recovery_points):
    results_data = []

    if slope == 0:
        st.error("O 'slope' da curva de calibração não pode ser zero.")
        return []

    c_inicial = (s_inicial - intercept) / slope

    for point in recovery_points:
        c_padrao = point["c_padrao"]
        s_final = point["s_final"]

        c_final_medida = (s_final - intercept) / slope

        c_recuperado = c_final_medida - c_inicial

        if c_padrao > 0:
            recuperacao_percentual = (c_recuperado / c_padrao) * 100
        else:
            recuperacao_percentual = 0.0  # Evita divisão por zero

        results_data.append(
            {
                "C. Padrão Adicionado": c_padrao,
                "Sinal Final": s_final,
                "C. Recuperado": c_recuperado,
                "Recuperação (%)": recuperacao_percentual,
            }
        )
    return results_data


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

        # AQUI ESTÁ A MUDANÇA PRINCIPAL: usando a nova função
        results_data = calcular_recuperacao_padrao(
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
