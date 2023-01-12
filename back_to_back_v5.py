"""
Angelo Alfredo Hafner
aah@dax.energy
"""
# import pythoncom
# import win32com
# win32com.client.Dispatch("Word.Application", pythoncom.CoInitialize())
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

import numpy as np

import streamlit as st
import plotly.graph_objects as go
from engineering_notation import EngNumber

st.set_page_config(layout="wide")
R_eq = 0.1

# ===================================================================================

st.markdown('# Resposta transitória de corrente durante a energização de capacitores')
col0, col1, col2, col3 = st.columns([3, 1, 0.01, 5])

with col0:
    st.image(image='IMG_24052017_115903_0.png')

with col1:
    FC = st.slider("Fator de Segurança", min_value=1.0, max_value=1.5, value=1.4, step=0.1)
    nr_bancos = st.slider("Número de Bancos", min_value=2, max_value=20, value=4, step=1)

with col1:
    V_ff = st.number_input("Tensão 3𝝋 [kV]", min_value=13.8, max_value=380.0, value=23.1, step=0.1) * 1e3
    V_fn = V_ff / np.sqrt(3)
    f_fund = st.number_input("Frequência [Hz]", min_value=50.0, max_value=60.0, value=60.0, step=0.1)
    w_fund = 2 * np.pi * f_fund

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
cols = st.columns(5)
ii = 0
k = 0
k = 0
with cols[ii]:
    Q_3f[k] = st.number_input("$Q_{3\\varphi}$[kVAr] ",
                              min_value=100.0, max_value=100e3, value=12000.0, step=0.0,
                              key="Q_3f_" + str(k)) * 1e3
ii = ii + 1
with cols[ii]:
    comp_cabo[k] = st.number_input("$\\ell_{\\rm cabo}{\\rm [m]}$",
                                   min_value=0.0, max_value=100.0, value=0.0, step=0.01,
                                   key="comp_cabo" + str(k))
# ii = ii + 1
# with cols[ii]:
#         comp_barra[k] =  st.number_input("$\\ell_{\\rm barra}{\\rm [m]}$",
#                                         min_value=0.0,  max_value=100.0, value=0.0, step=0.01,
#                                         key="comp_barra"+str(k))
ii = ii + 1
with cols[ii]:
    L_unit_cabo[k] = st.number_input("$L'_{\\rm cabo} {\\rm \\left[{\\mu H}/{m} \\right]}$",
                                     min_value=0.00, max_value=100.0, value=0.00, step=0.01,
                                     key="L_unit_cabo" + str(k)) * 1e-6
# ii = ii + 1
# with cols[ii]:
#         L_unit_barra[k] =  st.number_input("$L'_{\\rm barra} {\\rm \\left[{\\mu H}/{m} \\right]}$",
#                                         min_value=0.0,  max_value=100.0, value=0.00, step=0.01,
#                                         key="L_unit_barra"+str(k)) * 1e-6
ii = ii + 1
with cols[ii]:
    L_capacitor[k] = st.number_input("$L_{\\rm capacitor} {\\rm \\left[{\\mu H} \\right]}$",
                                     min_value=0.0, max_value=100.0, value=5.00, step=0.01,
                                     key="L_capacitor" + str(k)) * 1e-6
ii = ii + 1
with cols[ii]:
    L_reator[k] = st.number_input("$L_{\\rm reator} {\\rm \\left[{\\mu H} \\right]}$",
                                  min_value=0.0, max_value=1000.0, value=100.0, step=1.0,
                                  key="L_reator" + str(k)) * 1e-6

