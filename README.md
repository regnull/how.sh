# how.sh - Create and execute shell commands using Ollama

## Use at your own risk

This script is experimental and may not work as expected. Use at your own risk.

## Prerequisites

ollama must be installed. You can install it from https://ollama.ai

You might also want to pre-load the models you want to use:

```bash
$ ollama run llama3
```

how.sh uses llama3 by default, but you can use [any other model supported by ollama](https://ollama.ai/library).

## Usage

```bash
$ ./how.sh find and delete files older than 30 days
Generated command: find . -type f -mtime +30 -exec rm {} \;
Do you want to execute this command? (y/n):
```

or, if you feel adventurous:

```bash
$ ./how.sh -y "find and delete files older than 30 days"
```

You can specify the model to use with the `-m` flag.

```bash
$ ./how.sh -y -m llama3 "find and delete files older than 30 days"
```

## Installation

Just download the script and run it. If you want to can add an alias:

```bash
alias how="~/path/to/how.sh"
```

## More examples

```bash
$ ./how.sh find 10 biggest files in a directory
Generated command: find . -type f -wholename './*' | sort -n -k5 | head -n 10
```

```bash
$ ./how.sh find my external ip address
Generated command: curl ifconfig.me
```

```bash
$ ./how.sh cowsay a joke
Generated command: cowsay -f vader "Why was the math book sad? Because it had too many problems."
Do you want to execute this command? (y/n): y
Executing: cowsay -f vader "Why was the math book sad? Because it had too many problems."
 _______________________________________
/ Why was the math book sad? Because it \
\ had too many problems.                /
 ---------------------------------------
        \    ,-^-.
         \   !oYo!
          \ /./=\.\______
               ##        )\/\
                ||-----w||
                ||      ||

               Cowth Vader
```
