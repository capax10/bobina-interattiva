import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

# Funzione aggiornata secondo il disegno utente e logica reale

def draw_roll(D, L):
    fig, ax = plt.subplots(figsize=(7, 7))
    R = D / 2
    theta = L / R  # angolo in radianti che rappresenta la rotazione da applicare prima del taglio
    theta_deg = np.degrees(theta)

    # Sfondo e griglia
    ax.set_facecolor("#f9f9f9")
    ax.grid(True, linestyle='--', alpha=0.3)

    # Rotolo e nucleo
    roll = plt.Circle((0, 0), R, fill=False, linewidth=2, edgecolor="#333")
    core = plt.Circle((0, 0), R * 0.3, fill=False, linestyle='--', linewidth=1.2, edgecolor="#666")
    ax.add_patch(roll)
    ax.add_patch(core)

    # Punto fisso di contatto con il rullo (dove inizia il velo dopo il taglio)
    angle_contatto_deg = 250
    angle_contatto_rad = np.radians(angle_contatto_deg)
    x_contatto = R * np.cos(angle_contatto_rad)
    y_contatto = R * np.sin(angle_contatto_rad)

    # Punto colla iniziale (a 90°)
    angle_colla_init_rad = np.pi / 2
    x_colla_init = R * np.cos(angle_colla_init_rad)
    y_colla_init = R * np.sin(angle_colla_init_rad)

    # Punto colla dopo rotazione (ruotiamo INDIETRO di θ, senso antiorario)
    angle_colla_rotated_rad = angle_colla_init_rad + theta
    x_colla_rotated = R * np.cos(angle_colla_rotated_rad)
    y_colla_rotated = R * np.sin(angle_colla_rotated_rad)

    # Disegno tratto di velo (parte marrone): da contatto verso sinistra
    ax.plot([x_contatto - L, x_contatto], [y_contatto, y_contatto],
            color="#795548", linewidth=3.0, label='Velo da tagliare (L)')

    # Colla
    ax.plot([x_colla_init], [y_colla_init], 'o', color="#e53935", markersize=8, label='Colla applicata (@90°)')
    ax.plot([x_contatto], [y_contatto], 'o', color="#1e88e5", markersize=8, label='Posizione finale della colla (dopo rotazione)')

    # Arco θ (antiorario, da 90° a 90° + θ)
    arc = patches.Arc((0, 0), 2*R, 2*R, angle=0,
                      theta1=90,
                      theta2=90 + theta_deg,
                      color='#ffa726', linewidth=2.5, label='Rotazione θ')
    ax.add_patch(arc)

    # Arco interno per θ
    arc_theta = patches.Arc((0, 0), 0.6*R, 0.6*R, angle=0,
                            theta1=90,
                            theta2=90 + theta_deg,
                            color='blue', linewidth=1.5, linestyle='--')
    ax.add_patch(arc_theta)
    angle_label = (angle_colla_init_rad + angle_colla_rotated_rad) / 2
    x_theta = 0.4 * R * np.cos(angle_label)
    y_theta = 0.4 * R * np.sin(angle_label)
    ax.text(x_theta, y_theta, 'θ', fontsize=14, color='blue', ha='center', va='center')

    # Etichette gradi
    for deg in [0, 90, 180, 210, 250, 270, 360]:
        angle_rad = np.radians(deg)
        x = (R + 20) * np.cos(angle_rad)
        y = (R + 20) * np.sin(angle_rad)
        ax.text(x, y, f"{deg}°", ha='center', va='center', fontsize=9, color='black')

    # Rulli (grigi + evidenziati in giallo)
    rullo_raggio = 20
    rullo_offset_y = -R - 40
    distanza_rulli = 2 * R * 0.8
    for x in [-distanza_rulli/2, distanza_rulli/2]:
        ax.add_patch(plt.Circle((x, rullo_offset_y), rullo_raggio, color='gray'))
        ax.add_patch(plt.Circle((x, rullo_offset_y), rullo_raggio+5, fill=False, edgecolor='yellow', linewidth=2))

    # Impostazioni finali
    ax.set_xlim(-R - 200, R + 200)
    ax.set_ylim(rullo_offset_y - 60, R + 120)
    ax.set_aspect('equal')
    ax.set_title(f"\u2728 Bobina Interattiva \u2728\nDiametro = {D:.0f} mm | Lunghezza Velo = {L:.0f} mm | Rotazione θ = {theta_deg:.2f}°",
                 fontsize=13, fontweight='bold', color="#333")

    return fig

# Streamlit app
st.set_page_config(page_title="Bobina Interattiva", layout="centered")
st.title("🌀 Bobina Interattiva")

D = st.slider("Diametro della bobina (mm)", min_value=800, max_value=1200, value=1000, step=10)
L = st.slider("Lunghezza del velo (mm)", min_value=50, max_value=2000, value=1200, step=10)

fig = draw_roll(D, L)
st.pyplot(fig, use_container_width=True)

# Legenda esterna
st.markdown("<div style='display: flex; justify-content: center;'>",
            unsafe_allow_html=True)
st.pyplot(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"#### θ = {(360 * L / (np.pi * D)):.2f}° → Rotazione da applicare PRIMA del taglio per far combaciare la colla")

