import streamlit as st
import numpy as np
from scipy.stats import poisson

st.set_page_config(page_title="AI ORACLE v21.0 - Official", page_icon="🛡️")

st.title("🛡️ AI ORACLE v21.0")
st.write("Sincronizzato con la logica Colab")

# --- INPUT QUOTE ---
with st.sidebar:
    st.header("Quote 1X2")
    q1 = st.number_input("Quota 1", value=2.10)
    qx = st.number_input("Quota X", value=3.10)
    q2 = st.number_input("Quota 2", value=3.50)
    
    st.header("Quote Gol/NoGol")
    qgg = st.number_input("Quota Goal", value=1.80)
    qng = st.number_input("Quota No Goal", value=1.90)

    st.header("Dettaglio Over Casa/Ospite")
    c05 = st.number_input("Over 0.5 Casa", value=1.25)
    c15 = st.number_input("Over 1.5 Casa", value=2.30)
    o05 = st.number_input("Over 0.5 Ospite", value=1.45)
    o15 = st.number_input("Over 1.5 Ospite", value=3.20)

if st.button("ESEGUI ANALISI DI MERCATO"):
    # 1. Calcolo Lambda (Forza Offensiva)
    l_c = -np.log(max(0.01, 1 - (1/c05)))
    l_o = -np.log(max(0.01, 1 - (1/o05)))
    
    # Correzione basata sulla quota Over 1.5 (Peso Difensivo)
    if (1/c15) < 0.45: l_c *= 0.88
    if (1/o15) < 0.35: l_o *= 0.88

    # 2. Calcolo Probabilità Base
    p_u25 = sum(poisson.pmf(c, l_c) * poisson.pmf(o, l_o) for c in range(3) for o in range(3) if c+o <= 2) * 100
    p_o25 = 100 - p_u25
    p_gg = (1 - poisson.pmf(0, l_c)) * (1 - poisson.pmf(0, l_o)) * 100
    p_ng = 100 - p_gg

    # 3. Visualizzazione Analisi
    st.markdown("### 🛡️ ANALISI DI MERCATO")
    c1, c2 = st.columns(2)
    c1.metric("Under 2.5", f"{p_u25:.1f}%")
    c1.metric("Over 2.5", f"{p_o25:.1f}%")
    c2.metric("Goal", f"{p_gg:.1f}%")
    c2.metric("No Goal", f"{p_ng:.1f}%")

    # 4. LOGICA DI SELEZIONE COMBO (Identica al Colab)
    # Calcoliamo i vari range per trovare il migliore
    def calc_prob(dc_type, mg_min, mg_max):
        prob = 0
        for c in range(7):
            for o in range(7):
                tot = c + o
                is_dc = (c >= o) if dc_type == "1X" else (o >= c)
                if is_dc and mg_min <= tot <= mg_max:
                    prob += poisson.pmf(c, l_c) * poisson.pmf(o, l_o)
        return prob * 100

    # Testiamo i range
    res_1x_14 = calc_prob("1X", 1, 4)
    res_1x_25 = calc_prob("1X", 2, 5)
    
    st.markdown("---")
    st.markdown("### 🎯 IL PRONOSTICO COMBO")
    
    # Se l'Over 2.5 è dominante, preferiamo il 2-5, altrimenti l'1-4 (Logica Colab)
    if p_o25 > 55:
        st.success(f"CONSIGLIO: 1X + MULTIGOL TOTALE 2-5")
        st.write(f"PROBABILITÀ: {res_1x_25:.1f}%")
    else:
        st.success(f"CONSIGLIO: 1X + MULTIGOL TOTALE 1-4")
        st.write(f"PROBABILITÀ: {res_1x_14:.1f}%")

    # 5. ALERT DEL MOTORE
    st.markdown("### ⚠️ ALERT DEL MOTORE")
    if p_u25 > 62: st.error("🚨 ATTENZIONE: Partita da Under! Rischio 0-0 / 1-1")
    if p_ng > 58: st.warning("🚨 ATTENZIONE: Una delle due potrebbe non segnare.")
    if p_u25 < 62 and p_ng < 58: st.info("✅ Nessun Alert: Parametri di mercato stabili.")
