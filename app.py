import streamlit as st
import numpy as np
from scipy.stats import poisson

st.set_page_config(page_title="AI ORACLE v21.0", page_icon="📈")

st.title("⚽ AI ORACLE v21.0")
st.markdown("---")

# Sezione Input laterale (o in alto su mobile)
st.subheader("📊 Inserisci le Quote")
col_q1, col_qx, col_q2 = st.columns(3)
with col_q1: q1 = st.number_input("Quota 1", value=2.10)
with col_qx: qx = st.number_input("Quota X", value=3.20)
with col_q2: q2 = st.number_input("Quota 2", value=3.40)

col_gg, col_ng = st.columns(2)
with col_gg: qgg = st.number_input("Quota Goal", value=1.85)
with col_ng: qng = st.number_input("Quota No Goal", value=1.85)

st.markdown("---")
st.subheader("🎯 Dettaglio Gol (Over 0.5 / 1.5)")
c1, c2 = st.columns(2)
with c1: 
    c_05 = st.number_input("Over 0.5 Casa", value=1.25)
    c_15 = st.number_input("Over 1.5 Casa", value=2.20)
with c2:
    o_05 = st.number_input("Over 0.5 Ospite", value=1.40)
    o_15 = st.number_input("Over 1.5 Ospite", value=3.10)

if st.button("CALCOLA PRONOSTICO"):
    # Calcolo Logica Poisson
    l_casa = -np.log(max(0.01, 1 - (1/c_05)))
    l_ospite = -np.log(max(0.01, 1 - (1/o_05)))
    if (1/c_15) < 0.45: l_casa *= 0.85
    if (1/o_15) < 0.45: l_ospite *= 0.85

    p_u25 = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite) for c in range(3) for o in range(3) if c+o <= 2) * 100
    p_o25 = 100 - p_u25
    p_gg = (1 - poisson.pmf(0, l_casa)) * (1 - poisson.pmf(0, l_ospite)) * 100
    p_ng = 100 - p_gg

    # Mostra Risultati
    st.info(f"🛡️ ANALISI: Over 2.5: {p_o25:.1f}% | Goal: {p_gg:.1f}%")
    
    # Calcolo Combo (Esempio 1X + MG 1-4)
    p_1x_mg = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite) for c in range(6) for o in range(6) if c >= o and 1 <= (c+o) <= 4) * 100
    
    st.success(f"🎯 CONSIGLIO: 1X + MULTIGOL 1-4")
    st.metric("AFFIDABILITÀ", f"{p_1x_mg:.1f}%")

    if p_u25 > 60: st.warning("⚠️ ALERT: Partita da UNDER!")
