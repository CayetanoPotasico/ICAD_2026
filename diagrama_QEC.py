import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ==========================================
# PARÁMETROS EDITABLES (Colores y estilo)
# ==========================================
COLOR_Z = "#56BCFC"  # Azul claro (para Z / Detecta errores X)
COLOR_X = "#FF5454"  # Rojo claro (para X / Detecta errores Z)
ALPHA_PATCH = 0.4    # Transparencia del sombreado

COLOR_DATA_QUBIT = 'darkblue'
COLOR_ANCILLA = 'black'

# Topología d=5
z_plaquettes = [
    [0, 1], [2, 3], 
    [1, 2, 6, 7], [3, 4, 8, 9], 
    [5, 6, 10, 11], [7, 8, 12, 13], 
    [11, 12, 16, 17], [13, 14, 18, 19], 
    [15, 16, 20, 21], [17, 18, 22, 23], 
    [21, 22], [23, 24]
]
x_stars = [
    [5, 10], [15, 20], 
    [0, 1, 5, 6], [2, 3, 7, 8], 
    [6, 7, 11, 12], [8, 9, 13, 14], 
    [10, 11, 15, 16], [12, 13, 17, 18], 
    [16, 17, 21, 22], [18, 19, 23, 24], 
    [4, 9], [14, 19]
]

fig, ax = plt.subplots(figsize=(10, 10))

# Coordenadas de los qubits de datos (5x5 grid)
coords = {i: (i % 5, -(i // 5)) for i in range(25)}

def draw_patch(qubits, color, label):
    pts = [coords[q] for q in qubits]
    cx = sum([p[0] for p in pts]) / len(pts)
    cy = sum([p[1] for p in pts]) / len(pts)

    # Por defecto, la ancilla va en el centro geométrico (para weight-4)
    ancilla_x, ancilla_y = cx, cy

    if len(qubits) == 4:
        pts.sort(key=lambda p: np.arctan2(p[1] - cy, p[0] - cx))
        poly = patches.Polygon(pts, closed=True, facecolor=color, alpha=ALPHA_PATCH, edgecolor='none')
        ax.add_patch(poly)
        
    elif len(qubits) == 2:
        x1, y1 = pts[0]
        x2, y2 = pts[1]
        dx, dy = x2 - x1, y2 - y1
        length = np.hypot(dx, dy)
        nx, ny = -dy / length, dx / length
        
        # Aseguramos que la normal apunte hacia AFUERA del centro de la cuadrícula (2, -2)
        if (cx + nx - 2)**2 + (cy + ny - (-2))**2 < (cx - nx - 2)**2 + (cy - ny - (-2))**2:
            nx, ny = -nx, -ny
            
        # NUEVO: Desplazar la coordenada de la ancilla 0.5 unidades hacia el exterior 
        # (al centro de la hipotética casilla adyacente)
        ancilla_x = cx + 0.5 * nx
        ancilla_y = cy + 0.5 * ny

        # BORDES EN FORMA DE SEMICÍRCULOS
        # curve_pts = []
        # for t in np.linspace(0, np.pi, 20):
        #     px = cx + 0.5 * dx * np.cos(t) + 0.5 * length * nx * np.sin(t)
        #     py = cy + 0.5 * dy * np.cos(t) + 0.5 * length * ny * np.sin(t)
        #     curve_pts.append((px, py))
        
        # poly = patches.Polygon(curve_pts, closed=True, facecolor=color, alpha=ALPHA_PATCH, edgecolor='none')
        # ax.add_patch(poly)

        # BORDES EN FORMA DE TRIÁNGULOS
        # Conectamos el qubit 1, la ancilla exterior y el qubit 2
        triangle_pts = [pts[0], (ancilla_x, ancilla_y), pts[1]]
        
        poly = patches.Polygon(triangle_pts, closed=True, facecolor=color, alpha=ALPHA_PATCH, edgecolor='none')
        ax.add_patch(poly)

    # Dibujar líneas de conexión desde la ancilla a los datos
    for p in pts:
        ax.plot([ancilla_x, p[0]], [ancilla_y, p[1]], color='gray', linestyle='--', linewidth=1.5, zorder=1)

    # Dibujar el qubit Ancilla y su etiqueta
    ax.plot(ancilla_x, ancilla_y, marker='o', color=COLOR_ANCILLA, markersize=8, zorder=3)
    ax.text(ancilla_x, ancilla_y - 0.15, label, fontsize=17, fontweight='bold', color=COLOR_ANCILLA, alpha=ALPHA_PATCH, ha='center', va='top')

# Dibujar estabilizadores
for p in z_plaquettes:
    draw_patch(p, COLOR_Z, 'Z')
for s in x_stars:
    draw_patch(s, COLOR_X, 'X')

# Dibujar Qubits de Datos
for i, (x, y) in coords.items():
    ax.plot(x, y, marker='o', markerfacecolor='white', markeredgecolor=COLOR_DATA_QUBIT, 
            markersize=20, markeredgewidth=2, zorder=4)
    ax.text(x - 0.1, y + 0.1, str(i), fontsize=17, fontweight='bold', color='midnightblue', ha='right', va='bottom')

# Ampliar un poco los márgenes para que las ancillas exteriores no se corten
ax.set_xlim(-0.7, 4.8)
ax.set_ylim(-4.8, 0.7)

ax.set_aspect('equal')
ax.axis('off')
# plt.title("Topología del Código de Superficie Rotado (d=5)", fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
# Guardarlo en formato pdf
plt.savefig("diagrama_QEC.pdf", dpi=300)
plt.show()