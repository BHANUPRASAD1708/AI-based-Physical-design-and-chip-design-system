import json
from google import genai
from google.genai import types
from pydantic import BaseModel

class MovementDecision(BaseModel):
    macro_name: str
    delta_x: int
    delta_y: int
    target_layer: int
    reasoning: str

class OptimizationPlan(BaseModel):
    step_by_step_analysis: str
    moves: list[MovementDecision]

def optimize_congestion_with_cot(congestion_grid_data: dict) -> OptimizationPlan:
    client = genai.Client()

    prompt = f"""
    Congestion Grid Metrics:
    {json.dumps(congestion_grid_data, indent=2)}

    Perform Chain-of-Thought spatial analysis:
    1. Identify hot-spots where wire utilization exceeds 80%.
    2. Check adjacent macro bounding boxes for free routing channels.
    3. Evaluate if moving a macro to a different silicon layer relieves horizontal wire density.
    4. Provide the exact integer coordinate displacement (delta_x, delta_y) and target layer.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="You are a physical design congestion optimization assistant for 3D-ICs. Reason sequentially step-by-step before determining coordinate relocations.",
            response_mime_type="application/json",
            response_schema=OptimizationPlan,
            temperature=0.2
        )
    )

    plan = json.loads(response.text)
    print("=== CoT Congestion Reasoning ===")
    print(plan["step_by_step_analysis"])
    return plan

if __name__ == "__main__":
    sample_congestion = {
        "grid_size": [100, 100, 3],
        "hotspots": [{"layer": 0, "x_range": [20, 45], "y_range": [20, 45], "density": 0.89}],
        "macro_positions": [
            {"name": "NPU_CORE", "layer": 0, "x": 25, "y": 25, "w": 15, "h": 15},
            {"name": "DSP_0", "layer": 0, "x": 35, "y": 25, "w": 10, "h": 10}
        ]
    }
    optimize_congestion_with_cot(sample_congestion)
