"""ADK agent module exposing the sustainable-code skill as a root_agent.

AgentEvaluator looks for `root_agent` or `get_agent_async` in the module
passed to `agent_module`.
"""

from pathlib import Path

from google.adk import Agent
from google.adk.skills import load_skill_from_dir

_SKILL_DIR = Path(__file__).parent.parent.parent / "skills" / "sustainable-code"

_skill = load_skill_from_dir(str(_SKILL_DIR))

root_agent = Agent(
    model="gemini-3.8-flash",
    name="sustainable_code_evaluator",
    instruction=_skill.instructions,
)
