
# AI-based-physical-design-and-chip-design-system

An advanced # AI-based-AI-based-physical-design-and-chip-design-system for automated chip floorplanning, routing, and analysis using **Reinforcement Learning (PPO)**.

This project simulates a **mini version of industry tools like Cadence Innovus /  AlphaChip**, integrating placement, routing, congestion, timing, power, thermal, and 3D chip design in a unified pipeline.

---

#  Features

✔ Reinforcement Learning-based chip placement (PPO)
✔ Multi-layer routing (Manhattan + A* routing)
✔ Routing congestion analysis & heatmap
✔ Timing estimation (gate + interconnect delay)
✔ Power modeling
✔ Thermal heatmap generation 
✔ 3D chip stacking (TSV-based) 
✔ Dataset generator (1000+ chip designs)
✔ 2D & 3D visualization

---

#  System Overview

```
Input Design (JSON)
        ↓
AI Placement (RL - PPO)
        ↓
Routing (Multi-layer + A*)
        ↓
Congestion Analysis
        ↓
Timing Analysis
        ↓
Power Estimation
        ↓
Thermal Analysis
        ↓
3D Chip Visualization
```

---

#  Project Structure

```
├── environment.py          # RL environment (placement logic)
├── train.py               # PPO training script
├── design_chip.py         # Main execution & reporting
├── router_multilayer.py   # Routing engine
├── congestion_optimizer.py
├── timing_engine.py       # Delay calculation
├── power_model.py         # Power estimation
├── tsv_model.py           # 3D layer assignment
├── visualize_3d.py        # 3D chip visualization
├── generate_dataset.py    # Dataset generator
├── chip_input.json        # Input chip configuration
├── alpha_self_learn.py    # RL reward tuning
├── index.py               # CLI interface
```

---

#  Installation

### 1️ Clone Repository

```
git clone https://github.com/karnatikirankumarreddy234/AI-based-AI-based-physical-design-and-chip-design-system-.git
cd AI-based-AI-based-physical-design-and-chip-design-system-

### 2️ Install Dependencies

```
pip install numpy matplotlib gymnasium stable-baselines3
```

---

#  How to Run
You can design your **own chip architecture interactively** using:

```bash
python index.py
```

---

##  Input Format

The program will ask for inputs step-by-step:

### 1️ Chip Size

```text
Enter Chip Width :
Enter Chip Height:
```

---

### 2️ Number of Blocks

```text
Number of Blocks:
```

---

### 3️ Block Details

For each block, enter:

```text
Block Name
Width
Height
```

Example:

```text
Block 1 Name: CPU
Width : 4
Height: 4
```

---

### 4️ Number of Connections

```text
Number of Connections:
```

---

### 5️ Connections

Enter connections between blocks:

```text
From Block:
To Block:
```

---

#  Example 1 (Medium Design)

```text
Enter Chip Width : 25
Enter Chip Height: 25

Number of Blocks: 14
```

### Blocks

```text
CPU        4 4
GPU_CORE1  5 4
GPU_CORE2  5 4
GPU_CORE3  5 4
GPU_CORE4  5 4
L2CACHE    6 5
HBM1       4 3
HBM2       4 3
HBM3       4 3
HBM4       4 3
AI_ACCEL   4 4
DSP        3 3
IO         3 2
PCIE       3 2
```

---

### Connections (13)

```text
CPU L2CACHE
GPU_CORE1 L2CACHE
GPU_CORE2 L2CACHE
GPU_CORE3 L2CACHE
GPU_CORE4 L2CACHE
L2CACHE HBM1
L2CACHE HBM2
L2CACHE HBM3
L2CACHE HBM4
AI_ACCEL CPU
DSP CPU
IO CPU
PCIE CPU
```

---


#  Output

The system generates:

*  Floorplan layout
*  Congestion heatmap
*  Thermal heatmap
*  Timing report
*  Power report
*  3D chip visualization

---

#  Mathematical Model

### Wirelength

```
WL = Σ(|x1 - x2| + |y1 - y2|)
```

### Reward Function

```
R = -(WL + 5 × Congestion)
```

### Delay

```
D = Gate Delay + Wire Delay
```

### Power

```
P_total = Σ P_i
```

---

#  Sample Results

| Metric         | Value   |
| -------------- | ------- |
| Die Area       | 1225    |
| Utilization    | 1.47%   |
| Wirelength     | 287     |
| Delay          | 5.74 ns |
| Power          | 44.1 W  |
| Max Congestion | 10      |

---

#  Research Scope

This project can be extended into a **publishable research paper** with:

* Multi-objective RL reward (PPA optimization)
* Benchmark datasets (ISPD / ICCAD)
* Graph Neural Networks (GNN)
* RL-based routing integration

---

#  Future Improvements

* RL-based routing optimization
* Thermal-aware placement
* Real-world chip benchmarks
* Multi-agent reinforcement learning
* FPGA/ASIC backend integration

---

#  Applications

* AI-based chip design automation
* VLSI research & education
* Semiconductor optimization tools
* Smart EDA pipelines

---

#  License

This project is open-source and available 

---

#  Author

**Karnati Kiran Kumar Reddy**
B.Tech Student | AI + VLSI Enthusiast

---

# Support

If you like this project:

Star the repository
Fork it
Share it

---

#  Inspiration

Inspired by:

*  AlphaChip
* Cadence Innovus
* Synopsys ICC2

---
