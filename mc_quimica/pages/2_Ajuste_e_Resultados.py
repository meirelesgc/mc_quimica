import sys

import streamlit as st

sys.path.append("..")
import calculations as calc
import state_manager as sm

sm.initialize_session_state()

st.header("Etapa 2 — Ajuste da Curva e Resultados")

if len(st.session_state.points) < 2:
    st.warning(
        "Adicione pelo menos dois pontos na página 'Inserir Pontos' para continuar."
    )
else:
    regression_results = calc.perform_linear_regression(st.session_state.points)

    if regression_results:
        st.session_state.slope = regression_results["slope"]
        st.session_state.intercept = regression_results["intercept"]

        st.subheader("Gráfico da Curva de Calibração")
        fig = calc.generate_calibration_plot(
            regression_results["x_vals"],
            regression_results["y_vals"],
            st.session_state.slope,
            st.session_state.intercept,
        )
        st.pyplot(fig)

        st.subheader("Parâmetros do Ajuste Linear")
        st.latex(
            rf"y = {st.session_state.slope:.4f}x + {st.session_state.intercept:.4f}"
        )
        st.latex(rf"R^2 = {regression_results['r_squared']:.4f}")
        st.write(f"Erro Padrão da Inclinação: {regression_results['std_err']:.6e}")
