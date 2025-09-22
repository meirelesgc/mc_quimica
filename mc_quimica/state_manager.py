import streamlit as st


def initialize_session_state():
    if "points" not in st.session_state:
        st.session_state.points = []
    if "slope" not in st.session_state:
        st.session_state.slope = None
    if "intercept" not in st.session_state:
        st.session_state.intercept = None
    if "recovery_points" not in st.session_state:
        st.session_state.recovery_points = []


def reset_all_states():
    st.session_state.points = []
    st.session_state.slope = None
    st.session_state.intercept = None
    st.session_state.recovery_points = []
    st.success("Todos os dados foram limpos!")
