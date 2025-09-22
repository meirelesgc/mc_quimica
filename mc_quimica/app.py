import state_manager as sm
import streamlit as st

st.set_page_config(page_title="Página Principal", page_icon="🏠", layout="centered")

sm.initialize_session_state()

st.title("📊 Curva de Calibração e Teste de Recuperação")
st.markdown("---")
st.header("Bem-vindo!")
st.write(
    "Este aplicativo foi projetado para auxiliar em análises químicas, "
    "permitindo a construção de uma curva de calibração, o cálculo de regressão linear "
    "e a realização de testes de recuperação de padrão."
)
st.info("👈 **Navegue pelas etapas usando o menu na barra lateral** para começar.")

st.subheader("Como usar:")
st.markdown(
    """
    1.  **Inserir Pontos**: Vá para a primeira página para adicionar os pontos da sua curva de calibração (Concentração vs. Sinal).
    2.  **Ajuste e Resultados**: A segunda página irá gerar o gráfico, calcular a equação da reta e o R².
    3.  **Teste de Recuperação**: Na terceira página, insira os dados da sua amostra e padrão para calcular a porcentagem de recuperação.
    4.  **Exportar e Resetar**: A última página permite baixar os dados da calibração e limpar a memória do aplicativo para recomeçar.
    """
)
