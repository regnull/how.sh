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

# Combine all arguments into a single question
QUESTION="$*"

# Construct the prompt for Ollama
PROMPT="Please provide a single Linux command to accomplish 
the following task: $QUESTION. Only output the command as a single line, without quotes of any kind."

# Send the prompt to Ollama and capture the response
COMMAND=$(echo "$PROMPT" | ollama run $MODEL)

# Check if a command was generated
if [ -z "$COMMAND" ]; then
  echo "Error: No command was generated."
  exit 1
fi


while true; do
  echo "Generated command: $COMMAND"

  if [ "$auto_execute" = true ]; then
    echo "Executing: $COMMAND"
    eval "$COMMAND"
    exit $?
  fi

  # Request user confirmation
  read -p "Execute (e for explain)? (y/n/e): " CONFIRMATION

  if [[ "$CONFIRMATION" =~ ^[Yy]$ ]]; then
    echo "Executing: $COMMAND"
    eval "$COMMAND"
    exit $?
  elif [[ "$CONFIRMATION" =~ ^[Ee]$ ]]; then
    PROMPT="Please explain what does the following command do.
    If it's a sequence of commands, explain each command.
    Output plain text, no markdown.
    The command is: $COMMAND"

    EXPLANATION=$(echo "$PROMPT" | ollama run $MODEL)
    echo "$EXPLANATION"
    echo ""
  else
    echo "Command execution canceled."
    exit 1
  fi
done
