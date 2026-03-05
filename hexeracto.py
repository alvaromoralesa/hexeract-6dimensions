import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
import itertools

# Fondo oscuro absoluto para contraste de neones
plt.style.use('dark_background')

# Generar 64 vértices del hexeracto (hipercubo 6D)
vertices = np.array(list(itertools.product([-1, 1], repeat=6)), dtype=float)

# Encontrar aristas
edges = []
for i in range(len(vertices)):
    for j in range(i + 1, len(vertices)):
        if np.sum(vertices[i] != vertices[j]) == 1:
            edges.append((i, j))
edges = np.array(edges)

def rotation_matrix(dim, plane, angle):
    """ Genera matriz de rotación N-dimensional pura """
    R = np.eye(dim)
    i, j = plane
    c, s = np.cos(angle), np.sin(angle)
    R[i, i] = c; R[i, j] = -s
    R[j, i] = s; R[j, j] = c
    return R

def project_vertices(v_rotated, focal_length=3.5):
    """ Proyección prospectiva vectorizada de N-D a 2D """
    proj = v_rotated.copy()
    dim = proj.shape[1]
    while dim > 2:
        depth = proj[:, dim - 1]
        w = focal_length / np.maximum(1e-5, focal_length + depth)
        proj = proj[:, :dim-1] * w[:, np.newaxis]
        dim -= 1
    return proj

fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax.set_facecolor('black')
ax.axis('off')

# Límite de la cámara
lim = 4.2
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim * 0.8, lim * 1.2)  # Desplazado para hacer espacio al reflejo

# --- Colecciones para el efecto Neon Bloom / Glow ---
# Reflejos (zorder bajo para estar al fondo)
ref_glow2_col = LineCollection([], linewidths=12, alpha=0.03, zorder=1)
ref_glow1_col = LineCollection([], linewidths=5, alpha=0.05, zorder=2)
ref_core_col = LineCollection([], linewidths=1.5, alpha=0.15, zorder=3)
ax.add_collection(ref_glow2_col)
ax.add_collection(ref_glow1_col)
ax.add_collection(ref_core_col)

# Líneas del objeto principal (varias capas para simular bloom real)
glow3_col = LineCollection([], linewidths=20, alpha=0.03, zorder=5)
glow2_col = LineCollection([], linewidths=10, alpha=0.08, zorder=6)
glow1_col = LineCollection([], linewidths=4, alpha=0.2, zorder=7)
core_col = LineCollection([], linewidths=1.2, alpha=0.9, zorder=8)

ax.add_collection(glow3_col)
ax.add_collection(glow2_col)
ax.add_collection(glow1_col)
ax.add_collection(core_col)

# Vértices (Halo y Núcleo)
scatter_glow = ax.scatter([], [], s=120, alpha=0.2, zorder=9)
scatter_core = ax.scatter([], [], s=15, c='white', zorder=10)

def project_3d_to_2d(pts, focal_length=3.5):
    pts = np.array(pts)
    depth = pts[..., 2]
    w = focal_length / np.maximum(1e-5, focal_length + depth)
    p2d = pts[..., :2] * w[..., np.newaxis]
    return p2d

# Suelo (Grid) tipo Tron/Synthwave
floor_lines = []
for x in np.linspace(-6, 6, 25):
    floor_lines.append([(x, -2.0, -6), (x, -2.0, 6)])
for z in np.linspace(-6, 6, 25):
    floor_lines.append([(-6, -2.0, z), (6, -2.0, z)])

floor_lines_2d = [project_3d_to_2d(l) for l in floor_lines]
# Gradiente al suelo, para que el horizonte se difumine
floor_colors = np.zeros((len(floor_lines_2d), 4))
floor_colors[:, 0] = 0.8 # Violeta oscuro
floor_colors[:, 1] = 0.0
floor_colors[:, 2] = 1.0
floor_colors[:, 3] = 0.15 # Semitransparente

floor_col = LineCollection(floor_lines_2d, colors=floor_colors, linewidths=0.6, zorder=0)
ax.add_collection(floor_col)

def get_neon_colors(depths):
    """ Gradiente de color vectorizado: Cyan -> Pink -> Deep Purple basado en profundidad """
    d_min = depths.min()
    d_max = depths.max()
    t = (depths - d_min) / (d_max - d_min) if d_max > d_min else np.full_like(depths, 0.5)
    
    colors = np.zeros((len(t), 4))
    
    mask = t > 0.5
    # Distantes (t > 0.5): Rosa a Púrpura
    u_high = (t[mask] - 0.5) * 2.0
    colors[mask, 0] = 1.0 - 0.7 * u_high # R
    colors[mask, 1] = 0.0                # G
    colors[mask, 2] = 1.0 - 0.4 * u_high # B
    
    # Cercanos (t <= 0.5): Cyan a Rosa
    not_mask = ~mask
    u_low = t[not_mask] * 2.0
    colors[not_mask, 0] = u_low          # R
    colors[not_mask, 1] = 1.0 - u_low    # G
    colors[not_mask, 2] = 1.0            # B
    
    # Efecto de difuminado en profundidad superior 
    colors[:, 3] = 1.0 - 0.6 * t 
    return colors

