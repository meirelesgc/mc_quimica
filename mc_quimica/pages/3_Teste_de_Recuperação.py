import pandas as pd
import streamlit as st


def initialize_session_state():
    if "slope" not in st.session_state:
        st.session_state.slope = None
    if "intercept" not in st.session_state:
        st.session_state.intercept = None
    if "recovery_points" not in st.session_state:
        st.session_state.recovery_points = []
    if "amostra" not in st.session_state:
        st.session_state.amostra = []


initialize_session_state()

st.header("Etapa 3 — Teste de Recuperação")

if st.session_state.slope is None or st.session_state.intercept is None:
    st.warning(
        "A curva de calibração ainda não foi gerada. Vá para a página 'Ajuste e Resultados' primeiro."
    )
else:
    st.info(
        f"Usando a curva: y = {st.session_state.slope:.4f}x + {st.session_state.intercept:.4f}"
    )
    st.write(
        "Insira os pares de dados para calcular a quantidade de analito recuperado e a porcentagem de recuperação"
    )

    col1, col2 = st.columns(2)
    with col1:
        analito = st.number_input(
            "Quantidade do analito adicionado", format="%.4f", key="cal_x"
        )
    with col2:
        amostra = st.number_input("Sinal da amostra", format="%.4f", key="cal_y")

    if st.button("Adicionar"):
        qtd_analito_recuperado = (
            amostra - st.session_state.intercept
        ) / st.session_state.slope
        recuperacao = (100 * qtd_analito_recuperado) / analito
        st.session_state.amostra.append(
            {
                "Quantidade do analito adicionado": float(analito),
                "Sinal da amostra": float(amostra),
                "Analito recuperado (calculado)": float(qtd_analito_recuperado),
                "Recuperação (%)": float(recuperacao),
            }
        )
        st.success(f"Valores adicionados com sucesso! ({analito:.4f}, {amostra:.4f})")

        st.latex(
            rf"""
            x = \frac{{y - b}}{{a}} = \frac{{{amostra:.4f} - {st.session_state.intercept:.4f}}}{{{st.session_state.slope:.4f}}} = {qtd_analito_recuperado:.4f}
            """
        )
        st.latex(
            rf"""
            R = \frac{{x}}{{\text{{Adicionado}}}} \times 100 = \frac{{{qtd_analito_recuperado:.4f}}}{{{analito:.4f}}} \times 100 = {recuperacao:.2f}\%
            """
        )

    if st.button("Limpar tabela"):
        st.session_state.amostra = []
        st.success("Tabela limpa com sucesso!")

    if st.session_state.amostra:
        df = pd.DataFrame(st.session_state.amostra)
        st.dataframe(df)
