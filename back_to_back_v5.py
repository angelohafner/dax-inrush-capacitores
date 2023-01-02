
"""
Angelo Alfredo Hafner
aah@dax.energy
"""
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from engineering_notation import EngNumber
st.set_page_config(layout="wide")
R_eq = 0.1



# ===================================================================================

st.markdown('# Resposta transitória da energização de capacitores DAX-Energy')
col0, col1, col2, col3 = st.columns([3, 1, 0.01, 5])

with col0:
    st.image(image='IMG_24052017_115903_0.png')


with col1:
    FC              = st.slider("Fator de Segurança",  min_value=1.0, max_value=1.5, value=1.4, step=0.1)
    nr_bancos       = st.slider("Número de Bancos",    min_value=2,   max_value=10,  value=4,   step=1)

with col1:
    V_ff        =   st.number_input("Tensão 3𝝋 [kV]", min_value=13.8,  max_value=380.0, value=23.1, step=0.1) * 1e3
    V_fn        =   V_ff / np.sqrt(3)
    f_fund      =   st.number_input("Frequência [Hz]",       min_value=50.0,  max_value=60.0,  value=60.0, step=0.1)
    w_fund      =   2 * np.pi * f_fund


with col3:
    st.image(image='Sistema.png', width=500)


# ==============================================================================================

# ===============================================================================================
Q_3f = np.zeros(nr_bancos)
comp_cabo = np.zeros(nr_bancos)
comp_barra = np.zeros(nr_bancos)
L_unit_cabo = np.zeros(nr_bancos)
L_unit_barra = np.zeros(nr_bancos)
L_capacitor = np.zeros(nr_bancos)
L_reator = np.zeros(nr_bancos)


st.markdown("### Banco a ser conectado $($#$0)$")
st.markdown("É o banco de capacitores que vai ser acionado.")
cols = st.columns(7)
ii = 0
k  = 0
k = 0
with cols[ii]:
        Q_3f[k] =  st.number_input("$Q_{3\\varphi}$[kVAr] ",
                                   min_value=100.0,  max_value=100e3, value=12000.0, step=0.0,
                                   key="Q_3f_"+str(k)) * 1e3
ii = ii + 1
with cols[ii]:
        comp_cabo[k] =  st.number_input("$\\ell_{\\rm cabo}{\\rm [m]}$",
                                        min_value=0.01,  max_value=100.0, value=20.0, step=0.01,
                                        key="comp_cabo"+str(k))
ii = ii + 1
with cols[ii]:
        comp_barra[k] =  st.number_input("$\\ell_{\\rm barra}{\\rm [m]}$",
                                        min_value=0.01,  max_value=100.0, value=20.0, step=0.01,
                                        key="comp_barra"+str(k))
ii = ii + 1
with cols[ii]:
        L_unit_cabo[k] =  st.number_input("$L'_{\\rm cabo} {\\rm \\left[{\\mu H}/{m} \\right]}$",
                                        min_value=0.01,  max_value=100.0, value=0.40, step=0.01,
                                        key="L_unit_cabo"+str(k)) * 1e-6
ii = ii + 1
with cols[ii]:
        L_unit_barra[k] =  st.number_input("$L'_{\\rm barra} {\\rm \\left[{\\mu H}/{m} \\right]}$",
                                        min_value=0.0,  max_value=100.0, value=0.33, step=0.01,
                                        key="L_unit_barra"+str(k)) * 1e-6
ii = ii + 1
with cols[ii]:
        L_capacitor[k] =  st.number_input("$L_{\\rm capacitor} {\\rm \\left[{\\mu H} \\right]}$",
                                        min_value=0.0,  max_value=100.0, value=0.50, step=0.01,
                                        key="L_capacitor"+str(k)) * 1e-6
ii = ii + 1
with cols[ii]:
        L_reator[k] =  st.number_input("$L_{\\rm reator} {\\rm \\left[{\\mu H} \\right]}$",
                                        min_value=0.0,  max_value=1000.0, value=200.0, step=1.0,
                                        key="L_reator"+str(k)) * 1e-6




