from ollama import chat, ChatResponse
import psutil
import os
tools=[
    {
        'type': 'function',
        'function': {
            'name': 'get_running_processes',
            'description': 'Get the current running processes on the system',
            'parameters': {
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_files',
            'description': 'Get the list of files in the current directory',
            'parameters': {
            },
        },
    },
]

def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            process_info = proc.info
            processes.append({
                'pid': process_info['pid'],
                'name': process_info['name'],
                'status': process_info['status']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return f"Running processes: {processes}"

def get_files():
    files = []
    for file in os.listdir():
        files.append(file)
    return f"Files: {files}"

def call_tool(tool_name, tool_args):
    print(f"Calling tool {tool_name} with arguments {tool_args}")
    if tool_name == 'get_running_processes':
        return get_running_processes()
    elif tool_name == 'get_files':
        return get_files()
    else:
        return "Tool not found"

def main():
    conversation_history = [{'role': 'system', 'content': 
        'You are a helpful assistant. You can use the get_running_processes tool to ' + 
        'get the current running processes on the system.' +
        'Call this tool only when asked to get the current running processes on the system.' +
        'Do not call this tool unless asked. If the user provides a message that has nothing to ' +
        'do with the current running processes, do not call this tool, but answer the user\'s question.'
    }]
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        conversation_history.append({'role': 'user', 'content': user_input})

        response: ChatResponse = chat(
            'llama3.1',
            messages=conversation_history,
            tools=tools
        )

        while response['message'].get('tool_calls'):
            tool_call = response['message']['tool_calls'][0]
            tool_result = call_tool(tool_call['function']['name'], tool_call['function']['arguments'])
            # print(f"Tool result: {tool_result}")
            conversation_history.append({'role': 'tool', 'content': tool_result})
            response = chat(
                'llama3.1',
                messages=conversation_history,
                tools=tools
            )

        conversation_history.append({'role': 'assistant', 'content': response['message']['content']})
        print(f"LLaMA 3.1: {response['message']['content']}")

if __name__ == "__main__":
    main()

'''
response = ollama.chat(
    model='llama3.1',
    messages=[{'role': 'user', 'content':
        'What is the weather in Toronto?'}],

		# provide a weather checking tool to the model
)

print(response['message']['tool_calls'])
'''