def update(frame):
    # Rotaciones multiparamétricas suaves en varias dimensiones a la vez
    angles = [
        frame * 0.015,  # Planto X-Y
        frame * 0.022,  # Plano Y-Z
        frame * 0.011,  # 3era a 4ta dimension
        frame * 0.018,  # 4ta a 5ta
        frame * 0.009,  # 5ta a 6ta
        frame * 0.025   # Rotación cruzada extrema
    ]
    
    # Matriz de rotación combinada 6D
    R_total = np.eye(6)
    R_total = R_total @ rotation_matrix(6, (0, 1), angles[0])
    R_total = R_total @ rotation_matrix(6, (1, 2), angles[1])
    R_total = R_total @ rotation_matrix(6, (2, 3), angles[2])
    R_total = R_total @ rotation_matrix(6, (3, 4), angles[3])
    R_total = R_total @ rotation_matrix(6, (4, 5), angles[4])
    R_total = R_total @ rotation_matrix(6, (0, 5), angles[5])
    
    # Rotación principal
    v_rot = np.dot(vertices, R_total.T)
    
    # Calcular promedios desde dimensiones 4D, 5D, 6D para colorear profundidad
    vertex_depths = np.mean(v_rot[:, 3:], axis=1)
    
    # ---- Proyección Principal ----
    p2d = project_vertices(v_rot, focal_length=3.5)
    
    # Segmentos de línea central
    segs = np.zeros((len(edges), 2, 2))
    segs[:, 0, :] = p2d[edges[:, 0]]
    segs[:, 1, :] = p2d[edges[:, 1]]
    
    # Colores interpolando valores de los vértices conectados
    edge_depths = (vertex_depths[edges[:, 0]] + vertex_depths[edges[:, 1]]) / 2.0
    edge_colors = get_neon_colors(edge_depths)
    
    # Núcleo más brillante
    core_colors = edge_colors.copy()
    core_colors[:, :3] = core_colors[:, :3] * 0.3 + 0.7 
    core_colors[:, 3] = np.clip(core_colors[:, 3] * 1.5, 0, 1) # Aumentar Alpha
    
    # Aplicar a las capas de "glow" (Bloom emulado)
    glow3_col.set_segments(segs)
    glow3_col.set_edgecolors(edge_colors)
    
    glow2_col.set_segments(segs)
    glow2_col.set_edgecolors(edge_colors)
    
    glow1_col.set_segments(segs)
    glow1_col.set_edgecolors(edge_colors)
    
    core_col.set_segments(segs)
    core_col.set_edgecolors(core_colors)
    
    # Vértices (Puntos de anclaje)
    v_colors = get_neon_colors(vertex_depths)
    scatter_glow.set_offsets(p2d)
    scatter_glow.set_color(v_colors)
    scatter_core.set_offsets(p2d)
    
    # ---- Reflejo de Suelo con RTX simulado ----
    # Capturar coordenadas 3D para reflejar en el suelo correctamente
    dim = 6
    v_ref = v_rot.copy()
    fl = 3.5
    while dim > 3: # Proyectamos desde 6D hasta llegar a 3D nativo (X, Y, Z)
        d = v_ref[:, dim - 1]
        w = fl / np.maximum(1e-5, fl + d)
        v_ref = v_ref[:, :dim-1] * w[:, np.newaxis]
        dim -= 1
        
    # Aplicar espejo en Y sobre un "suelo" de neón
    floor_y = -2.0
    v_ref[:, 1] = floor_y - (v_ref[:, 1] - floor_y)
    
    # Completar proyección final desde 3D a la cámara 2D
    d = v_ref[:, 2]
    w = fl / np.maximum(1e-5, fl + d)
    p2d_ref = v_ref[:, :2] * w[:, np.newaxis]
    
    # Construir segmentos de la reflexión
    segs_ref = np.zeros((len(edges), 2, 2))
    segs_ref[:, 0, :] = p2d_ref[edges[:, 0]]
    segs_ref[:, 1, :] = p2d_ref[edges[:, 1]]
    
    # Coloreado del reflejo (Corrimiento de espectro y transparencia real)
    ref_colors = edge_colors.copy()
    ref_colors[:, 0] *= 0.3 # Bajar rojo a tope
    ref_colors[:, 2] = np.clip(ref_colors[:, 2] * 1.5, 0, 1) # Subir brillo azul
    ref_colors[:, 3] *= 0.35 # Mucha transparencia por pérdida especular
    
    ref_glow2_col.set_segments(segs_ref)
    ref_glow2_col.set_edgecolors(ref_colors)
    
    ref_glow1_col.set_segments(segs_ref)
    ref_glow1_col.set_edgecolors(ref_colors)
    
    ref_core_col.set_segments(segs_ref)
    ref_colors_core = ref_colors.copy()
    ref_colors_core[:, 3] = np.clip(ref_colors_core[:, 3] * 1.5, 0, 1) # Núcleo un poco mas firme
    ref_core_col.set_edgecolors(ref_colors_core)
    
    return (glow3_col, glow2_col, glow1_col, core_col, 
            scatter_glow, scatter_core, 
            ref_glow2_col, ref_glow1_col, ref_core_col)

# Renderizado asíncrono y multi-hilo no es trivial en matplotlib, pero:
# Reducimos interval a 16ms (aprox 60 FPS) ya que el i7 12700 tritura este código vectorizado.
ani = animation.FuncAnimation(fig, update, frames=1000, interval=16, blit=True)

plt.tight_layout()
plt.show()
