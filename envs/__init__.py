from gymnasium.envs.registration import register

register(
    id="RealWorldEnv-v0",
    entry_point="envs.core_env:RealWorldEnv",
)