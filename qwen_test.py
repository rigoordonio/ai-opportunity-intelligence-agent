import subprocess

prompt = """
Act as a Bilfinger Asset Performance Business Development Director.

Shell announced a new LNG expansion project.

Identify:
1. Opportunity Summary
2. Relevant Services
3. Recommended Action
"""

result = subprocess.run(
    ["ollama", "run", "qwen3:14b", prompt],
    capture_output=True,
    text=True
)

print(result.stdout)