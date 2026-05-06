from stable_baselines3 import PPO
from environment import DynamicChipEnv

print("\n🚀 Training AI on Current chip_input.json ...")

env = DynamicChipEnv()

model = PPO(
    "MlpPolicy",
    env,
    learning_rate=2e-4,
    n_steps=1024,
    batch_size=128,
    gamma=0.99,
    verbose=1
)

model.learn(total_timesteps=120000)

model.save("chip_designer")

print("\n✅ AI Training Complete")