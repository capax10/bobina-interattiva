import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

# Funzione per disegnare il rotolo con stile migliorato

def draw_roll(D, L):
    fig, ax = plt.subplots(figsize=(7, 7))
    R = D / 2
    theta = L / R

    # Sfondo più chiaro e griglia
    ax.set_facecolor("#f9f9f9")
    ax.grid(True, linestyle='--', alpha=0.3)

    # Rotolo e nucleo
    roll = plt.Circle((0, 0), R, fill=False, linewidth=2, edgecolor="#333")
    core = plt.Circle((0, 0), R * 0.3, fill=False, linestyle='--', linewidth=1.2, edgecolor="#666")
    ax.add_patch(roll)
    ax.add_patch(core)

    # Punto di partenza a ore 7 (210°)
    angle_start = 7 * np.pi / 6
    x_start = R * np.cos(angle_start)
    y_start = R * np.sin(angle_start)

    # Punto colla dopo rotazione
    angle_colla_rotated = angle_start - theta
    x_colla = R * np.cos(angle_colla_rotated)
    y_colla = R * np.sin(angle_colla_rotated)

    # Disegno del velo
    ax.plot([x_start, x_colla], [y_start, y_colla], color="#4caf50", linewidth=2.5, label='Velo L')
    ax.plot([x_colla], [y_colla], 'o', color="#e53935", markersize=8, label='Colla')

    # Arco evidenziato
    arc = patches.Arc((0, 0), 2*R, 2*R, angle=0,
                      theta1=np.degrees(angle_colla_rotated),
                      theta2=np.degrees(angle_start),
                      color='#ffa726', linewidth=2.5, label='Arco L')
    ax.add_patch(arc)

    # Etichette ore
    x_ore12 = R * np.cos(np.pi / 2)
    y_ore12 = R * np.sin(np.pi / 2)
    ax.text(x_ore12, y_ore12 + 25, "Ore 12", ha='center', va='bottom', fontsize=10, color='black')

    x_ore7 = R * np.cos(angle_start)
    y_ore7 = R * np.sin(angle_start)
    ax.text(x_ore7 - 25, y_ore7 - 15, "Ore 7", ha='right', va='top', fontsize=10, color='black')

    # Rulli
    rullo_raggio = 20
    rullo_offset_y = -R - 40
    distanza_rulli = 2 * R * 0.8
    ax.add_patch(plt.Circle((-distanza_rulli / 2, rullo_offset_y), rullo_raggio, color='#888'))
    ax.add_patch(plt.Circle((distanza_rulli / 2, rullo_offset_y), rullo_raggio, color='#888'))

    # Impostazioni finali
    ax.set_xlim(-R - 150, R + 150)
    ax.set_ylim(rullo_offset_y - 60, R + 120)
    ax.set_aspect('equal')
    ax.set_title(f"\u2728 Bobina Interattiva \u2728\nDiametro = {D:.0f} mm | Lunghezza Velo = {L:.0f} mm | θ = {np.degrees(theta):.2f}°",
                 fontsize=13, fontweight='bold', color="#333")
    ax.legend(loc='upper right', frameon=True, framealpha=0.9)

    return fig

# Streamlit app
st.set_page_config(page_title="Bobina Interattiva", layout="centered")
st.title("🌀 Bobina Interattiva")

D = st.slider("Diametro della bobina (mm)", min_value=800, max_value=1200, value=1000, step=10)
L = st.slider("Lunghezza del velo (mm)", min_value=50, max_value=600, value=300, step=10)

fig = draw_roll(D, L)
st.pyplot(fig, use_container_width=True)

st.markdown(f"#### θ = {np.degrees(L / (D/2)):.2f}° di rotazione necessaria")
