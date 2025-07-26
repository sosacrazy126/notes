---
tags:
  - code_execution
  - security
  - integration
---
# About

Piston is a high performance general purpose code execution engine. It excels at running untrusted and possibly malicious code without fear from any harmful effects.

It's used in numerous places including:

- [EMKC Challenges](https://emkc.org/challenges)
- [EMKC Weekly Contests](https://emkc.org/contests)
- [Engineer Man Discord Server](https://discord.gg/engineerman)
- Web IDEs
- 200+ direct integrations

### Official Extensions

The following are approved and endorsed extensions/utilities to the core Piston offering.

- [I Run Code](https://github.com/engineer-man/piston-bot), a Discord bot used in 4100+ servers to handle arbitrary code evaluation in Discord. To get this bot in your own server, go here: https://emkc.org/run.
- [Piston CLI](https://github.com/Shivansh-007/piston-cli), a universal shell supporting code highlighting, files, and interpretation without the need to download a language.
- [Node Piston Client](https://github.com/dthree/node-piston), a Node.js wrapper for accessing the Piston API.
- [Piston4J](https://github.com/the-codeboy/Piston4J), a Java wrapper for accessing the Piston API.
- [Pyston](https://github.com/ffaanngg/pyston), a Python wrapper for accessing the Piston API.
- [Go-Piston](https://github.com/milindmadhukar/go-piston), a Golang wrapper for accessing the Piston API.
- [piston_rs](https://github.com/Jonxslays/piston_rs), a Rust wrapper for accessing the Piston API.
- [piston_rspy](https://github.com/Jonxslays/piston_rspy), Python bindings for accessing the Piston API via `piston_rs`.

---

# Public API

- Requires no installation and you can use it immediately.
- Reference the Runtimes/Execute sections below to learn about the request and response formats.

When using the public Piston API, use the following two URLs:

```
GET  https://emkc.org/api/v2/piston/runtimes
POST https://emkc.org/api/v2/piston/execute
```

> Important Note: The Piston API is rate limited to 5 requests per second. Effective May 7, 2024, no additional unlimited keys will be granted and existing keys will be revoked on Jan 1, 2025. The public instance is at capacity and the public limit is already very generous. For usage beyond 5 requests/second, you should consider self hosting.

---

# Getting Started

## All In One

### Host System Package Dependencies

- Docker
- Docker Compose
- Node JS (>= 15)
- cgroup v2 enabled, and cgroup v1 disabled

### After system dependencies are installed, clone this repository:

```sh
# clone and enter repo
git clone https://github.com/engineer-man/piston
```

> [!NOTE]
>
> Ensure the repository is cloned with LF line endings

### Installation

```sh
# Start the API container
docker-compose up -d api

# Install all the dependencies for the cli
cd cli && npm i && cd -
```

The API will now be online with no language runtimes installed. To install runtimes, [use the CLI](#cli).

## Just Piston (no CLI)

### Host System Package Dependencies

- Docker

### Installation

```sh
docker run \
    --privileged \
    -v $PWD:'/piston' \
    -dit \
    -p 2000:2000 \
    --name piston_api \
    ghcr.io/engineer-man/piston
```

## Piston for testing packages locally

### Host System Package Dependencies

- Same as [All In One](#All-In-One)

### Installation

```sh
# Build the Docker containers
./piston start

# For more help
./piston help
```

---

# Usage

### CLI

The CLI is the main tool used for installing packages within piston, but also supports running code.

You can execute the cli with `cli/index.js`.

```sh
# List all available packages
cli/index.js ppman list

# Install latest python
cli/index.js ppman install python

# Install specific version of python
cli/index.js ppman install python=3.9.4

# Run a python script using the latest version
echo 'print("Hello world!")' > test.py
cli/index.js run python test.py

# Run a python script using a specific version
echo 'print("Hello world!")' > test.py
cli/index.js run python test.py -l 3.9.4
cli/index.js run python test.py -l 3.x
cli/index.js run python test.py -l 3
```

If you are operating on a remote machine, add the `-u` flag like so:

```sh
cli/index.js -u http://piston.server:2000 ppman list
```

### API

The container exposes an API on port 2000 by default. This is used by the CLI to carry out running jobs and package management.

#### Runtimes Endpoint

`GET /api/v2/runtimes`  
This endpoint will return the supported languages along with the current version and aliases. To execute code for a particular language using the `/api/v2/execute` endpoint, either the name or one of the aliases must be provided, along with the version. Multiple versions of the same language may be present at the same time, and may be selected when running a job.

```json
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "language": "bash",
        "version": "5.1.0",
        "aliases": ["sh"]
    },
    {
        "language": "brainfuck",
        "version": "2.7.3",
        "aliases": ["bf"]
    },
    ...
]
```

#### Execute Endpoint

`POST /api/v2/execute`  
This endpoint requests execution of some arbitrary code.

**Parameters:**
- `language` (**required**): The language to use for execution (string, must be installed).
- `version` (**required**): The version of the language (string, SemVer selector or exact version).
- `files` (**required**): Array of files to execute. The first file is the main file.
  - `files[].name` (optional): File name (string, no path).
  - `files[].content` (**required**): File content (string).
  - `files[].encoding` (optional): Encoding (`base64`, `hex`, or `utf8`; defaults to `utf8`).
- `stdin` (optional): Input for stdin (string).
- `args` (optional): Arguments for the program (array).
- `compile_timeout` (optional): Max compile wall-time (ms, defaults to 10000).
- `run_timeout` (optional): Max run wall-time (ms, defaults to 3000).
- `compile_cpu_time` (optional): Max compile CPU-time (ms, defaults to 10000).
- `run_cpu_time` (optional): Max run CPU-time (ms, defaults to 3000).
- `compile_memory_limit` (optional): Max compile memory (bytes, defaults to -1/no limit).
- `run_memory_limit` (optional): Max run memory (bytes, defaults to -1/no limit).

**Example Request:**
```json
{
    "language": "js",
    "version": "15.10.0",
    "files": [
        {
            "name": "my_cool_code.js",
            "content": "console.log(process.argv)"
        }
    ],
    "stdin": "",
    "args": ["1", "2", "3"],
    "compile_timeout": 10000,
    "run_timeout": 3000,
    "compile_cpu_time": 10000,
    "run_cpu_time": 3000,
    "compile_memory_limit": -1,
    "run_memory_limit": -1
}
```

**Example Response (Success):**
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "language": "js",
    "version": "15.10.0",
    "run": {
        "stdout": "[\n  '/piston/packages/node/15.10.0/bin/node',\n  '/piston/jobs/9501b09d-0105-496b-b61a-e5148cf66384/my_cool_code',.js\n  '1',\n  '2',\n  '3'\n]\n",
        "stderr": "",
        "output": "[\n  '/piston/packages/node/15.10.0/bin/node',\n  '/piston/jobs/9501b09d-0105-496b-b61a-e5148cf66384/my_cool_code.js',\n  '1',\n  '2',\n  '3'\n]\n",
        "code": 0,
        "signal": null,
        "message": null,
        "status": null,
        "cpu_time": 8,
        "wall_time": 154,
        "memory": 1160000
    }
}
```

**Example Response (Error):**
```json
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "message": "html-5.0.0 runtime is unknown"
}
```

#### Interactive execution endpoint (not available through the public API)

Establish a WebSocket connection at `/api/v2/connect` for real-time interaction with processes. Messages are JSON objects with a `type` field:

- **init** (client → server): Initialize a job with parameters (excluding stdin).
- **runtime** (server → client): Returns runtime details (language, version).
- **stage** (server → client): Current stage ("compile" or "run").
- **data** (bidirectional): Exchange stdin/stdout/stderr data.
- **signal** (client → server): Send signals to processes.
- **exit** (server → client): Indicates stage completion with exit details.
- **error** (server → client): Reports fatal errors.

**Example Workflow:**
1. Client connects to `/api/v2/connect`.
2. `<` `{"type":"init", "language":"bash", "version":"*", "files":[{"content": "cat"}]}`
3. `>` `{"type":"runtime","language": "bash", "version": "5.1.0"}`
4. `>` `{"type":"stage", "stage":"run"}`
5. `<` `{"type":"data", "stream":"stdin", "data":"Hello World!"}`
6. `>` `{"type":"data", "stream":"stdout", "data":"Hello World!"}`
7. `>` `{"type":"exit", "stage":"run", "code":null, "signal": "SIGKILL"`

**Error Codes:**
- 4000: Already Initialized
- 4001: Initialization Timeout
- 4002: Notified Error
- 4003: Not yet Initialized
- 4004: Can only write to stdin
- 4005: Invalid Signal

---

# Supported Languages

- awk
- bash
- befunge93
- brachylog
- brainfuck
- bqn
- c
- c++
- cjam
- clojure
- cobol
- coffeescript
- cow
- crystal
- csharp
- csharp.net
- d
- dart
- dash
- dragon
- elixir
- emacs
- emojicode
- erlang
- file
- forte
- forth
- fortran
- freebasic
- fsharp.net
- fsi
- go
- golfscript
- groovy
- haskell
- husk
- iverilog
- japt
- java
- javascript
- jelly
- julia
- kotlin
- lisp
- llvm_ir
- lolcode
- lua
- matl
- nasm
- nasm64
- nim
- ocaml
- octave
- osabie
- paradoc
- pascal
- perl
- php
- ponylang
- powershell
- prolog
- pure
- pyth
- python
- python2
- racket
- raku
- retina
- rockstar
- rscript
- ruby
- rust
- samarium
- scala
- smalltalk
- sqlite3
- swift
- typescript
- basic
- basic.net
- vlang
- vyxal
- yeethon
- zig

---

# Principle of Operation

Piston uses [Isolate](https://www.ucw.cz/moe/isolate.1.html) inside Docker as the primary mechanism for sandboxing. The API within the container (written in Node.js) handles execution requests, writing source code and running it within an Isolate sandbox. Languages requiring compilation (e.g., C, C++, C#, Go) are compiled and executed in separate stages.

---

# Security

Piston leverages Isolate with Linux namespaces, chroot, unprivileged users, and cgroups for robust sandboxing. Key security measures include:

- Disabled outgoing network access by default.
- Process limit of 256 (prevents fork bombs).
- File limit of 2048 (resists file-based attacks).
- Temporary space cleanup post-execution.
- Unique unprivileged users per execution.
- Isolated Linux namespaces per submission.
- Default 3-second runtime limits (CPU and wall-time).
- Memory capping for processes.
- stdout capped at 1024 characters (prevents output bombs).
- SIGKILL for non-compliant processes.

---

# License

Piston is licensed under the MIT license.