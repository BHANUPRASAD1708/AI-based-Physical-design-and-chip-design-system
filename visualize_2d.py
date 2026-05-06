import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from environment import DynamicChipEnv

# ================= INIT =================
env = DynamicChipEnv()
model = PPO.load("chip_designer")

obs, _ = env.reset()
done = False

while not done:
    action, _ = model.predict(obs)
    obs, _, done, _, _ = env.step(action)

# ================= FIGURE =================
plt.figure(figsize=(9,8))
ax = plt.gca()

block_edges = {}

# ================= DRAW BLOCKS =================
for block, (x, y) in env.layout.items():
    w, h = env.blocks[block]

    rect = plt.Rectangle(
        (y, x), h, w,
        facecolor="#c9a227",
        edgecolor="black",
        linewidth=1.5
    )
    ax.add_patch(rect)

    # Only LEFT and RIGHT edges
    block_edges[block] = {
        "left":  (y, x + w/2),
        "right": (y + h, x + w/2)
    }

    ax.text(
        y + h/2, x + w/2,
        block,
        ha='center', va='center',
        fontsize=8,
        fontweight='bold'
    )

# ================= CLEAN SIDE ROUTING =================
colors = ["#7b1fa2", "#f57c00", "#388e3c", "#1976d2", "#c2185b"]

for i, (b1, b2) in enumerate(env.connections):

    if b1 in block_edges and b2 in block_edges:

        e1 = block_edges[b1]
        e2 = block_edges[b2]

        color = colors[i % len(colors)]

        # Decide direction (left → right)
        if e1["right"][0] <= e2["left"][0]:
            p1 = e1["right"]
            p2 = e2["left"]
        else:
            p1 = e1["left"]
            p2 = e2["right"]

        # If aligned → straight line
        if abs(p1[1] - p2[1]) < 2:
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                    color=color, lw=2)

        else:
            # Clean L-shape (no top routing)
            mid_x = (p1[0] + p2[0]) / 2

            ax.plot([p1[0], mid_x], [p1[1], p1[1]],
                    color=color, lw=2)

            ax.plot([mid_x, mid_x], [p1[1], p2[1]],
                    color=color, lw=2)

            ax.plot([mid_x, p2[0]], [p2[1], p2[1]],
                    color=color, lw=2)

# ================= AXIS =================
ax.set_xlim(0, env.width)
ax.set_ylim(0, env.height)

ax.set_xlabel("Chip Width (Grid Units)")
ax.set_ylabel("Chip Height (Grid Units)")

ax.set_title("2D Chip Layout with Clean Side Routing", 
             fontsize=14, fontweight='bold')

plt.grid(True, linewidth=0.4, alpha=0.4)
ax.set_aspect('equal')

plt.gca().invert_yaxis()

# ================= SAVE =================
plt.tight_layout()
plt.savefig("clean_side_routing.png", dpi=300)

plt.show()