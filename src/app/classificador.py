from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st
import joblib


model = joblib.load('models/best_model.joblib')

def get_text(y_hat):
    saida = 'Pinguin com '
    if y_hat[1] > .4 and y_hat[1] < .6:
        saida = 'Com essas probabilidades, o modelo não tem certeza do sexo do pinguin.'
    elif y_hat[1] < .5:
        saida = saida + f'{y_hat[0]*100:.1f}% de probabilidade de ser fêmea.'
    else:
        saida = saida + f'{y_hat[1]*100:.1f}% de probabilidade de ser macho.'
    return saida

def predict_sex():
    X_ = pd.DataFrame(
        {
            'species': [st.session_state.species],
            'island': [st.session_state.island],
            'bill_length_mm': [st.session_state.bill_length_mm],
            'bill_depth_mm': [st.session_state.bill_depth_mm],
            'flipper_length_mm': [st.session_state.flipper_length_mm],
            'body_mass_g': [st.session_state.body_mass_g]
        }
    )
    st.session_state.y_hat = model.predict_proba(X_)[0]


def page():
    if 'y_hat' not in st.session_state:
        st.session_state['y_hat'] = [0, 0]
    st.title("Classificador de pinguins")
    st.subheader("Adicione informações do pinguin")
    col1, col2 = st.columns(2)
    species = col1.selectbox(
        'Espécie',
        ["Adelie", "Chinstrap", "Gentoo"],
        key='species',
        on_change=predict_sex
    )
    island = col2.selectbox(
        'Ilha',
        ["Torgersen", "Biscoe", "Dream"],
        key='island',
        on_change=predict_sex
    )
    col1, col2, col3, col4 = st.columns(4)
    bill_length_mm = col1.slider(
        'Largura do bico (mm)',
        min_value=.0,
        max_value=100.0,
        value=43.0,
        step=.1,
        key='bill_length_mm',
        on_change=predict_sex
    )
    bill_depth_mm = col2.slider(
        'Profundidade do bico (mm)',
        min_value=0.0,
        max_value=100.0,
        value=17.0,
        step=.1,
        key='bill_depth_mm',
        on_change=predict_sex
    )
    flipper_length_mm = col3.slider(
        'Largura da nadadeira (mm)',
        min_value=0.0,
        max_value=400.0,
        value=200.0,
        step=.1,
        key='flipper_length_mm',
        on_change=predict_sex
    )
    body_mass_g = col4.slider(
        'Massa (g)',
        min_value=0,
        max_value=10000,
        value=4000,
        key='body_mass_g',
        on_change=predict_sex
    )
    col1, col2 = st.columns([.55, .45])
    if all(st.session_state.y_hat):
        fig, ax = plt.subplots()
        fig.set_figheight(1)
        ax.barh(["Femea", "Macho"], 100*st.session_state.y_hat)
        plt.xlim([0, 100])
        # plt.title("Probabilidades")
        for i, v in enumerate(100*st.session_state.y_hat):
            if v < 10:
                ax.text(v + 3, i, f'{v:.1f}%', )
            else:
                ax.text(v-13, i, f'{v:.1f}%', {'color':'white'})
        col1.info(get_text(st.session_state.y_hat))
        col2.pyplot(fig)
    else:
        col1.info('Modifique os valores das variáveis...')
            
