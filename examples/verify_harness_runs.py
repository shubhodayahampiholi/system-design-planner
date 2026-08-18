from dotenv import load_dotenv

from system_design_planner.agent import build_planner_agent
from system_design_planner.debug import get_final_text, print_message_trace

load_dotenv()

agent = build_planner_agent(system_prompt=None)  # bare harness, no persona

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "In one or two sentences: what tools do you currently have access to, and is there anything in your working directory right now?",
        }
    ]
})

print(get_final_text(result))
print_message_trace(result)
