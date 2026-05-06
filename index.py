import json
import subprocess

print("\n=========== AI CHIP DESIGNER ===========")

w = int(input("Enter Chip Width : "))
h = int(input("Enter Chip Height: "))

blocks = {}
n = int(input("\nNumber of Blocks: "))

for i in range(n):
    name = input(f"\nBlock {i+1} Name: ")
    bw = int(input("Width : "))
    bh = int(input("Height: "))
    blocks[name] = [bw, bh]

connections = []
c = int(input("\nNumber of Connections: "))

for i in range(c):
    b1 = input("From Block: ")
    b2 = input("To Block  : ")
    connections.append([b1, b2])

data = {
    "chip_size": [w, h],
    "blocks": blocks,
    "connections": connections
}

with open("chip_input.json", "w") as f:
    json.dump(data, f, indent=4)

print("\n🚀 Training AI...")
subprocess.run(["python", "AI_VLSI_Dynamic_Chip\train.py"])

print("\n📊 Generating Report...")
subprocess.run(["python", "AI_VLSI_Dynamic_Chip\design_chip.py"])

print("\n🧠 Showing 3D Chip...")
subprocess.run(["python", "AI_VLSI_Dynamic_Chip\visualize_3d.py"])