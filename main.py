import openai
import os
import sqlite3
import json


API_KEY = os.getenv("OPENAI_API_KEY", "NA")
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo")

Client = openai.OpenAI(api_key=API_KEY)

conn = sqlite3.connect(":memory:")

conn.execute(
    """
CREATE TABLE IF NOT EXISTS todo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    status TEXT NOT NULL
)
"""
)
conn.commit()


def create_task(task):
    try:
        conn.execute("INSERT INTO todo (task, status) VALUES (?, ?)", (task, "todo"))
        conn.commit()
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "message": str(e)}


def get_tasks():
    try:
        tasks = conn.execute("SELECT * FROM todo").fetchall()
        return {"result": "ok", "tasks": tasks}
    except Exception as e:
        return {"result": "error", "message": str(e)}


def update_task(id, status):
    try:
        conn.execute("UPDATE todo SET status = ? WHERE id = ?", (status, id))
        conn.commit()
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "message": str(e)}


def delete_task(id):
    try:
        conn.execute("DELETE FROM todo WHERE id = ?", (id,))
        conn.commit()
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "message": str(e)}


def delete_all_done_tasks():
    try:
        conn.execute("DELETE FROM todo WHERE status = ?", ("done",))
        conn.commit()
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "message": str(e)}


Tools = [
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "Get all tasks",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Task's content",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {"type": "number", "description": "Task id"},
                    "status": {
                        "type": "string",
                        "description": "Task status, todo or done",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {"id": {"type": "number", "description": "Task id"}},
            },
        },
    },
]


def eval_tools(tools):
    result = []
    for tool in tools:
        fun = tool.function
        if fun.name == "create_task":
            arguments = json.loads(fun.arguments)
            result.append(create_task(arguments["task"]))
        elif fun.name == "get_tasks":
            result.append(get_tasks())
        elif fun.name == "update_task":
            arguments = json.loads(fun.arguments)
            result.append(update_task(arguments["id"], arguments["status"]))
        elif fun.name == "delete_task":
            arguments = json.loads(fun.arguments)
            result.append(delete_task(arguments["id"]))
        else:
            fun_name = fun.name
            result.append(
                {"result": "error", "message": f"Unknown function for {fun_name}"}
            )

    if len(result) > 0:
        print("Tool:")
        print(result)

    return result


def handler_llm_response(messages, stream):
    tools = []
    content = ""
    print("Assistant:")
    for chunk in stream:
        if len(chunk.choices) == 0:
            break
        delta = chunk.choices[0].delta
        print(delta.content, end="")
        content += delta.content
        if len(delta.tool_calls) == 0:
            pass
        else:
            if len(tools) == 0:
                tools = delta.tool_calls
            else:
                for i, tool_call in enumerate(delta.tool_calls):
                    if tools[i] == None:
                        tools[i] = tool_call
                    else:
                        argument_delta = tool_call["function"]["arguments"]
                        tools[i]["function"]["arguments"].extend(argument_delta)
    if len(tools) == 0:
        messages.append({"role": "assistant", "content": content})
    else:
        tools_json = [tool.json() for tool in tools]
        messages.append(
            {"role": "assistant", "content": content, "tool_call": tools_json}
        )

    print()

    return eval_tools(tools)


def chat_completions(messages):
    stream = Client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=Tools,
        stream=True,
    )

    tool_result = handler_llm_response(messages, stream)
    if len(tool_result) > 0:
        for result in tool_result:
            messages.append({"role": "tool", "content": json.dumps(result)})
        return False
    else:
        return True


def main():
    messages = [
        {"role": "system", "content": "You are a todo list assistant."},
    ]

    wait_input = True
    while True:
        if wait_input:
            user_input = input("User: ")
            messages.append({"role": "user", "content": user_input})

        wait_input = chat_completions(messages)

        print("Tasks:")
        print(get_tasks())


if __name__ == "__main__":
    main()
