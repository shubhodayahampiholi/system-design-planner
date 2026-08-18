from dotenv import load_dotenv

from system_design_planner.agent import build_planner_agent
from system_design_planner.debug import get_final_text, print_message_trace

load_dotenv()

agent = build_planner_agent()  # default PLANNER_SYSTEM_PROMPT

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "I need an AI architecture for my Azure + Databricks estate. Where do we start?",
        }
    ]
})

print(get_final_text(result))
print_message_trace(result)
