from dotenv import load_dotenv

from system_design_planner.agent import build_planner_agent
from system_design_planner.debug import get_final_text, print_message_trace
from system_design_planner.tools import check_current_standards

load_dotenv()

agent = build_planner_agent(tools=[check_current_standards])

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": (
                "Use check_current_standards to verify: is 'Microsoft Foundry' "
                "still the current name for what used to be called 'Azure AI "
                "Foundry', as of today? Just report what you find."
            ),
        }
    ]
})

print(get_final_text(result))
print_message_trace(result)
