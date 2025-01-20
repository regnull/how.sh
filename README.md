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
Execute (e for explain)? (y/n/e):
```

If you enter `e`, the script will explain what the command does:

```bash
./how.sh find and delete files older than 30 days
Generated command: find . -type f -mtime +30 -exec rm {} \;
Execute (e for explain)? (y/n/e): e
This command finds files in the current directory and all its subdirectories that are older than 30 days and deletes them.

Here's a breakdown of what each part of the command does:

* `find`: This is the command to search for files.
* `.`, the current directory: The dot at the beginning of the command tells find to start searching in the current directory.
* `-type f`: This option tells find to only consider files, not directories or other types of files.
* `-mtime +30`: This option tells find to only consider files that are older than 30 days. The `+` sign is used to specify a range of times, where the start time is less than the specified time (in this case, 30 days). In other words, this will match any file with a modification time more than 30 days ago.
* `-exec rm {} \;`: This option tells find to execute a command on each matching file. The `rm` command is used to delete the file. The `{}` placeholder represents the name of the file that was found, and the `\;` at the end of the command is needed because the semicolon (`;`) is a special character in the shell and needs to be escaped.

So, when you put it all together, this command will find all files in the current directory and its subdirectories that are older than 30 days and delete them.

Generated command: find . -type f -mtime +30 -exec rm {} \;
Execute (e for explain)? (y/n/e):
```

If you feel adventurous, specify the `-y` flag to automatically execute the command:

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
Execute (e for explain)? (y/n/e): y
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
