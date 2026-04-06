import streamlit as st
import numpy as np
from scipy.stats import poisson

# Configurazione Pagina
st.set_page_config(page_title="AI ORACLE v21.0 - PRO", page_icon="🛡️")

st.title("🛡️ AI ORACLE v21.0 - Web Edition")
st.markdown("---")

# --- SEZIONE INPUT (SIDEBAR) ---
with st.sidebar:
    st.header("📊 Quote Mercato")
    q1 = st.number_input("Quota 1", value=2.10)
    qx = st.number_input("Quota X", value=3.20)
    q2 = st.number_input("Quota 2", value=3.50)
    st.markdown("---")
    qgg = st.number_input("Quota Goal", value=1.80)
    qng = st.number_input("Quota No Goal", value=1.90)
    st.markdown("---")
    st.header("⚽ Dettaglio Gol")
    c05 = st.number_input("Over 0.5 Casa", value=1.25)
    c15 = st.number_input("Over 1.5 Casa", value=2.30)
    o05 = st.number_input("Over 0.5 Ospite", value=1.45)
    o15 = st.number_input("Over 1.5 Ospite", value=3.20)

# --- LOGICA DI CALCOLO MATEMATICO ---
if st.button("GENERA ANALISI PROFESSIONALE"):
    # 1. Calcolo Forza Offensiva (Lambda)
    l_c = -np.log(max(0.01, 1 - (1/c05)))
    l_o = -np.log(max(0.01, 1 - (1/o05)))
    
    # Correzione pesata sulla quota Over 1.5 (Analisi Difensiva)
    if (1/c15) < 0.45: l_c *= 0.88
    if (1/o15) < 0.35: l_o *= 0.88

    # 2. Calcolo Probabilità Mercati Principali
    p_u25 = sum(poisson.pmf(c, l_c) * poisson.pmf(o, l_o) for c in range(3) for o in range(3) if c+o <= 2) * 100
    p_o25 = 100 - p_u25
    p_gg = (1 - poisson.pmf(0, l_c)) * (1 - poisson.pmf(0, l_o)) * 100
    p_ng = 100 - p_gg

    # 3. Visualizzazione Analisi di Mercato
    st.subheader("🛡️ ANALISI DI MERCATO")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Under 2.5", f"{p_u25:.1f}%")
        st.metric("Over 2.5", f"{p_o25:.1f}%")
    with col2:
        st.metric("Goal", f"{p_gg:.1f}%")
        st.metric("No Goal", f"{p_ng:.1f}%")

    # 4. FUNZIONE DI CALCOLO COMBO (Identica a Colab)
    def calc_combo_prob(tipo_dc, mg_min, mg_max):
        prob = 0
        for c in range(8): # Simulazione fino a 7 gol
            for o in range(8):
                tot_gol = c + o
                # Controllo Doppia Chance
                match_dc = (c >= o) if tipo_dc == "1X" else (o >= c)
                # Controllo Range Gol
                match_mg = (mg_min <= tot_gol <= mg_max)
                
                if match_dc and match_mg:
                    prob += poisson.pmf(c, l_c) * poisson.pmf(o, l_o)
        return prob * 100

    # Scelta dinamica del range Multigol in base all'Over 2.5
    m_min, m_max = (2, 5) if p_o25 > 55 else (1, 4)

    # CONFRONTO INTELLIGENTE: 1X vs X2
    prob_1x_final = calc_combo_prob("1X", m_min, m_max)
    prob_x2_final = calc_combo_prob("X2", m_min, m_max)

    st.markdown("---")
    st.subheader("🎯 IL PRONOSTICO COMBO")

    # Il sistema sceglie l'opzione con la probabilità più alta
    if prob_1x_final >= prob_x2_final:
        risultato_dc = "1X"
        percentuale = prob_1x_final
    else:
        risultato_dc = "X2"
        percentuale = prob_x2_final

    st.success(f"CONSIGLIO: **{risultato_dc} + MULTIGOL TOTALE {m_min}-{m_max}**")
    st.info(f"PROBABILITÀ ESTIMATA: **{percentuale:.1f}%**")

    # 5. ALERT DEL MOTORE
    st.markdown("---")
    st.subheader("⚠️ ALERT DEL MOTORE")
    alert_count = 0
    
    if p_u25 > 62:
        st.error("🚨 ATTENZIONE: Partita da Under! Possibile 0-0, 1-0 o 0-1.")
        alert_count += 1
    if p_ng > 60:
        st.warning("🚨 ATTENZIONE: Una delle due squadre potrebbe non segnare.")
        alert_count += 1
    
    if alert_count == 0:
        st.write("✅ Nessun Alert: Parametri di mercato stabili.")