st.markdown("### Demais Bancos $($#$1$ ao #$n)$")
st.markdown("Bancos que já estão energizados.")
cols = st.columns(7)
for k in range(1, nr_bancos):

    ii = 0
    with cols[ii]:
        Q_3f[k] = st.number_input("$Q_{3\\varphi}$[kVAr] ",
                                  min_value=100.0, max_value=100e3, value=12000.0, step=0.0,
                                  key="Q_3f_" + str(k)) * 1e3
    ii = ii + 1
    with cols[ii]:
        comp_cabo[k] = st.number_input("$\\ell_{\\rm cabo}{\\rm [m]}$",
                                       min_value=0.01, max_value=100.0, value=20.0, step=0.01,
                                       key="comp_cabo" + str(k))
    ii = ii + 1
    with cols[ii]:
        comp_barra[k] = st.number_input("$\\ell_{\\rm barra}{\\rm [m]}$",
                                        min_value=0.0, max_value=100.0, value=20.0, step=0.01,
                                        key="comp_barra" + str(k))
    ii = ii + 1
    with cols[ii]:
        L_unit_cabo[k] = st.number_input("$L'_{\\rm cabo} {\\rm \\left[{\\mu H}/{m} \\right]}$",
                                         min_value=0.0, max_value=100.0, value=0.40, step=0.01,
                                         key="L_unit_cabo" + str(k)) * 1e-6
    ii = ii + 1
    with cols[ii]:
        L_unit_barra[k] = st.number_input("$L'_{\\rm barra} {\\rm \\left[{\\mu H}/{m} \\right]}$",
                                          min_value=0.0, max_value=100.0, value=0.33, step=0.01,
                                          key="L_unit_barra" + str(k)) * 1e-6
    ii = ii + 1
    with cols[ii]:
        L_capacitor[k] = st.number_input("$L_{\\rm capacitor} {\\rm \\left[{\\mu H} \\right]}$",
                                         min_value=0.0, max_value=100.0, value=0.50, step=0.01,
                                         key="L_capacitor" + str(k)) * 1e-6
    ii = ii + 1
    with cols[ii]:
        L_reator[k] = st.number_input("$L_{\\rm reator} {\\rm \\left[{\\mu H} \\right]}$",
                                      min_value=0.0, max_value=1000.0, value=200.0, step=1.0,
                                      key="L_reator" + str(k)) * 1e-6




# ===============================================================================================


L_barra_mais_cabo = comp_barra * L_unit_barra + comp_cabo * L_unit_cabo
L = L_barra_mais_cabo + L_capacitor + L_reator

Q_1f = Q_3f / 3

I_fn =  Q_1f / V_fn
X = V_fn / I_fn
C = 1 / ( w_fund * X )
C_paralelos = np.sum(C[1:])
den_C = 1/C[0] + 1/C_paralelos
C_eq = 1/den_C

L_paralelos =  1 / np.sum( 1 / L[1:] )
L_eq = L[0] + L_paralelos

raiz = -(R_eq/L_eq)**2 + 4/(C_eq*L_eq)
omega = np.sqrt(raiz) / 2
num_i = V_fn * np.sqrt(2)
den_i = L_eq * omega
i_pico_inical =  FC * num_i / den_i
sigma = R_eq/(2*L_eq)

t = np.linspace(0, 1/60, 50000 )
i_curto = i_pico_inical * np.exp(-sigma*t) * np.sin(omega*t)



fig = go.Figure()

fig.add_trace(go.Scatter(
    x=t*1e3,
    y=i_curto/1e3,
    name="Instantânea",
    line = dict(shape = 'linear', color = 'rgb(0, 0, 255)', width = 2)
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

fig.add_trace(go.Scatter(
    x=t*1e3,
    y=i_pico_inical * np.sin(2*np.pi*f_fund*t)/1e3,
    name="Ciclo 60 Hz",
    line = dict(shape = 'linear', color = 'rgb(0.2, 0.2, 0.2)', width = 1),
    connectgaps = True)
)

fig.update_layout(legend_title_text='Corrente:', title_text="Inrush Banco de Capacitores",
                  xaxis_title=r"Tempo [ms]", yaxis_title="Corrente [kA]" )
st.plotly_chart(fig, use_container_width=True)

st.write("Corrente de pico considerada = ",         EngNumber(i_pico_inical), "A")
st.write("Ireal/Iconsiderado =",                    np.round(np.max(i_curto)/i_pico_inical, 2))
st.write("Frequência de Oscilação = ",              EngNumber(omega/(2*np.pi)), "Hz")
st.write("Harmônico de Oscilação = ",               EngNumber(omega/w_fund))
temp = i_pico_inical/I_fn[0]
st.write("$\\dfrac{I_{\\rm inrush}}{I_{\\rm nominal}} = $",   EngNumber(temp))

st.markdown('## Conclusão')
if temp < 100:
    st.write("Reator adequado, pois $\\dfrac{I_{\\rm inrush}}{I_{\\rm nominal}} < 100 $")
else:
    st.write("Reator não adequado, pois $\\dfrac{I_{\\rm inrush}}{I_{\\rm nominal}} \\ge 100 $")


st.markdown('## Bibliografia')
st.write("[IEEE Application Guide for Capacitance Current Switching for AC High-Voltage Circuit Breakers Rated on a Symmetrical Current Basis](https://ieeexplore.ieee.org/document/7035261)")


