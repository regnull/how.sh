# how.sh - Create and execute shell commands using Ollama

## Prerequisites

ollama must be installed. You can install it from https://ollama.ai

## Usage

```bash
./how.sh find and delete files older than 30 days
Generated command: find . -type f -mtime +30 -exec rm {} \;
Do you want to execute this command? (y/n):
```

or, if you feel adventurous:

```bash
./how.sh -y "find and delete files older than 30 days"
```

You can specify the model to use with the `-m` flag.

```bash
./how.sh -y -m llama3 "find and delete files older than 30 days"
```

## Installation

Just download the script and run it. If you want to can add an alias:

```bash
alias how="~/path/to/how.sh"
```

## More examples

```bash
./how.sh find 10 biggest files in a directory
Generated command: find . -type f -wholename './*' | sort -n -k5 | head -n 10
```

```bash
./how.sh find my external ip address
Generated command: curl ifconfig.me
```

```bash
./how.sh cowsay hello
Generated command: cowsay -f tux "hello"
```
