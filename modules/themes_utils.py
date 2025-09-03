import matplotlib.pyplot as plt

# 🎨 Colores de marca (base)
ROSE_LEVEL_COLORS = {
    "primary": "#201e4c",    # azul oscuro
    "secondary": "#00bab3",  # turquesa
    "contrast": "#f3c300",   # amarillo
    "light_bg": "#ffffff"    # blanco puro
}

# 🎨 Paleta para las series
ROSE_LEVEL_PALETTE = [
    ROSE_LEVEL_COLORS["primary"],
    ROSE_LEVEL_COLORS["secondary"],
    ROSE_LEVEL_COLORS["contrast"],
]

ROSE_LEVEL_GRADIENT = [
    "#17677e",
    "#0e92b0",
    "#06b1b7",
    "#00bab3"
]

# Configuración global de matplotlib
plt.rcParams.update({
    # Fondo
    "figure.facecolor": ROSE_LEVEL_COLORS["light_bg"],   # exterior
    "axes.facecolor": ROSE_LEVEL_COLORS["light_bg"],    # interior

    # Textos y títulos
    "text.color": ROSE_LEVEL_COLORS["primary"],
    "axes.labelcolor": ROSE_LEVEL_COLORS["primary"],
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.titlecolor": ROSE_LEVEL_COLORS["primary"],

    # Ejes y ticks
    "xtick.color": ROSE_LEVEL_COLORS["primary"],
    "ytick.color": ROSE_LEVEL_COLORS["primary"],
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,

    # Leyenda
    "legend.frameon": False,
    "legend.fontsize": 8,

    # Grid
    "grid.color": ROSE_LEVEL_COLORS["secondary"],
    "grid.linestyle": "--",
    "grid.alpha": 0.5,

    # Estilo de líneas y colores de serie
    "lines.linewidth": 2,
    "axes.prop_cycle": plt.cycler(color=ROSE_LEVEL_GRADIENT)
})
