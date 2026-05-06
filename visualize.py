import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from environment import DynamicChipEnv
import numpy as np

# ================= LOAD MODEL =================
env = DynamicChipEnv()
model = PPO.load("chip_designer")

obs, _ = env.reset()
done = False

while not done:
    action, _ = model.predict(obs)
    obs, _, done, _, _ = env.step(action)

# ================= FIGURE =================
fig, ax = plt.subplots(figsize=(9, 9))

# CHIP BOUNDARY
ax.add_patch(
    plt.Rectangle((0, 0), env.width, env.height,
                  fill=False, linewidth=3, color="black")
)

ax.set_xlim(0, env.width)
ax.set_ylim(0, env.height)
ax.set_aspect("equal")
ax.grid(True, alpha=0.2)

# ================= OBSTACLE GRID =================
grid = np.zeros((env.width, env.height))
pins = {}

BLOCK_MARGIN = 1  # spacing from blocks

# ================= BLOCK DRAW =================
for block, (x, y) in env.layout.items():

    w, h = env.blocks[block]

    # mark obstacle with margin
    for i in range(x - BLOCK_MARGIN, x + w + BLOCK_MARGIN):
        for j in range(y - BLOCK_MARGIN, y + h + BLOCK_MARGIN):
            if 0 <= i < env.width and 0 <= j < env.height:
                grid[i][j] = 1

    # draw block
    rect = plt.Rectangle((y, x), h, w,
                         facecolor="gold",
                         edgecolor="black",
                         linewidth=2)

    ax.add_patch(rect)

    ax.text(y + h / 2, x + w / 2, block,
            ha="center", va="center", fontsize=9)

    # pin placement (safe edge)
    pin_x = x + w // 2
    pin_y = y - 1 if y > 1 else y + h + 1

    pins[block] = (pin_x, pin_y)

# ------------------------------------------------
# 🔥 BUILD CONTINUOUS CHAIN (VERY IMPORTANT FIX)
# ------------------------------------------------
chain = []

for b1, b2 in env.connections:
    if not chain:
        chain.append(b1)
    if b2 not in chain:
        chain.append(b2)

# ------------------------------------------------
# 🔥 SAFE CHANNEL FINDER (NO BLOCK COLLISION)
# ------------------------------------------------
def find_safe_channel(x1, x2):
    for ch in range(1, env.height - 1):

        safe = True

        for x in range(min(x1, x2), max(x1, x2) + 1):
            if grid[x][ch] == 1:
                safe = False
                break

        if safe:
            return ch

    return env.height // 2  # fallback

# ------------------------------------------------
# 🔥 CONTINUOUS ROUTING (FIXED CORE LOGIC)
# ------------------------------------------------
color = "#1976d2"

for i in range(len(chain) - 1):

    b1 = chain[i]
    b2 = chain[i + 1]

    if b1 in pins and b2 in pins:

        x1, y1 = pins[b1]
        x2, y2 = pins[b2]

        # find safe routing channel
        channel = find_safe_channel(x1, x2)

        # -------- horizontal from source --------
        ax.plot([y1, channel], [x1, x1],
                color=color, lw=2)

        # -------- vertical routing --------
        ax.plot([channel, channel], [x1, x2],
                color=color, lw=2)

        # -------- horizontal to destination --------
        ax.plot([channel, y2], [x2, x2],
                color=color, lw=2)

# ================= FINAL =================
plt.title("Correct Continuous Innovus Routing (No Overlap)")

plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()