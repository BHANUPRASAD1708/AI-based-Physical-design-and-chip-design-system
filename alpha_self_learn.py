import numpy as np

def cluster_bonus(env):
    bonus = 0
    for b1,b2 in env.connections:
        if b1 in env.layout and b2 in env.layout:
            x1,y1 = env.layout[b1]
            x2,y2 = env.layout[b2]
            bonus -= abs(x1-x2)+abs(y1-y2)
    return bonus

def reinforcement_update(env, router):

    congestion = np.max(router.congestion_map())
    wire = env.total_wirelength()

    reward = -(2 * wire + 20 * congestion)
    reward += 0.1 * cluster_bonus(env)

    return reward