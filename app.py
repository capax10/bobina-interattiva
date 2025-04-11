import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

# Funzione aggiornata secondo i 4 step reali del processo

def draw_roll(D, L):
    fig, ax = plt.subplots(figsize=(7, 7))
    R = D / 2
    theta = L / R  # angolo in radianti della rotazione PRE-TAGLIO necessaria
    theta_deg = np.degrees(theta)

    # Sfondo e griglia
    ax.set_facecolor("#f9f9f9")
    ax.grid(True, linestyle='--', alpha=0.3)

    # Rotolo e nucleo
    roll = plt.Circle((0, 0), R, fill=False, linewidth=2, edgecolor="#333")
    core = plt.Circle((0, 0), R * 0.3, fill=False, linestyle='--', linewidth=1.2, edgecolor="#666")
    ax.add_patch(roll)
    ax.add_patch(core)

    # Punto di nip fisso (250°)
    angle_nip_deg = 250
    angle_nip_rad = np.radians(angle_nip_deg)
    x_nip = R * np.cos(angle_nip_rad)
    y_nip = R * np.sin(angle_nip_rad)

    # Punto colla iniziale (90°)
    angle_colla_rad = np.pi / 2
    x_colla_init = R * np.cos(angle_colla_rad)
    y_colla_init = R * np.sin(angle_colla_rad)

    # Rotazione antioraria (step 2): ruoto la bobina per spostare la colla verso il nip
    angle_colla_rotated_rad = angle_colla_rad + theta
    x_colla_rotated = R * np.cos(angle_colla_rotated_rad)
    y_colla_rotated = R * np.sin(angle_colla_rotated_rad)

    # Segmento marrone = il tratto di velo che sarà tagliato
    ax.plot([x_nip - L, x_nip], [y_nip, y_nip], color="#795548", linewidth=3.0, label='Velo da tagliare (L)')

    # Colla: iniziale e posizione dopo rotazione
    ax.plot([x_colla_init], [y_colla_init], 'o', color="#e53935", markersize=8, label='Colla applicata (@90°)')
    ax.plot([x_nip], [y_nip], 'o', color="#1e88e5", markersize=8, label='Punto di NIP (fisso)')

    # Arco θ antiorario = quanto devo ruotare prima del taglio
    arc = patches.Arc((0, 0), 2*R, 2*R, angle=0,
                      theta1=90,
                      theta2=90 + theta_deg,
                      color='#ffa726', linewidth=2.5, label='Rotazione pre-taglio θ')
    ax.add_patch(arc)

    arc_theta = patches.Arc((0, 0), 0.6*R, 0.6*R, angle=0,
                            theta1=90,
                            theta2=90 + theta_deg,
                            color='blue', linewidth=1.5, linestyle='--')
    ax.add_patch(arc_theta)

    angle_label = angle_colla_rad + theta / 2
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
    ax.set_title(f"\u2728 Bobina Interattiva \u2728\nDiametro = {D:.0f} mm | Lunghezza Velo = {L:.0f} mm",
                 fontsize=13, fontweight='bold', color="#333")

    return fig, theta_deg

# Streamlit app
st.set_page_config(page_title="Bobina Interattiva", layout="centered")
st.title("🌀 Bobina Interattiva")

D = st.slider("Diametro della bobina (mm)", min_value=800, max_value=1200, value=1000, step=10)
L = st.slider("Lunghezza del velo (mm)", min_value=50, max_value=2000, value=1200, step=10)

fig, theta = draw_roll(D, L)
st.pyplot(fig, use_container_width=True)

st.markdown(f"#### θ = {theta:.2f}° → Rotazione da applicare PRIMA del taglio per far combaciare la colla con la fine del velo")
