import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

# Funzione per disegnare il rotolo con stile corretto secondo la logica reale

def draw_roll(D, L):
    fig, ax = plt.subplots(figsize=(7, 7))
    R = D / 2
    theta = L / R  # rotazione in radianti

    # Sfondo e griglia
    ax.set_facecolor("#f9f9f9")
    ax.grid(True, linestyle='--', alpha=0.3)

    # Rotolo e nucleo
    roll = plt.Circle((0, 0), R, fill=False, linewidth=2, edgecolor="#333")
    core = plt.Circle((0, 0), R * 0.3, fill=False, linestyle='--', linewidth=1.2, edgecolor="#666")
    ax.add_patch(roll)
    ax.add_patch(core)

    # Colla iniziale a 90° (ore 12)
    angle_colla_initial = np.pi / 2
    x_colla_initial = R * np.cos(angle_colla_initial)
    y_colla_initial = R * np.sin(angle_colla_initial)

    # Dopo la rotazione, il punto colla si sposta in avanti (in senso orario)
    angle_colla_rotated = angle_colla_initial - theta
    x_colla_rotated = R * np.cos(angle_colla_rotated)
    y_colla_rotated = R * np.sin(angle_colla_rotated)

    # Disegno del tratto di velo (dal nuovo punto colla al punto in uscita - idealizzato verso sinistra)
    ax.plot([x_colla_rotated, x_colla_rotated - L], [y_colla_rotated, y_colla_rotated],
            color="#4caf50", linewidth=2.5, label='Velo tagliato (L)')

    # Punti colla
    ax.plot([x_colla_initial], [y_colla_initial], 'o', color="#e53935", markersize=8, label='Colla applicata (inizio)')
    ax.plot([x_colla_rotated], [y_colla_rotated], 'o', color="#1e88e5", markersize=8, label='Colla dopo rotazione')

    # Arco di rotazione
    arc = patches.Arc((0, 0), 2*R, 2*R, angle=0,
                      theta1=90,
                      theta2=np.degrees(angle_colla_rotated),
                      color='#ffa726', linewidth=2.5, label='Rotazione θ')
    ax.add_patch(arc)

    # Arco interno per θ
    arc_theta = patches.Arc((0, 0), 0.6*R, 0.6*R, angle=0,
                            theta1=90,
                            theta2=np.degrees(angle_colla_rotated),
                            color='blue', linewidth=1.5, linestyle='--')
    ax.add_patch(arc_theta)
    angle_label = (angle_colla_initial + angle_colla_rotated) / 2
    x_theta = 0.4 * R * np.cos(angle_label)
    y_theta = 0.4 * R * np.sin(angle_label)
    ax.text(x_theta, y_theta, 'θ', fontsize=14, color='blue', ha='center', va='center')

    # Etichette gradi
    for deg in [0, 90, 180, 210, 250, 270, 360]:
        angle_rad = np.radians(deg)
        x = (R + 20) * np.cos(angle_rad)
        y = (R + 20) * np.sin(angle_rad)
        ax.text(x, y, f"{deg}°", ha='center', va='center', fontsize=9, color='black')

    # Rulli
    rullo_raggio = 20
    rullo_offset_y = -R - 40
    distanza_rulli = 2 * R * 0.8
    ax.add_patch(plt.Circle((-distanza_rulli / 2, rullo_offset_y), rullo_raggio, color='#888'))
    ax.add_patch(plt.Circle((distanza_rulli / 2, rullo_offset_y), rullo_raggio, color='#888'))

    # Impostazioni finali
    ax.set_xlim(-R - 200, R + 200)
    ax.set_ylim(rullo_offset_y - 60, R + 120)
    ax.set_aspect('equal')
    ax.set_title(f"\u2728 Bobina Interattiva \u2728\nDiametro = {D:.0f} mm | Velo tagliato = {L:.0f} mm | Rotazione θ = {np.degrees(theta):.2f}°",
                 fontsize=13, fontweight='bold', color="#333")
    ax.legend(loc='upper right', frameon=True, framealpha=0.9)

    return fig

# Streamlit app
st.set_page_config(page_title="Bobina Interattiva", layout="centered")
st.title("🌀 Bobina Interattiva")

D = st.slider("Diametro della bobina (mm)", min_value=800, max_value=1200, value=1000, step=10)
L = st.slider("Lunghezza del velo (mm)", min_value=50, max_value=2000, value=1200, step=10)

fig = draw_roll(D, L)
st.pyplot(fig, use_container_width=True)

st.markdown(f"#### θ = {np.degrees(L / (D/2)):.2f}° di rotazione necessaria per chiudere il velo")


