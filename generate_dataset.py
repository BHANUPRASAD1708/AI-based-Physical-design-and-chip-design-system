import json
import random
import os
import numpy as np

os.makedirs("dataset", exist_ok=True)

BLOCK_TYPES = [
    "CPU","GPU_CORE","DSP",
    "AI_ACCEL","CACHE","HBM",
    "IO","PCIE","MEM_CTRL"
]

def generate_chip(index):

    chip_size = [random.randint(20,35), random.randint(20,35)]

    blocks = {}
    n_blocks = random.randint(6,12)

    for i in range(n_blocks):
        name = random.choice(BLOCK_TYPES) + f"_{i}"
        blocks[name] = [
            random.randint(2,6),
            random.randint(2,6)
        ]

    connections = []
    names = list(blocks.keys())

    for _ in range(n_blocks * 3):
        b1,b2 = random.sample(names,2)
        connections.append([b1,b2])

    data = {
        "chip_size": chip_size,
        "blocks": blocks,
        "connections": connections
    }

    with open(f"dataset/chip_{index}.json","w") as f:
        json.dump(data,f,indent=4)

for i in range(1000):
    generate_chip(i)

print(" 1000 Advanced Chips Generated")