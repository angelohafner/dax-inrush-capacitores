
"""
Angelo Alfredo Hafner
aah@dax.energy
"""
from engineering_notation import EngNumber
import numpy as np
import pandas as pd
import streamlit as st
import pandas as pd
import openpyxl
from io import BytesIO
import streamlit as st


st.markdown('# Resposta transitória da energização de capacitores DAX-Energy')
col1, col2 = st.columns([3, 1])

with col1:
    st.image(image='Sistema.png', width=500)
    uploaded_file = st.file_uploader("Choose the file")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file                        , usecols=[1,2,3,4,5,6,7,8,9], header=1)
    else:
        df = pd.read_excel('Dados_do_sistema_e_capacitores.xlsx', usecols=[1,2,3,4,5,6,7,8,9], header=1)

    with open('Dados_do_sistema_e_capacitores.xlsx', "rb") as file:
        st.download_button(label='📥 Download do Modelo de Arquivo',
                        data=file,
                        file_name= 'Dados_do_sistema_e_capacitores_MODELO.xlsx')

    df = pd.read_excel('Dados_do_sistema_e_capacitores.xlsx', usecols=[1,2,3,4,5,6,7,8,9], header=1)
    df = df.fillna(0)

    Q_3f            = df.iloc[:, 1].values * 1e3
    comp_cabo       = df.iloc[:, 2].values
    comp_barra      = df.iloc[:, 3].values
    L_unit_cabo     = df.iloc[:, 4].values * 1e-6
    L_unit_barra    = df.iloc[:, 5].values * 1e-6
    L_reator        = df.iloc[:, 6].values * 1e-6
    L_capacitor     = df.iloc[:, 7].values * 1e-6

    nr_bancos = df.shape[0] - 2
    L_barra_mais_cabo = comp_barra * L_unit_barra + comp_cabo * L_unit_cabo
    L = L_barra_mais_cabo + L_capacitor + L_reator
    
with col2:
    FC = st.slider("Fator de Segurança", min_value=1.0,  max_value=1.4, value=1.4, step=0.1)
    V_ff = st.slider("Tensão [kV]", min_value=13.8,  max_value=380.0, value=23.1, step=0.1)
    V_ff = 1e3 * V_ff
    V_fn = V_ff / np.sqrt(3)
    f_fund = st.slider("Frequência [Hz]", min_value=50.0,  max_value=60.0, value=60.0, step=0.1)
    w_fund = 2*np.pi*f_fund
    R_eq = st.slider("Resistência [mΩ]", min_value=0,  max_value=2000, value=200, step=1) * 1e-3
    
  
Q_1f = Q_3f / 3
I_fn = np.zeros(nr_bancos, dtype=float)
I_fn =  Q_1f / V_fn
X = V_fn / I_fn
C = 1 / ( w_fund * X )
C_paralelos = np.sum(C[1:])
den_C = 1/C[0] + 1/C_paralelos
C_eq = 1/den_C

L[L==0] = np.inf
L_paralelos =  1 / np.sum( 1 / L[1:] )
L_eq = L[0] + L_paralelos


raiz = -(R_eq/L_eq)**2 +  4/(C_eq*L_eq)
omega = np.sqrt(raiz) / 2
num_i = V_fn * np.sqrt(2)
den_i = L_eq * omega
i_pico_inical =  FC * num_i / den_i
sigma = R_eq/(2*L_eq)

t = np.linspace(0, 5/sigma, 2**14 )
i_curto = i_pico_inical * np.exp(-sigma*t) * np.sin(omega*t)

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=t*1e3,
    y=i_curto/1e3,
    name="Instantânea",
    line = dict(shape = 'linear', color = 'rgb(0, 0, 255)', width = 1)
))

fig.add_trace(go.Scatter(
    x=t*1e3,
    y=i_pico_inical * np.exp(-sigma*t)/1e3,
    name="Envelope",
    line = dict(shape = 'linear', color = 'rgb(0, 0, 0)', width = 1, dash = 'dot'),
    connectgaps = True)
)

fig.add_trace(go.Scatter(
    x=t*1e3,
    y=-i_pico_inical * np.exp(-sigma*t)/1e3,
    name="Envelope",
    line = dict(shape = 'linear', color = 'rgb(0, 0, 0)', width = 1, dash = 'dot'),
    connectgaps = True)
)

fig.update_layout(legend_title_text='Corrente:', title_text="Inrush Banco de Capacitores",
                  xaxis_title=r"Tempo [ms]", yaxis_title="Corrente [kA]")
st.plotly_chart(fig)

st.write("Corrente de pico considerada = ", EngNumber(i_pico_inical), "A")
st.write("Corrente de pico real = ",        EngNumber(np.max(i_curto)), "A")
st.write("Ireal/Iconsiderado =",            np.round(np.max(i_curto)/i_pico_inical, 2))
st.write("Frequência de Oscilação = ",      EngNumber(omega/(2*np.pi)), "Hz")
st.write("Harmônico de Oscilação = ",       EngNumber(omega/w_fund))


st.markdown('## Formulário')
st.latex(r"I\left( s \right) = \frac{{\frac{{\sqrt 2 {V_{fn}}}}{s}}}{{R + sL + \frac{1}{{sC}}}}")
st.latex(r"i\left( t \right) = \frac{{\sqrt 2 {V_{fn}}}}{{L\sqrt {\frac{1}{{LC}} - \frac{{{R^2}}}{{4{L^2}}}} }}\,\,\exp \left( { - \frac{R}{{2L}}\,t} \right)\,\,\sin \left( {\sqrt {\frac{1}{{LC}} - \frac{{{R^2}}}{{4{L^2}}}} \,t} \right)")

st.markdown('## Bibliografia')
st.write("[IEEE Application Guide for Capacitance Current Switching for AC High-Voltage Circuit Breakers Rated on a Symmetrical Current Basis](https://ieeexplore.ieee.org/document/7035261)")


