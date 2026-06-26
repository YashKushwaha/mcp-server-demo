import json

# ---- pretend MCP tools (replace with real MCP calls) ----
def call_tool(name, args):
    if name == "echo":
        return args["text"]

    if name == "reverse":
        return args["text"][::-1]

    if name == "random_number":
        import random
        return random.randint(1, 10)

    if name == "current_time":
        from datetime import datetime
        return datetime.now().isoformat()

    if name == "save_note":
        with open("notes.txt", "a") as f:
            f.write(args["text"] + "\n")
        return "saved"

    raise ValueError(f"Unknown tool: {name}")


# ---- fake LLM call (replace with real API call) ----
def llm(messages, tools):
    """
    Replace this with OpenAI / other LLM API call.
    Must return either:
    - {"type": "tool", "name": "...", "args": {...}}
    - {"type": "final", "content": "..."}
    """
    user_input = messages[-1]["content"]

    # very naive routing logic (for demo only)
    if "log" in user_input:
        return {
            "type": "tool",
            "name": "save_note",
            "args": {"text": user_input}
        }

    if "reverse" in user_input:
        return {
            "type": "tool",
            "name": "reverse",
            "args": {"text": user_input}
        }

    if "time" in user_input:
        return {
            "type": "tool",
            "name": "current_time",
            "args": {}
        }

    if "random" in user_input:
        return {
            "type": "tool",
            "name": "random_number",
            "args": {}
        }

    return {
        "type": "final",
        "content": f"I understood: {user_input}"
    }


# ---- MCP agent loop ----
def run_agent():
    messages = []

    while True:
        user = input("PYTHON> ")
        messages.append({"role": "user", "content": user})

        while True:
            response = llm(messages, tools=None)

            # TOOL CALL
            if response["type"] == "tool":
                result = call_tool(
                    response["name"],
                    response.get("args", {})
                )

                # feed tool result back into context
                messages.append({
                    "role": "tool",
                    "content": str(result)
                })

            # FINAL ANSWER
            else:
                print(response["content"])
                messages.append({
                    "role": "assistant",
                    "content": response["content"]
                })
                break


if __name__ == "__main__":
    run_agent()