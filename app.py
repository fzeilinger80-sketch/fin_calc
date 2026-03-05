import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Seiten-Konfiguration (Titel und Icon)
st.set_page_config(page_title="Zinseszins Rechner", page_icon="📈")

st.title("📈 Dein ETF Rechner")
st.write("Berechne, wie dein Geld über die Jahre für dich arbeitet.")

# 1. Eingabefelder (Die schöne Benutzeroberfläche)
col1, col2 = st.columns(2)
with col1:
    startkapital = st.number_input("Startkapital (CHF)", value=25000, step=1000)
    sparplan = st.number_input("Monatliche Sparrate (CHF)", value=300, step=50)
with col2:
    rendite_pa = st.number_input("Rendite pro Jahr (%)", value=10.0, step=1.0) / 100
    jahre = st.number_input("Laufzeit (Jahre)", value=10, min_value=1, max_value=50, step=1)

# 2. Mathematik
rendite_pm = rendite_pa / 12
jahre_array = np.arange(0, jahre + 1)
eingezahlt_array = np.zeros(jahre + 1)
kapital_array = np.zeros(jahre + 1)

eingezahlt_array[0] = startkapital
kapital_array[0] = startkapital

aktuell_eingezahlt = startkapital
aktuelles_kapital = startkapital

for jahr in range(1, jahre + 1):
    for_jahr_kapital = aktuelles_kapital
    for _ in range(12):
        for_jahr_kapital = for_jahr_kapital * (1 + rendite_pm) + sparplan
    
    aktuell_eingezahlt += sparplan * 12
    aktuelles_kapital = for_jahr_kapital

    eingezahlt_array[jahr] = aktuell_eingezahlt
    kapital_array[jahr] = aktuelles_kapital

gewinn = aktuelles_kapital - aktuell_eingezahlt

# 3. Ergebnisse groß anzeigen
st.divider()
st.subheader("Ergebnis")
metric1, metric2, metric3 = st.columns(3)
metric1.metric("Eingezahlt", f"{aktuell_eingezahlt:,.0f} CHF")
metric2.metric("Reiner Gewinn", f"{gewinn:,.0f} CHF")
metric3.metric("Endkapital", f"{aktuelles_kapital:,.0f} CHF")

# 4. Den Plot zeichnen und in der App anzeigen
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(jahre_array, kapital_array, label='Gesamtkapital', color='#2ca02c', linewidth=2)
ax.plot(jahre_array, eingezahlt_array, label='Selbst eingezahlt', color='#1f77b4', linewidth=2)
ax.fill_between(jahre_array, eingezahlt_array, kapital_array, color='#2ca02c', alpha=0.2)
ax.fill_between(jahre_array, 0, eingezahlt_array, color='#1f77b4', alpha=0.1)

ax.set_title("Vermögensentwicklung")
ax.set_xlabel("Jahre")
ax.set_ylabel("CHF")
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

# Plot an Streamlit übergeben

st.pyplot(fig)
