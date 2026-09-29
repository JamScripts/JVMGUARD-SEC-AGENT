import json

from ollama import chat

from jvmguard.security.action import ActionRequest
from jvmguard.security.risk import assess_action
from jvmguard.tools.system_info import get_system_info


VERSION = "0.4.0"
MODEL = "qwen3.5:0.8b"
MAX_AGENT_STEPS = 4

SYSTEM_PROMPT = """
You are JVMGuard, a local AI security agent.

Your job is to accurately analyze AI security risks and use authorized tools
when real system information is required.

GENERAL RULES:
1. Normal questions are benign by default.
2. Do not invent attacks or malicious intent.
3. Do not invent system information.
4. Do not claim an action occurred unless an authorized tool performed it.
5. Clearly distinguish facts from assumptions.
6. Keep responses concise.

TOOL RULES:
You have access to an authorized tool called get_system_info.
Use get_system_info whenever the user asks about the current computer,
hostname, operating system, kernel, CPU information, architecture, current
system date or time, or system inspection.
Never guess these values when the tool can retrieve them.

SECURITY RULES:
Tools may only execute if JVMGuard's controller explicitly allows them.
A tool being requested by the language model does not automatically mean it is
authorized.
"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

AVAILABLE_TOOLS = {"get_system_info": get_system_info}
TOOLS = [get_system_info]


def tool_is_allowed(tool_name: str) -> bool:
    """Return whether a tool is explicitly allowlisted in v0.4."""

    return tool_name in AVAILABLE_TOOLS


def execute_tool(tool_call, user_goal: str) -> dict:
    tool_name = tool_call.function.name
    arguments = tool_call.function.arguments or {}

    action = ActionRequest(
        agent="jvmguard-agent",
        tool=tool_name,
        arguments=arguments,
        user_goal=user_goal,
        source="user",
        trust_level="trusted",
    )
    risk = assess_action(action)

    print("\n================================")
    print("      JVMGUARD INTERCEPT")
    print("================================")
    print(f"Agent:       {action.agent}")
    print(f"Tool:        {action.tool}")
    print(f"Arguments:   {action.arguments}")
    print(f"User Goal:   {action.user_goal}")
    print(f"Source:      {action.source}")
    print(f"Trust:       {action.trust_level}")
    print(f"Timestamp:   {action.timestamp}")
    print(f"Risk Score:  {risk.score}/100")
    print(f"Risk Level:  {risk.level.value}")
    print("Risk Reasons:")
    for reason in risk.reasons:
        print(f"  - {reason}")
    print("================================")

    if not tool_is_allowed(tool_name):
        print("[DECISION] BLOCK")
        print(f"[REASON] Tool is not authorized: {tool_name}")
        return {
            "status": "blocked",
            "action": action.to_dict(),
            "reason": "Tool is not authorized by JVMGuard policy.",
        }

    function_to_call = AVAILABLE_TOOLS[tool_name]
    print("[DECISION] ALLOW")
    print(f"[EXECUTING] {tool_name}")

    try:
        result = function_to_call(**arguments)
        print(f"[SUCCESS] {tool_name}")
        return {
            "status": "success",
            "action": action.to_dict(),
            "result": result,
        }
    except Exception as error:
        print(f"[ERROR] {tool_name}: {error}")
        return {
            "status": "error",
            "action": action.to_dict(),
            "error": str(error),
        }


def process_message(user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})

    for _ in range(MAX_AGENT_STEPS):
        response = chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            think=False,
        )
        messages.append(response.message)
        tool_calls = response.message.tool_calls

        if not tool_calls:
            return response.message.content

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_result = execute_tool(tool_call, user_goal=user_input)
            messages.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": json.dumps(tool_result),
                }
            )

    return (
        "JVMGuard stopped the agent loop because the maximum number of tool "
        "steps was reached."
    )


def main() -> None:
    print("\n================================")
    print(f"        JVMGuard v{VERSION}")
    print("================================")
    print(f"Model:   {MODEL}")
    print("Backend: Ollama")
    print("Tools:   get_system_info")
    print("Security: Action interception + allowlist")
    print("Type 'exit' to quit.")

    while True:
        print()
        user_input = input("YOU > ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("\nJVMGuard stopped.")
            break

        try:
            answer = process_message(user_input)
            print(f"\nJVMGUARD > {answer}")
        except Exception as error:
            print(f"\n[JVMGUARD ERROR] {error}")


if __name__ == "__main__":
    main()
