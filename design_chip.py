from stable_baselines3 import PPO
from environment import DynamicChipEnv
from power_model import estimate_power
from timing_engine import compute_timing
from router_multilayer import MultiLayerRouter
from tsv_model import assign_layers

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

GRID_SIZE = 10  # µm per grid

# ================= CUSTOM COLOR MAP =================
# Black → Yellow → Orange → Red
eda_cmap = LinearSegmentedColormap.from_list(
    "custom_heatmap",
    ["black", "yellow", "orange", "red"]
)

# ================= INIT =================
env = DynamicChipEnv()
model = PPO.load("chip_designer")

obs, _ = env.reset()
done = False

while not done:
    action, _ = model.predict(obs)
    obs, reward, done, _, _ = env.step(action)

print("\n==============================")
print("      FINAL CHIP REPORT")
print("==============================")

for block, pos in env.layout.items():
    print(f"{block:15s} -> {pos}")

# ================= METRICS =================
wire = env.total_wirelength()
area = env.width * env.height
util = len(env.layout) / area

die_area_mm2 = (env.width * GRID_SIZE * env.height * GRID_SIZE) / 1e6
wire_um = wire * GRID_SIZE

print("\n==== CHIP METRICS ====")
print(f"Die Area           : {die_area_mm2:.4f} mm²")
print(f"Utilization        : {util * 100:.2f} %")
print(f"Wirelength         : {wire_um:.2f} µm")
print(f"Estimated Delay    : {wire * 0.02:.2f} ns")

# ================= POWER =================
total_power, detail = estimate_power(env.layout)

print("\n==== POWER REPORT ====")
for b, p in detail.items():
    print(f"{b:15s} : {p:.2f} W")
print(f"Total Power        : {total_power:.2f} W")

# ================= ROUTING =================
router = MultiLayerRouter(env.width, env.height)

for src, dst in env.connections:
    if src in env.layout and dst in env.layout:
        router.route(env.layout[src], env.layout[dst])

# ================= CONGESTION =================
heat = router.congestion_map()
cong = np.max(heat)

print("\n==== CONGESTION REPORT ====")
print(f"Max Congestion Density : {cong:.2f} tracks/layer")

# ================= TIMING =================
total_delay, critical = compute_timing(env)

print("\n==== TIMING REPORT ====")
print(f"Total Delay        : {total_delay:.4f} ns")

print("\nTop Critical Paths:")
for p in critical[:5]:
    print(p)

# ================= TSV =================
layers = assign_layers(env)

print("\n==== 3D LAYER ASSIGNMENT ====")
for b, l in layers.items():
    print(f"{b:15s} -> Layer {l}")

# ================= ROUTING HEATMAP =================
plt.figure(figsize=(7,6))

norm_heat = heat / np.max(heat) if np.max(heat) != 0 else heat

plt.imshow(norm_heat, cmap=eda_cmap, origin="lower")

plt.title("Routing Congestion Heatmap", fontsize=14, fontweight='bold')
plt.xlabel("Chip Width (Grid Units)", fontsize=12)
plt.ylabel("Chip Height (Grid Units)", fontsize=12)

cbar = plt.colorbar()
cbar.set_label("Congestion Level (tracks/layer)", fontsize=11)

# Grid overlay (chip-like look)
plt.grid(color='white', linestyle='--', linewidth=0.3)

# Highlight hotspot
y, x = np.unravel_index(np.argmax(norm_heat), norm_heat.shape)
plt.scatter(x, y, color='cyan', s=60, label='Critical Hotspot')
plt.legend()

plt.tight_layout()
plt.savefig("routing_heatmap.png", dpi=300)
plt.show()

# ================= THERMAL =================
thermal = np.zeros((env.width, env.height))

for block, (x, y) in env.layout.items():
    thermal[x][y] += detail.get(block, 1.0)

plt.figure(figsize=(7,6))

norm_thermal = thermal / np.max(thermal) if np.max(thermal) != 0 else thermal

plt.imshow(norm_thermal, cmap=eda_cmap, origin="lower")

plt.title("Thermal Distribution Heatmap", fontsize=14, fontweight='bold')
plt.xlabel("Chip Width (Grid Units)", fontsize=12)
plt.ylabel("Chip Height (Grid Units)", fontsize=12)

cbar = plt.colorbar()
cbar.set_label("Temperature Intensity (Normalized)", fontsize=11)

# Grid overlay
plt.grid(color='white', linestyle='--', linewidth=0.3)

# Highlight hotspot
y, x = np.unravel_index(np.argmax(norm_thermal), norm_thermal.shape)
plt.scatter(x, y, color='cyan', s=60, label='Hotspot')
plt.legend()

plt.tight_layout()
plt.savefig("thermal_heatmap.png", dpi=300)
plt.show()