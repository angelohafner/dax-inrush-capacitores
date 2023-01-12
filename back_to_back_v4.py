
"""
Angelo Alfredo Hafner
aah@dax.energy
"""
from engineering_notation import EngNumber
import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.graph_objects as go
from engineering_notation import EngNumber



# ===================================================================================

def show_grid(df):

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True)
    grid_table = AgGrid(
        df,
        height=400,
        gridOptions=gb.build(),
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
    )
    return grid_table

def update(grid_table):
    grid_table_df = pd.DataFrame(grid_table['data'])
    grid_table_df.to_csv('data.csv', index=False)

# ===================================================================================

df = pd.read_csv("data.csv", header=0, dtype=np.float64)


st.markdown('# Resposta transitória da energização de capacitores DAX-Energy')
col1, col2 = st.columns([3, 1])

with col1:
    st.image(image='Sistema.png', width=500)

with col2:
    FC          =   st.number_input("Fator de Segurança", min_value=1.0,  max_value=1.4, value=1.4, step=0.1)
    V_ff        =   st.number_input("Tensão fase-fase [kV]", min_value=13.8,  max_value=380.0, value=23.1, step=0.1) * 1e3
    V_fn        =   V_ff / np.sqrt(3)
    f_fund      =   st.number_input("Frequência [Hz]", min_value=50.0,  max_value=60.0, value=60.0, step=0.1)
    w_fund      =   2*np.pi*f_fund
    nr_bancos        =   st.number_input("Número de Bancos", min_value=1,  max_value=11, value=2, step=1)
    

grid_table = show_grid(df)
st.sidebar.button("Update", on_click=update, args=[grid_table])

nr_bancos = np.min(np.where(df.isna().any(axis=1)))
nr_bancos

Q_3f            = df.iloc[0:nr_bancos, 1].values * 1e3
comp_cabo       = df.iloc[0:nr_bancos, 2].values
comp_barra      = df.iloc[0:nr_bancos, 3].values
L_unit_cabo     = df.iloc[0:nr_bancos, 4].values * 1e-6
L_unit_barra    = df.iloc[0:nr_bancos, 5].values * 1e-6
L_reator        = df.iloc[0:nr_bancos, 6].values * 1e-6
L_capacitor     = df.iloc[0:nr_bancos, 7].values * 1e-6
# L_reator[0]     = L_reator_


L_barra_mais_cabo = comp_barra * L_unit_barra + comp_cabo * L_unit_cabo
L = L_barra_mais_cabo + L_capacitor + L_reator



Q_1f = Q_3f / 3
I_fn = np.zeros(nr_bancos, dtype=float)
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

t = np.linspace(0, 3/sigma, 10000 )
i_curto = i_pico_inical * np.exp(-sigma*t) * np.sin(omega*t)



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