st.markdown("### Demais Bancos $($#$1$ ao #$n)$")
st.markdown("Bancos que já estão energizados.")
cols = st.columns(5)
for k in range(1, nr_bancos):
    ii = 0
    with cols[ii]:
        Q_3f[k] = st.number_input("$Q_{3\\varphi}$[kVAr] ",
                                  min_value=100.0, max_value=100e3, value=12000.0, step=0.0,
                                  key="Q_3f_" + str(k)) * 1e3
    ii = ii + 1
    with cols[ii]:
        comp_cabo[k] = st.number_input("$\\ell_{\\rm cabo}{\\rm [m]}$",
                                       min_value=0.0, max_value=100.0, value=0.0, step=0.01,
                                       key="comp_cabo" + str(k))
    # ii = ii + 1
    # with cols[ii]:
    #     comp_barra[k] = st.number_input("$\\ell_{\\rm barra}{\\rm [m]}$",
    #                                     min_value=0.0, max_value=100.0, value=0.0, step=0.01,
    #                                     key="comp_barra" + str(k))
    ii = ii + 1
    with cols[ii]:
        L_unit_cabo[k] = st.number_input("$L'_{\\rm cabo} {\\rm \\left[{\\mu H}/{m} \\right]}$",
                                         min_value=0.0, max_value=100.0, value=0.00, step=0.01,
                                         key="L_unit_cabo" + str(k)) * 1e-6
    # ii = ii + 1
    # with cols[ii]:
    #     L_unit_barra[k] = st.number_input("$L'_{\\rm barra} {\\rm \\left[{\\mu H}/{m} \\right]}$",
    #                                       min_value=0.0, max_value=100.0, value=0.00, step=0.01,
    #                                       key="L_unit_barra" + str(k)) * 1e-6
    ii = ii + 1
    with cols[ii]:
        L_capacitor[k] = st.number_input("$L_{\\rm capacitor} {\\rm \\left[{\\mu H} \\right]}$",
                                         min_value=0.0, max_value=100.0, value=5.00, step=0.01,
                                         key="L_capacitor" + str(k)) * 1e-6
    ii = ii + 1
    with cols[ii]:
        L_reator[k] = st.number_input("$L_{\\rm reator} {\\rm \\left[{\\mu H} \\right]}$",
                                      min_value=0.1, max_value=10000.0, value=100.0, step=1.0,
                                      key="L_reator" + str(k)) * 1e-6

# ===============================================================================================


L_barra_mais_cabo = comp_barra * L_unit_barra + comp_cabo * L_unit_cabo
L = L_barra_mais_cabo + L_capacitor + L_reator

Q_1f = Q_3f / 3

I_fn = Q_1f / V_fn
X = V_fn / I_fn
C = 1 / (w_fund * X)
C_paralelos = np.sum(C[1:])
den_C = 1 / C[0] + 1 / C_paralelos
C_eq = 1 / den_C

L_paralelos = 1 / np.sum(1 / L[1:])
L_eq = L[0] + L_paralelos

raiz = -(R_eq / L_eq) ** 2 + 4 / (C_eq * L_eq)
omega = np.sqrt(raiz) / 2
num_i = V_fn * np.sqrt(2)
den_i = L_eq * omega
i_pico_inical = FC * num_i / den_i
sigma = R_eq / (2 * L_eq)

t = np.linspace(0, 1 / 60, int(2 ** 10))
i_curto = i_pico_inical * np.exp(-sigma * t) * np.sin(omega * t)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=t * 1e3,
    y=i_curto / 1e3,
    name="Instantânea",
    line=dict(shape='linear', color='rgb(0, 0, 255)', width=2)
))

fig.add_trace(go.Scatter(
    x=t * 1e3,
    y=i_pico_inical * np.exp(-sigma * t) / 1e3,
    name="Envelope",
    line=dict(shape='linear', color='rgb(0, 0, 0)', width=1, dash='dot'),
    connectgaps=True)
)

fig.add_trace(go.Scatter(
    x=t * 1e3,
    y=-i_pico_inical * np.exp(-sigma * t) / 1e3,
    name="Envelope",
    line=dict(shape='linear', color='rgb(0, 0, 0)', width=1, dash='dot'),
    connectgaps=True)
)

fig.add_trace(go.Scatter(
    x=t * 1e3,
    y=i_pico_inical * np.sin(2 * np.pi * f_fund * t) / 1e3,
    name="Ciclo 60 Hz",
    line=dict(shape='linear', color='rgb(0.2, 0.2, 0.2)', width=1),
    connectgaps=True)
)

fig.update_layout(legend_title_text='Corrente:', title_text="Inrush Banco de Capacitores",
                  xaxis_title=r"Tempo [ms]", yaxis_title="Corrente [kA]")
st.plotly_chart(fig, use_container_width=True)

coluna0, coluna1 = st.columns([1, 1])

