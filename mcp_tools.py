# mcp_tools.py
# D:\AI\RAG_Project\scripts\mcp_tools.py

import sys

# ===== Dummy MCP Tools Example =====
def calculator_tool(expression):
    try:
        return eval(expression)
    except Exception as e:
        return f"Error: {e}"

def file_reader_tool(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def search_tool(query):
    # Replace this with your actual search function
    return f"Search results for '{query}'"

# ===== Interactive loop / command-line friendly =====
while True:
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        sys.argv = [sys.argv[0]]  # reset arguments
    else:
        user_input = input("Enter MCP command (or 'exit' to quit): ")

    if user_input.lower() == "exit":
        print("Exiting MCP Tools...")
        break

    # Simple command parsing example
    if user_input.startswith("calc "):
        expr = user_input.replace("calc ", "")
        print("Result:", calculator_tool(expr))
    elif user_input.startswith("read "):
        path = user_input.replace("read ", "")
        print(file_reader_tool(path))
    elif user_input.startswith("search "):
        q = user_input.replace("search ", "")
        print(search_tool(q))
    else:
        print("Unknown command. Use 'calc', 'read', or 'search'.")
