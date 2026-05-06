def compute_tsv_delay(z_height):
    # Through Silicon Via delay
    resistance = 0.05
    capacitance = 0.03
    return z_height * resistance * capacitance


def assign_layers(env):
    layer_map = {}
    z = 0

    for block in env.layout:
        layer_map[block] = z
        z = (z + 1) % 3  # distribute across 3 layers

    return layer_map