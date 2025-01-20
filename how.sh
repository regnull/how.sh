#!/bin/bash
set -e

# Ensure Ollama is installed
if ! command -v ollama &> /dev/null; then
  echo "Error: Ollama is not installed. Please install it from https://ollama.ai to use this script."
  exit 1
fi

# Ensure the script is called with a question
if [ "$#" -eq 0 ]; then
  echo "Usage: $0 [-y] [-m model_name] <your question>"
  exit 1
fi

# Check for the -y flag and optional model name
auto_execute=false
MODEL="llama3"
while [[ "$1" =~ ^- ]]; do
  case "$1" in
    -y)
      auto_execute=true
      shift
      ;;
    -m)
      shift
      MODEL="$1"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done
auto_execute=false
if [ "$1" == "-y" ]; then
  auto_execute=true
  shift
fi

# Combine all arguments into a single question
QUESTION="$*"

# Construct the prompt for Ollama
PROMPT="Please provide a single Linux command to accomplish 
the following task: $QUESTION. Only output the command as a single line, without quotes of any kind."

# Send the prompt to Ollama and capture the response
COMMAND=$(echo "$PROMPT" | ollama run llama3)

# Check if a command was generated
if [ -z "$COMMAND" ]; then
  echo "Error: No command was generated."
  exit 1
fi

# Display the generated command to the user
echo "Generated command: $COMMAND"

if [ "$auto_execute" = true ]; then
  echo "Executing: $COMMAND"
  eval "$COMMAND"
  exit $?
fi

# Request user confirmation
read -p "Do you want to execute this command? (y/n): " CONFIRMATION

if [[ "$CONFIRMATION" =~ ^[Yy]$ ]]; then
  echo "Executing: $COMMAND"
  eval "$COMMAND"
else
  echo "Command execution canceled."
fi