with coluna0:
    st.write("Corrente de pico considerada = ", EngNumber(i_pico_inical), "A")
    # st.write("Ireal/Iconsiderado =",                    np.round(np.max(i_curto)/i_pico_inical, 2))
    st.write("Frequência de Oscilação = ", EngNumber(omega / (2 * np.pi)), "Hz")
    st.write("Harmônico de Oscilação = ", EngNumber(omega / w_fund))
    temp = i_pico_inical / (I_fn[0] * np.sqrt(2))

with coluna1:
    st.markdown('## Conclusão')
    conclusao1 = "cuidado aqui"
    if temp < 100:
        conclusao1 = "Reator adequado"
        st.write("Reator adequado, pois $\\dfrac{I_{\\rm inrush}}{I_{\\rm nominal}} = $", EngNumber(temp),
                 "$\\le 100$.")
    else:
        st.write("Reator não adequado, pois $\\dfrac{I_{\\rm inrush}}{I_{\\rm nominal}} = $", EngNumber(temp),
                 "$\\ge 100.$")
        conclusao1 = "Reator não adequado"

    cem = str(EngNumber(temp))

st.markdown('## Bibliografia')
st.write(
    "[IEEE Application Guide for Capacitance Current Switching for AC High-Voltage Circuit Breakers Rated on a Symmetrical Current Basis](https://ieeexplore.ieee.org/document/7035261)")

# ===============================================================================================================
# RELATORIO
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
from docx2pdf import convert

t = np.asarray(t)
i_curto = i_pico_inical * np.exp(-sigma * t) * np.sin(omega * t)
mpl.rcParams.update({'font.size': 8})
cm = 1 / 2.54
fig_mpl, ax_mpl = plt.subplots(figsize=(16 * cm, 7 * cm))
ax_mpl.plot(t * 1e3, i_curto / 1e3, label='$i(t)$', color='blue', lw=1.0)
ax_mpl.plot(t * 1e3, i_pico_inical * np.exp(-sigma * t) / 1e3, color='gray', ls='--', lw=0.5)
ax_mpl.plot(t * 1e3, -i_pico_inical * np.exp(-sigma * t) / 1e3, color='gray', ls='--', lw=0.5)
ax_mpl.plot(t * 1e3, i_pico_inical * np.sin(2 * np.pi * f_fund * t) / 1e3, label='$60 {\\rm Hz}$', color='gray',
            alpha=0.5, lw=1.0)
ax_mpl.set_xlabel('Tempo [ms]')
ax_mpl.set_ylabel('Corrente [kA]')
ax_mpl.legend()
fig_mpl.savefig('Correntes.png', bbox_inches='tight', dpi=200)

flag_relatorio = 0
if st.button('Gerar Relatório'):
    from docxtpl import DocxTemplate, InlineImage
    import datetime as dt

    doc = DocxTemplate("Inrush_template_word.docx")
    context = {
        "Correntes_figura": InlineImage(doc, "Correntes.png"),
        "indutância_escolhida": str(EngNumber(L_reator[0])),
        "corrente_pico": str(EngNumber(i_pico_inical)),
        "frequencia_oscilacao": str(EngNumber(omega / (2 * np.pi))),
        "inrush_inominal": str(int(i_pico_inical / (I_fn[0] * np.sqrt(2)))),
        "conclusao1": conclusao1,
        "cem": cem,
        "data": dt.datetime.now().strftime("%d-%b-%Y")
    }
    doc.render(context)
    doc.save('Relatorio_Inrush_DAX.docx')
    flag_relatorio = 1

if flag_relatorio:
    import docx2pdf
    docx2pdf.convert("Relatorio_Inrush_DAX.docx", "Relatorio_Inrush_DAX.pdf")

    with open("Relatorio_Inrush_DAX.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

        st.download_button(label="Download",
                        data=PDFbyte,
                        file_name="Inrush_DAX_Report.pdf",
                        mime='application/octet-stream')

colunas = st.columns(2)
with colunas[0]:
    st.markdown('#### Desenvolvimento')
    """
    Angelo A. Hafner\\
    Engenheiro Eletricista\\
    Confea: 2.500.821.919\\
    Crea/SC: 045.776-5\\
    aah@dax.energy
    """
with colunas[1]:
    st.markdown('#### Comercial')
    """
    Tiago Machado\\
    Business Manager\\
    Mobile: +55 41 99940-3744\\
    tm@dax.energy
    """
