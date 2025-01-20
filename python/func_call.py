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
    {
        'type': 'function',
        'function': {
            'name': 'get_current_directory',
            'description': 'Get the current directory',
            'parameters': {
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'go_one_directory_up',
            'description': 'Go one directory up',
            'parameters': {
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'go_to_directory',
            'description': 'Go to a specific directory',
            'parameters': {
                'path': {
                    'type': 'string',
                    'description': 'The path to the directory to go to',
                },
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
    files_info = []
    for file in os.listdir('.'):
        try:
            if os.path.isfile(file):  # Only include files, not directories
                size = os.path.getsize(file)
                files_info.append({
                    'path': file,
                    'size': f"{size / 1024:.2f} KB"
                })
            else:
                files_info.append({
                    'path': file,
                    'size': 'Directory'
                })
        except (OSError, IOError):
            continue
    
    return f"Files: {files_info}"

def get_current_directory():
    return f"Current directory: {os.getcwd()}"

def go_one_directory_up():
    os.chdir('..')
    return f"Current directory: {os.getcwd()}"

def go_to_directory(path):
    os.chdir(path)
    return f"Current directory: {os.getcwd()}"

def call_tool(tool_name, tool_args):
    print(f"Calling tool {tool_name} with arguments {tool_args}")
    if tool_name == 'get_running_processes':
        return get_running_processes()
    elif tool_name == 'get_files':
        return get_files()
    elif tool_name == 'get_current_directory':
        return get_current_directory()
    elif tool_name == 'go_one_directory_up':
        return go_one_directory_up()
    elif tool_name == 'go_to_directory':
        return go_to_directory(tool_args['path'])
    else:
        return "Tool not found"

def main():
    conversation_history = [{'role': 'system', 'content': 
        'You are a computer running Linux-like operating system. ' + 
        'You can answer the user questions and perform tasks on the system. ' +
        'You can use the provided tools to perform tasks on the system. ' +
        'Use tools only when necessary. If the user request does not require a tool, ' +
        'just answer the question or perform the task without using tools.' +
        'If user says something in a conversational way, reply in the same way.'
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