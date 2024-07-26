# Run llama-api-server.wasm
```bash
wasmedge --dir .:. --nn-preload default:GGML:AUTO:Llama-3-Groq-8B-Tool-Use-Q5_K_M.gguf \
llama-api-server.wasm \
--prompt-template groq-llama3-tool  --log-all \
--ctx-size 2048 \
--model-name llama3
```

# Set BASE_URL & MODEL_NAME
```bash
export OPENAI_MODEL_NAME="llama3"
export OPENAI_BASE_URL="http://127.0.0.1:8080/v1"
```

# Install dependencies & Run
```bash
pip install -r requirements.txt
python main.py
```

# Example
```
User: hello
Assistant:
Hi, I can help you with that. What would you like to do?

Current Tasks:
{'result': 'ok', 'tasks': []}

User: 1+1=?
Assistant:
I'm sorry, but I don't have the capability to perform mathematical calculations. However, if you need help with tasks or managing your to-do list, feel free to let me know!

Current Tasks:
{'result': 'ok', 'tasks': []}

User: Help me to write down it I'm going to fix a bug
Assistant:
Sure, I can help with that. Would you like me to add this task to your list?

Current Tasks:
{'result': 'ok', 'tasks': []}

User: going to fix a bug
Assistant:
<tool_call>
{"id": 0, "name": "create_task", "arguments": {"task": "going to fix a bug"}}
</tool_call>
Tool:
[{'result': 'ok'}]

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'todo')]}

Assistant:
I've added "going to fix a bug" to your task list. Is there anything else you'd like to do?

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'todo')]}

User: Oh, make a note for me that I'm going to modify a Readme
Assistant:
<tool_call>
{"id": 0, "name": "create_task", "arguments": {"task": "going to modify a Readme"}}
</tool_call>
Tool:
[{'result': 'ok'}]

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'todo'), (2, 'going to modify a Readme', 'todo')]}

Assistant:
I've added "going to modify a Readme" to your task list. Do you need help with anything else?

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'todo'), (2, 'going to modify a Readme', 'todo')]}

User: 
Assistant:
Do you have any tasks that need updating or deleting?

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'todo'), (2, 'going to modify a Readme', 'todo')]}

User: Now I have many unfinished tasks
Assistant:
<tool_call>
{"id": 0, "name": "get_tasks", "arguments": {}}
</tool_call>
Tool:
[{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'todo'), (2, 'going to modify a Readme', 'todo')]}]

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'todo'), (2, 'going to modify a Readme', 'todo')]}

Assistant:
You have the following tasks:
1. going to fix a bug (todo)
2. going to modify a Readme (todo)

Would you like to update or delete any of these?

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'todo'), (2, 'going to modify a Readme', 'todo')]}

User: I have finished the task of fixing the bug
Assistant:
<tool_call>
{"id": 0, "name": "update_task", "arguments": {"id": 1, "status": "done"}}
</tool_call>
Tool:
[{'result': 'ok'}]

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'done'), (2, 'going to modify a Readme', 'todo')]}

Assistant:
I've updated the status of "going to fix a bug" as done. Anything else you need assistance with?

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'done'), (2, 'going to modify a Readme', 'todo')]}

User: Now I have many unfinished tasks
Assistant:
<tool_call>
{"id": 0, "name": "get_tasks", "arguments": {}}
</tool_call>
Tool:
[{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'done'), (2, 'going to modify a Readme', 'todo')]}]

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'done'), (2, 'going to modify a Readme', 'todo')]}

Assistant:
You still have the following tasks:
1. going to fix a bug (done)
2. going to modify a Readme (todo)
Do you want to delete any task or create new ones?

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'done'), (2, 'going to modify a Readme', 'todo')]}

User: I want to know how many unfinished tasks I have just answer me the number
Assistant:
<tool_call>
{"id": 0, "name": "get_tasks", "arguments": {}}
</tool_call>
Tool:
[{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'done'), (2, 'going to modify a Readme', 'todo')]}]

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'done'), (2, 'going to modify a Readme', 'todo')]}

Assistant:
You have 1 unfinished task.

Current Tasks:
{'result': 'ok', 'tasks': [(1, 'going to fix a bug', 'done'), (2, 'going to modify a Readme', 'todo')]}

User: Delete a completed task
Assistant:
<tool_call>
{"id": 0, "name": "delete_task", "arguments": {"id": 1}}
</tool_call>
Tool:
[{'result': 'ok'}]

Current Tasks:
{'result': 'ok', 'tasks': [(2, 'going to modify a Readme', 'todo')]}

Assistant:
I've deleted the completed task "going to fix a bug". Now, you have 0 unfinished tasks. Anything else I can assist you with?

Current Tasks:
{'result': 'ok', 'tasks': [(2, 'going to modify a Readme', 'todo')]}

User: good
Assistant:
You're welcome! If you need any more help, feel free to ask. Have a great day!

Current Tasks:
{'result': 'ok', 'tasks': [(2, 'going to modify a Readme', 'todo')]}

User: 
```