import numpy as np

def compute_congestion(router):
    return np.max(router.congestion_map())


def optimize_layout(env, router):
    congestion = compute_congestion(router)

    if congestion > 5:
        # simple spreading heuristic
        for block in env.layout:
            x, y = env.layout[block]
            env.layout[block] = (x+1 if x+1 < env.width else x,
                                 y+1 if y+1 < env.height else y)

    return env.layout