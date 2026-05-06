POWER_TABLE = {
    "CPU": 2.5,
    "GPU": 5.0,
    "GPU_CORE": 4.5,
    "L2CACHE": 1.2,
    "HBM": 3.0,
    "AI_ACCEL": 4.0,
    "DSP": 1.8,
    "IO": 0.8,
    "PCIE": 1.0
}

def estimate_power(layout):

    total_power = 0
    report = {}

    for name in layout:
        for key, val in POWER_TABLE.items():
            if key in name.upper():
                report[name] = val
                total_power += val
                break
        else:
            report[name] = 1.0
            total_power += 1.0

    return total_power, report