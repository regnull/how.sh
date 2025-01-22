# how.sh - Create and execute shell commands using LLM

Use any LLM supported by [LLM CLI](https://llm.datasette.io/en/stable/index.html),
including OpenAI LLMs or local models provided by Ollama and any other LLM engines 
supported by LLM CLI.

## Use at your own risk

This script is experimental and may not work as expected. Use at your own risk.

## Prerequisites

### Install llm CLI

Follow the instructions at https://llm.datasette.io/en/stable/index.html.

### [Optional] Install Ollama and Ollama llm plugin

You don't have to do this unless you want to use Ollama models hosted on your own machine.
Depending on the LLM you use, your results may vary. Currently, this script is mostly tested
with Ollama-hosted deepseek-coder-v2 model.

To install Ollama, follow the instructions at https://ollama.com/download.

To use deepseek-coder-v2 model, you need to pre-load it:

```terminal
ollama pull deepseek-coder-v2
```

After installing Ollama, install the Ollama llm plugin:

```terminal
pip install llm-ollama
```

Verify that everything works:

```terminal
llm -m ollama/deepseek-coder-v2 "list files in the current directory"

how.sh uses llama3 by default, but you can use [any other model supported by ollama](https://ollama.ai/library).

## Usage

```bash
$ ./how.sh find and delete files older than 30 days
Generated command: find . -type f -mtime +30 -exec rm {} \;
Confirm (y/n/e/?) >>
```

If you enter `e`, the script will explain what the command does:

```text
./how.sh find and delete files older than 30 days
Generated command: find . -type f -mtime +30 -exec rm {} \;
Confirm (y/n/e/?) >> e
This command finds files in the current directory and all its subdirectories that are 
older than 30 days and deletes them.

Here's a breakdown of what each part of the command does:

* `find`: This is the command to search for files.
* `.`, the current directory: The dot at the beginning of the command tells 
find to start searching in the current directory.
* `-type f`: This option tells find to only consider files, not directories 
or other types of files.
* `-mtime +30`: This option tells find to only consider files that are older than 30 days. 
The `+` sign is used to specify a range of times, where the start time is less than the 
specified time (in this case, 30 days). In other words, this will match any file with a 
modification time more than 30 days ago.
* `-exec rm {} \;`: This option tells find to execute a command on each matching file. 
The `rm` command is used to delete the file. The `{}` placeholder represents the name of 
the file that was found, and the `\;` at the end of the command is needed because the 
semicolon (`;`) is a special character in the shell and needs to be escaped.

So, when you put it all together, this command will find all files in the 
current directory and its subdirectories that are older than 30 days and delete them.

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

To specify the default model, you can set the `HOW_SH_MODEL` environment variable:

```bash
export HOW_SH_MODEL=llama3
```

## Installation

Clone this repository and run the script from there.

If you want, you can add an alias:

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
Confirm (y/n/e/?) >> y
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

```bash
$ ./how.sh find large files in the current directory modified within the last 30 days and compress them into a single archive
Generated command:  find . -type f -size +10M -mtime -30 | xargs tar czvf large_files_archive.tar.gz
```

```terminal
$ ./how.sh create a file named bob containing the current timestamp
Generated command:  echo $(date +"%Y-%m-%d_%H:%M:%S") > bob
Confirm (y/n/e/?) >> y
Executing:  echo $(date +"%Y-%m-%d_%H:%M:%S") > bob
```

## Experimental features

### Fixing errors

If a command fails, how.sh can attempt to analyze the error and provide a fix:

```terminal
how -m 4o find out which process consumes the most memory
Generated command: ps -eo pid,comm,%mem --sort=-%mem | head -n 2 | tail -n 1
Confirm (y/n/e/?) >> y
Executing: ps -eo pid,comm,%mem --sort=-%mem | head -n 2 | tail -n 1
ps: illegal option -- -
usage: ps [-AaCcEefhjlMmrSTvwXx] [-O fmt | -o fmt] [-G gid[,gid...]]
          [-g grp[,grp...]] [-u [uid,uid...]]
          [-p pid[,pid...]] [-t tty[,tty...]] [-U user[,user...]]
       ps [-L]

Command failed with exit code 1
I can attempt to analyze the error and provide a fix.
Try to fix the command (y/n) >> y
Generated command: ps aux --sort=-%mem | head -n 2 | tail -n 1
Confirm (y/n/e/?) >> y
Executing: ps aux --sort=-%mem | head -n 2 | tail -n 1
ps: illegal option -- -
usage: ps [-AaCcEefhjlMmrSTvwXx] [-O fmt | -o fmt] [-G gid[,gid...]]
          [-u]
          [-p pid[,pid...]] [-t tty[,tty...]] [-U user[,user...]]
       ps [-L]

Command failed with exit code 1
I can attempt to analyze the error and provide a fix.
Try to fix the command (y/n) >> y
Generated command: ps aux | sort -rk 4 | head -n 2 | tail -n 1
Confirm (y/n/e/?) >> y
Executing: ps aux | sort -rk 4 | head -n 2 | tail -n 1
regnull           4490   0.0  3.0 1624091136 568288   ??  S    Sun09AM  60:50.79 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/131.0.6778.265/Helpers/Google Chrome Helper (Renderer).app/Contents/MacOS/Google Chrome Helper (Renderer) --type=renderer --string-annotations --enable-chrome-cart --lang=en-US --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=75 --time-ticks-at-unix-epoch=-1737295686309350 --launch-time-ticks=218700919 --shared-files --field-trial-handle=1718379636,r,5166342679572925582,4154369641191108277,262144 --variations-seed-version=20250117-130131.443000 --seatbelt-client=103
```

### How.sh Scripting

If you like to live dangerously, you can use how.sh in your bash scripts, like so:

```bash
#!/bin/bash
set -e
../how.sh -y create a file named bob which contains the current timestamp 
../how.sh -y tell me what does file named bob contain
../how.sh -y delete file named bob
```

If you run this, and you are lucky, you will get the following output:

```teminal
./bob.sh
Generated command:  echo $(date +"%Y-%m-%d %H:%M:%S") > bob
Executing:  echo $(date +"%Y-%m-%d %H:%M:%S") > bob
Generated command:  cat bob
Executing:  cat bob
2025-01-22 17:16:43
Generated command:  rm -f bob
Executing:  rm -f bob
```

