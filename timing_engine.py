import math

# Gate delay model (simplified Elmore delay)
def gate_delay(load_cap, drive_strength=1.0):
    R = 1.0 / drive_strength
    C = load_cap
    return R * C


def interconnect_delay(length, metal_layer=1):
    # Higher metal → lower resistance
    resistance = 0.08 / metal_layer
    capacitance = 0.02 * metal_layer
    return length * resistance * capacitance


def compute_timing(env):
    
    total_delay = 0
    critical_path = []

    for (src, dst) in env.connections:

        # ✅ Skip missing blocks
        if src not in env.layout or dst not in env.layout:
            print(f"⚠ Timing skip ({src},{dst}) - block missing")
            continue

        x1, y1 = env.layout[src]
        x2, y2 = env.layout[dst]

        length = abs(x1-x2) + abs(y1-y2)

        wire_d = interconnect_delay(length, metal_layer=2)
        gate_d = gate_delay(load_cap=0.5)

        path_delay = wire_d + gate_d
        total_delay += path_delay

        critical_path.append((src, dst, round(path_delay,4)))

    return round(total_delay,4), critical_path
