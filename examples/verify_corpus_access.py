from dotenv import load_dotenv

from deepagents.backends.filesystem import FilesystemBackend
from system_design_planner.agent import build_planner_agent
from system_design_planner.debug import get_final_text, print_message_trace

load_dotenv()

# root_dir scoped narrowly to knowledge_base/, not the whole project - the
# agent should only ever see the reference corpus, nothing else on disk.
backend = FilesystemBackend(root_dir="knowledge_base")

agent = build_planner_agent(backend=backend)

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": (
                "List every file in your working directory, then give a "
                "one-line summary of what each one covers."
            ),
        }
    ]
})

print(get_final_text(result))
print_message_trace(result)
