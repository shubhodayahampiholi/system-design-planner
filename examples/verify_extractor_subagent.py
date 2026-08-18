from dotenv import load_dotenv

from deepagents.backends.filesystem import FilesystemBackend
from system_design_planner.agent import build_planner_agent
from system_design_planner.debug import get_final_text, print_message_trace
from system_design_planner.subagents import REFERENCE_EXTRACTOR

load_dotenv()

backend = FilesystemBackend(root_dir="knowledge_base")

agent = build_planner_agent(backend=backend, subagents=[REFERENCE_EXTRACTOR])

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": (
                "Before we design anything: delegate to your reference-extractor "
                "subagent to pull the facts on Unity Catalog governance. Then just "
                "report back what it found - don't add your own analysis yet."
            ),
        }
    ]
})

print(get_final_text(result))
print_message_trace(result)
