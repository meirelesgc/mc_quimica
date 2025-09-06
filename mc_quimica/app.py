import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import linregress


def reset_points():
    st.session_state.points = []


if "points" not in st.session_state:
    st.session_state.points = []

st.set_page_config(page_title="Curva de Calibração e Recuperação", layout="centered")
st.title("Curva de Calibração e Teste de Recuperação")
step = st.sidebar.radio(
    "Etapas",
    (
        "1. Inserir Pontos (Calibração)",
        "2. Ajuste e Resultados",
        "3. Teste de Recuperação (Padrão)",
        "4. Exportar/Reset",
    ),
)

if step == "1. Inserir Pontos (Calibração)":
    st.header("Etapa 1 — Inserir Pontos")
    st.write(
        "Prático: nesta etapa o usuário insere pares (X, Y). O código armazena esses pontos na sessão e os utiliza para plotar o gráfico e para o ajuste linear na etapa seguinte."
    )
    col1, col2 = st.columns(2)
    with col1:
        x_input = st.number_input(
            "Valor de X (Concentração)", format="%.2f", key="cal_x"
        )
    with col2:
        y_input = st.number_input("Valor de Y (Sinal)", format="%.2f", key="cal_y")
    if st.button("Adicionar Ponto"):
        st.session_state.points.append((float(x_input), float(y_input)))
        st.success(f"Ponto ({x_input:.2f}, {y_input:.2f}) adicionado")
    if st.session_state.points:
        df = pd.DataFrame(st.session_state.points, columns=["X", "Y"])
        st.dataframe(df)
        if st.button("Limpar Pontos"):
            reset_points()
            st.experimental_rerun()
    else:
        st.info("Adicione pelo menos dois pontos para prosseguir para o ajuste")

elif step == "2. Ajuste e Resultados":
    st.header("Etapa 2 — Ajuste da Curva de Calibração")
    st.write(
        "Prático: nesta etapa o código usa os pontos inseridos para calcular a regressão linear (inclinação e intercepto), plotar a reta ajustada sobre os pontos e fornecer métricas do ajuste."
    )
    if len(st.session_state.points) < 2:
        st.warning("Adicione pelo menos dois pontos na Etapa 1")
    else:
        points = np.array(st.session_state.points)
        x_vals = points[:, 0]
        y_vals = points[:, 1]
        slope, intercept, r_value, p_value, std_err = linregress(x_vals, y_vals)
        r_squared = r_value**2
        fig, ax = plt.subplots()
        ax.scatter(x_vals, y_vals, label="Pontos")
        line_x = np.linspace(0, max(x_vals) * 1.1, 100)
        line_y = slope * line_x + intercept
        ax.plot(line_x, line_y, label="Ajuste", color="red")
        ax.set_xlabel("Concentração (X)")
        ax.set_ylabel("Sinal (Y)")
        ax.set_title("Curva de Calibração")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
        st.subheader("Parâmetros do Ajuste")
        st.latex(rf"y = {slope:.2f}x + {intercept:.2f}")
        st.latex(rf"R^2 = {r_squared:.2f}")
        st.write(f"Erro padrão da inclinação: {std_err:.6e}")
        if slope == 0:
            st.error(
                "Inclinação igual a zero. Não é possível converter sinais em concentrações."
            )
        download_df = pd.DataFrame({"X": x_vals, "Y": y_vals})
        csv = download_df.to_csv(index=False)
        st.download_button(
            "Baixar pontos (CSV)", csv, "calibration_points.csv", "text/csv"
        )

elif step == "3. Teste de Recuperação (Padrão)":
    st.header("Etapa 3 — Teste de Recuperação")
    st.write(
        "Prático: o usuário fornece o sinal da amostra sem Padrão e com Padrão e a concentração do Padrão. O código converte esses sinais em concentrações usando a equação da reta ajustada e calcula a recuperação percentual."
    )
    if len(st.session_state.points) < 2:
        st.warning("Adicione pontos na Etapa 1 e faça o ajuste na Etapa 2")
    else:
        points = np.array(st.session_state.points)
        x_vals = points[:, 0]
        y_vals = points[:, 1]
        slope, intercept, r_value, p_value, std_err = linregress(x_vals, y_vals)
        if slope == 0:
            st.error("Inclinação da curva é zero. Ajuste inválido.")
        else:
            with st.expander("Teoria"):
                st.latex(
                    r"\frac{C_{inicial}}{C_{inicial} + C_{padrao}} = \frac{S_{inicial}}{S_{final}}"
                )
            s_inicial = st.number_input(
                "Sinal da amostra inicial (sem padrão)", format="%.2f", key="s_inicial"
            )
            s_final = st.number_input(
                "Sinal da amostra final (com padrão)", format="%.2f", key="s_final"
            )
            c_padrao = st.number_input(
                "Concentração do padrão adicionado (C_Padrão)",
                format="%.2f",
                key="c_padrao",
            )
            if st.button("Calcular Recuperação"):
                if c_padrao <= 0:
                    st.error("C_Padrão deve ser maior que zero")
                else:
                    c_inicial = (s_inicial - intercept) / slope
                    c_final = (s_final - intercept) / slope
                    recuperacao = ((c_final - c_inicial) / c_padrao) * 100
                    st.metric("Recuperação (%)", f"{recuperacao:.2f}")
                    st.write(f"Concentração calculada inicial: {c_inicial:.2f}")
                    st.write(f"Concentração calculada com Padrão: {c_final:.2f}")
                    if 80 <= recuperacao <= 120:
                        st.success("Recuperação dentro da faixa aceitável (80–120%)")
                    elif 70 <= recuperacao < 80 or 120 < recuperacao <= 130:
                        st.warning(
                            "Recuperação um pouco fora da faixa ideal; investigar possíveis interferências"
                        )
                    else:
                        st.error(
                            "Recuperação fora da faixa aceitável; possível interferência da matriz ou erro experimental"
                        )

elif step == "4. Exportar/Reset":
    st.header("Etapa 4 — Exportar e Reset")
    st.write(
        "Prático: permite baixar os pontos inseridos em CSV ou apagar todos os pontos da sessão para iniciar um novo experimento."
    )
    if st.session_state.points:
        df = pd.DataFrame(st.session_state.points, columns=["X", "Y"])
        csv = df.to_csv(index=False)
        st.download_button(
            "Baixar pontos (CSV)", csv, "calibration_points.csv", "text/csv"
        )
        if st.button("Limpar tudo"):
            reset_points()
            st.experimental_rerun()
    else:
        st.info("Nenhum ponto salvo")
