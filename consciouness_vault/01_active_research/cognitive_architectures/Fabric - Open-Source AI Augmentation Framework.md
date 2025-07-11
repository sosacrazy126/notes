---
tags:
  - open_source
  - AI_augmentation
  - frameworks
---
<div align="center">

<img src="./images/fabric-logo-gif.gif" alt="fabriclogo" width="400" height="400"/>

# `fabric`

![Static Badge](https://img.shields.io/badge/mission-human_flourishing_via_AI_augmentation-purple)
<br />
![GitHub top language](https://img.shields.io/github/languages/top/danielmiessler/fabric)
![GitHub last commit](https://img.shields.io/github/last-commit/danielmiessler/fabric)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

<p class="align center">
<h4><code>fabric</code> is an open-source framework for augmenting humans using AI.</h4>
</p>

[Updates](#updates) •
[What and Why](#what-and-why) •
[Philosophy](#philosophy) •
[Installation](#Installation) •
[Usage](#Usage) •
[Examples](#examples) •
[Just Use the Patterns](#just-use-the-patterns) •
[Custom Patterns](#custom-patterns) •
[Helper Apps](#helper-apps) •
[Meta](#meta)

![Screenshot of fabric](images/fabric-summarize.png)

</div>

## Navigation

- [`fabric`](#fabric)
  - [Navigation](#navigation)
  - [Updates](#updates)
  - [What and why](#what-and-why)
  - [Intro videos](#intro-videos)
  - [Philosophy](#philosophy)
    - [Breaking problems into components](#breaking-problems-into-components)
    - [Too many prompts](#too-many-prompts)
  - [Installation](#installation)
    - [Get Latest Release Binaries](#get-latest-release-binaries)
      - [Windows](#windows)
      - [macOS (arm64)](#macos-arm64)
      - [macOS (amd64)](#macos-amd64)
      - [Linux (amd64)](#linux-amd64)
      - [Linux (arm64)](#linux-arm64)
    - [Using package managers](#using-package-managers)
      - [macOS (Homebrew)](#macos-homebrew)
      - [Arch Linux (AUR)](#arch-linux-aur)
    - [From Source](#from-source)
    - [Environment Variables](#environment-variables)
    - [Setup](#setup)
    - [Add aliases for all patterns](#add-aliases-for-all-patterns)
      - [Save your files in markdown using aliases](#save-your-files-in-markdown-using-aliases)
    - [Migration](#migration)
    - [Upgrading](#upgrading)
  - [Usage](#usage)
  - [Our approach to prompting](#our-approach-to-prompting)
  - [Examples](#examples)
  - [Just use the Patterns](#just-use-the-patterns)
    - [Prompt Strategies](#prompt-strategies)
  - [Custom Patterns](#custom-patterns)
  - [Helper Apps](#helper-apps)
    - [`to_pdf`](#to_pdf)
    - [`to_pdf` Installation](#to_pdf-installation)
    - [`code_helper`](#code_helper)
  - [pbpaste](#pbpaste)
  - [Web Interface](#web-interface)
    - [Installing](#installing)
    - [Streamlit UI](#streamlit-ui)
      - [Clipboard Support](#clipboard-support)
  - [Meta](#meta)
    - [Primary contributors](#primary-contributors)

<br />

## Updates

> [!NOTE]
> February 24, 2025
>
> - Fabric now supports Sonnet 3.7! Update and use `-S` to select it as your default if you want, or just use the shortcut `-m claude-3-7-sonnet-latest`. Enjoy!

## What and why

Since the start of 2023 and GenAI we've seen a massive number of AI applications for accomplishing tasks. It's powerful, but _it's not easy to integrate this functionality into our lives._

<div align="center">
<h4>In other words, AI doesn't have a capabilities problem—it has an <em>integration</em> problem.</h4>
</div>

Fabric was created to address this by enabling everyone to granularly apply AI to everyday challenges.

## Intro videos

Keep in mind that many of these were recorded when Fabric was Python-based, so remember to use the current [install instructions](#installation) below.

- [Network Chuck](https://www.youtube.com/watch?v=UbDyjIIGaxQ)
- [David Bombal](https://www.youtube.com/watch?v=vF-MQmVxnCs)
- [My Own Intro to the Tool](https://www.youtube.com/watch?v=wPEyyigh10g)
- [More Fabric YouTube Videos](https://www.youtube.com/results?search_query=fabric+ai)

## Philosophy

> AI isn't a thing; it's a _magnifier_ of a thing. And that thing is **human creativity**.

We believe the purpose of technology is to help humans flourish, so when we talk about AI we start with the **human** problems we want to solve.

### Breaking problems into components

Our approach is to break problems into individual pieces (see below) and then apply AI to them one at a time. See below for some examples.

<img width="2078" alt="augmented_challenges" src="https://github.com/danielmiessler/fabric/assets/50654/31997394-85a9-40c2-879b-b347e4701f06">

### Too many prompts

Prompts are good for this, but the biggest challenge I faced in 2023——which still exists today—is **the sheer number of AI prompts out there**. We all have prompts that are useful, but it's hard to discover new ones, know if they are good or not, _and manage different versions of the ones we like_.

One of `fabric`'s primary features is helping people collect and integrate prompts, which we call _Patterns_, into various parts of their lives.

Fabric has Patterns for all sorts of life and work activities, including:

- Extracting the most interesting parts of YouTube videos and podcasts
- Writing an essay in your own voice with just an idea as an input
- Summarizing opaque academic papers
- Creating perfectly matched AI art prompts for a piece of writing
- Rating the quality of content to see if you want to read/watch the whole thing
- Getting summaries of long, boring content
- Explaining code to you
- Turning bad documentation into usable documentation
- Creating social media posts from any content input
- And a million more…

## Installation

To install Fabric, you can use the latest release binaries or install it from the source.

### Get Latest Release Binaries

#### Windows

`https://github.com/danielmiessler/fabric/releases/latest/download/fabric-windows-amd64.exe`

#### macOS (arm64)

`curl -L https://github.com/danielmiessler/fabric/releases/latest/download/fabric-darwin-arm64 > fabric && chmod +x fabric && ./fabric --version`

#### macOS (amd64)

`curl -L https://github.com/danielmiessler/fabric/releases/latest/download/fabric-darwin-amd64 > fabric && chmod +x fabric && ./fabric --version`

#### Linux (amd64)

`curl -L https://github.com/danielmiessler/fabric/releases/latest/download/fabric-linux-amd64 > fabric && chmod +x fabric && ./fabric --version`

#### Linux (arm64)

`curl -L https://github.com/danielmiessler/fabric/releases/latest/download/fabric-linux-arm64 > fabric && chmod +x fabric && ./fabric --version`

### Using package managers

**NOTE:** using Homebrew or the Arch Linux package managers makes `fabric` available as `fabric-ai`, so add
the following alias to your shell startup files to account for this:

```bash
alias fabric='fabric-ai'
```

#### macOS (Homebrew)

`brew install fabric-ai`

#### Arch Linux (AUR)

`yay -S fabric-ai`

### From Source

To install Fabric, [make sure Go is installed](https://go.dev/doc/install), and then run the following command.

```bash
# Install Fabric directly from the repo
go install github.com/danielmiessler/fabric@latest
```

### Environment Variables

You may need to set some environment variables in your `~/.bashrc` on linux or `~/.zshrc` file on mac to be able to run the `fabric` command. Here is an example of what you can add:

For Intel based macs or linux

```bash
# Golang environment variables
export GOROOT=/usr/local/go
export GOPATH=$HOME/go

# Update PATH to include GOPATH and GOROOT binaries
export PATH=$GOPATH/bin:$GOROOT/bin:$HOME/.local/bin:$PATH
```

for Apple Silicon based macs

```bash
# Golang environment variables
export GOROOT=$(brew --prefix go)/libexec
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$HOME/.local/bin:$PATH
```

### Setup

Now run the following command

```bash
# Run the setup to set up your directories and keys
fabric --setup
```

If everything works you are good to go.

### Add aliases for all patterns

In order to add aliases for all your patterns and use them directly as commands ie. `summarize` instead of `fabric --pattern summarize`
You can add the following to your `.zshrc` or `.bashrc` file.

```bash
# Loop through all files in the ~/.config/fabric/patterns directory
for pattern_file in $HOME/.config/fabric/patterns/*; do
    # Get the base name of the file (i.e., remove the directory path)
    pattern_name=$(basename "$pattern_file")

    # Create an alias in the form: alias pattern_name="fabric --pattern pattern_name"
    alias_command="alias $pattern_name='fabric --pattern $pattern_name'"

    # Evaluate the alias command to add it to the current shell
    eval "$alias_command"
done

yt() {
    if [ "$#" -eq 0 ] || [ "$#" -gt 2 ]; then
        echo "Usage: yt [-t | --timestamps] youtube-link"
        echo "Use the '-t' flag to get the transcript with timestamps."
        return 1
    fi

    transcript_flag="--transcript"
    if [ "$1" = "-t" ] || [ "$1" = "--timestamps" ]; then
        transcript_flag="--transcript-with-timestamps"
        shift
    fi
    local video_link="$1"
    fabric -y "$video_link" $transcript_flag
}
```

You can add the below code for the equivalent aliases inside PowerShell by running `notepad $PROFILE` inside a PowerShell window:

```powershell
# Path to the patterns directory
$patternsPath = Join-Path $HOME ".config/fabric/patterns"
foreach ($patternDir in Get-ChildItem -Path $patternsPath -Directory) {
    $patternName = $patternDir.Name

    # Dynamically define a function for each pattern
    $functionDefinition = @"
function $patternName {
    [CmdletBinding()]
    param(
        [Parameter(ValueFromPipeline = `$true)]
        [string] `$InputObject,

        [Parameter(ValueFromRemainingArguments = `$true)]
        [String[]] `$patternArgs
    )

    begin {
        # Initialize an array to collect pipeline input
        `$collector = @()
    }

    process {
        # Collect pipeline input objects
        if (`$InputObject) {
            `$collector += `$InputObject
        }
    }

    end {
        # Join all pipeline input into a single string, separated by newlines
        `$pipelineContent = `$collector -join "`n"

        # If there's pipeline input, include it in the call to fabric
        if (`$pipelineContent) {
            `$pipelineContent | fabric --pattern $patternName `$patternArgs
        } else {
            # No pipeline input; just call fabric with the additional args
            fabric --pattern $patternName `$patternArgs
        }
    }
}
"@
    # Add the function to the current session
    Invoke-Expression $functionDefinition
}

# Define the 'yt' function as well
function yt {
    [CmdletBinding()]
    param(
        [Parameter()]
        [Alias("timestamps")]
        [switch]$t,

        [Parameter(Position = 0, ValueFromPipeline = $true)]
        [string]$videoLink
    )

    begin {
        $transcriptFlag = "--transcript"
        if ($t) {
            $transcriptFlag = "--transcript-with-timestamps"
        }
    }

    process {
        if (-not $videoLink) {
            Write-Error "Usage: yt [-t | --timestamps] youtube-link"
            return
        }
    }

    end {
        if ($videoLink) {
            # Execute and allow output to flow through the pipeline
            fabric -y $videoLink $transcriptFlag
        }
    }
}
```

This also creates a `yt` alias that allows you to use `yt https://www.youtube.com/watch?v=4b0iet22VIk` to get transcripts, comments, and metadata.

#### Save your files in markdown using aliases

If in addition to the above aliases you would like to have the option to save the output to your favorite markdown note vault like Obsidian then instead of the above add the following to your `.zshrc` or `.bashrc` file:

```bash
# Define the base directory for Obsidian notes
obsidian_base="/path/to/obsidian"

# Loop through all files in the ~/.config/fabric/patterns directory
for pattern_file in ~/.config/fabric/patterns/*; do
    # Get the base name of the file (i.e., remove the directory path)
    pattern_name=$(basename "$pattern_file")

    # Remove any existing alias with the same name
    unalias "$pattern_name" 2>/dev/null

    # Define a function dynamically for each pattern
    eval "
    $pattern_name() {
        local title=\$1
        local date_stamp=\$(date +'%Y-%m-%d')
        local output_path=\"\$obsidian_base/\${date_stamp}-\${title}.md\"

        # Check if a title was provided
        if [ -n \"\$title\" ]; then
            # If a title is provided, use the output path
            fabric --pattern \"$pattern_name\" -o \"\$output_path\"
        else
            # If no title is provided, use --stream
            fabric --pattern \"$pattern_name\" --stream
        fi
    }
    "
done
```

This will allow you to use the patterns as aliases like in the above for example `summarize` instead of `fabric --pattern summarize --stream`, however if you pass in an extra argument like this `summarize "my_article_title"` your output will be saved in the destination that you set in `obsidian_base="/path/to/obsidian"` in the following format `YYYY-MM-DD-my_article_title.md` where the date gets autogenerated for you.
You can tweak the date format by tweaking the `date_stamp` format.

### Migration

If you have the Legacy (Python) version installed and want to migrate to the Go version, here's how you do it. It's basically two steps: 1) uninstall the Python version, and 2) install the Go version.

```bash
# Uninstall Legacy Fabric
pipx uninstall fabric

# Clear any old Fabric aliases
(check your .bashrc, .zshrc, etc.)
# Install the Go version
go install github.com/danielmiessler/fabric@latest
# Run setup for the new version. Important because things have changed
fabric --setup
```

Then [set your environmental variables](#environment-variables) as shown above.

### Upgrading

The great thing about Go is that it's super easy to upgrade. Just run the same command you used to install it in the first place and you'll always get the latest version.

```bash
go install github.com/danielmiessler/fabric@latest
```

## Usage

Once you have it all set up, here's how to use it.

```bash
fabric -h
```

```bash

Usage:
  fabric [OPTIONS]

Application Options:
  -p, --pattern=                    Choose a pattern from the available patterns
  -v, --variable=                   Values for pattern variables, e.g. -v=#role:expert -v=#points:30
  -C, --context=                    Choose a context from the available contexts
      --session=                    Choose a session from the available sessions
  -a, --attachment=                 Attachment path or URL (e.g. for OpenAI image recognition messages)
  -S, --setup                       Run setup for all reconfigurable parts of fabric
  -t, --temperature=                Set temperature (default: 0.7)
  -T, --topp=                       Set top P (default: 0.9)
  -s, --stream                      Stream
  -P, --presencepenalty=            Set presence penalty (default: 0.0)
  -r, --raw                         Use the defaults of the model without sending chat options (like temperature etc.) and use the user role instead of the system role for patterns.
  -F, --frequencypenalty=           Set frequency penalty (default: 0.0)
  -l, --listpatterns                List all patterns
  -L, --listmodels                  List all available models
  -x, --listcontexts                List all contexts
  -X, --listsessions                List all sessions
  -U, --updatepatterns              Update patterns
  -c, --copy                        Copy to clipboard
  -m, --model=                      Choose model
      --modelContextLength=         Model context length (only affects ollama)
  -o, --output=                     Output to file
      --output-session              Output the entire session (also a temporary one) to the output file
  -n, --latest=                     Number of latest patterns to list (default: 0)
  -d, --changeDefaultModel          Change default model
  -y, --youtube=                    YouTube video or play list "URL" to grab transcript, comments from it and send to chat or print it put to the console and store it in the output file
      --playlist                    Prefer playlist over video if both ids are present in the URL
      --transcript                  Grab transcript from YouTube video and send to chat (it is used per default).
      --transcript-with-timestamps  Grab transcript from YouTube video with timestamps and send to chat
      --comments                    Grab comments from YouTube video and send to chat
      --metadata                    Output video metadata
  -g, --language=                   Specify the Language Code for the chat, e.g. -g=en -g=zh
  -u, --scrape_url=                 Scrape website URL to markdown using Jina AI
  -q, --scrape_question=            Search question using Jina AI
  -e, --seed=                       Seed to be used for LMM generation
  -w, --wipecontext=                Wipe context
  -W, --wipesession=                Wipe session
      --printcontext=               Print context
      --printsession=               Print session
      --readability                 Convert HTML input into a clean, readable view
      --input-has-vars              Apply variables to user input
      --dry-run                     Show what would be sent to the model without actually sending it
      --serve                       Serve the Fabric Rest API
      --serveOllama                 Serve the Fabric Rest API with ollama endpoints
      --address=                    The address to bind the REST API (default: :8080)
      --config=                     Path to YAML config file
      --version                     Print current version
      --listextensions              List all registered extensions
      --addextension=               Register a new extension from config file path
      --rmextension=                Remove a registered extension by name
      --strategy=                   Choose a strategy from the available strategies
      --liststrategies              List all strategies

Help Options:
  -h, --help                        Show this help message

```

## Our approach to prompting

Fabric _Patterns_ are different than most prompts you'll see.

- **First, we use `Markdown` to help ensure maximum readability and editability**. This not only helps the creator make a good one, but also anyone who wants to deeply understand what it does. _Importantly, this also includes the AI you're sending it to!_

Here's an example of a Fabric Pattern.

```bash
https://github.com/danielmiessler/fabric/blob/main/patterns/extract_wisdom/system.md
```

<img width="1461" alt="pattern-example" src="https://github.com/danielmiessler/fabric/assets/50654/b910c551-9263-405f-9735-71ca69bbab6d">

- **Next, we are extremely clear in our instructions**, and we use the Markdown structure to emphasize what we want the AI to do, and in what order.

- **And finally, we tend to use the System section of the prompt almost exclusively**. In over a year of being heads-down with this stuff, we've just seen more efficacy from doing that. If that changes, or we're shown data that says otherwise, we will adjust.

## Examples

> The following examples use the macOS `pbpaste` to paste from the clipboard. See the [pbpaste](#pbpaste) section below for Windows and Linux alternatives.

Now let's look at some things you can do with Fabric.

1. Run the `summarize` Pattern based on input from `stdin`. In this case, the body of an article.

    ```bash
    pbpaste | fabric --pattern summarize
    ```

2. Run the `analyze_claims` Pattern with the `--stream` option to get immediate and streaming results.

    ```bash
    pbpaste | fabric --stream --pattern analyze_claims
    ```

3. Run the `extract_wisdom` Pattern with the `--stream` option to get immediate and streaming results from any      Youtube video (much like in the original introduction video).

    ```bash
    fabric -y "https://youtube.com/watch?v=uXs-zPc63kM" --stream --pattern extract_wisdom
    ```

4. Create patterns- you must create a .md file with the pattern and save it to `~/.config/fabric/patterns/[yourpatternname]`.

5. Run a `analyze_claims` pattern on a website. Fabric uses Jina AI to scrape the URL into markdown format before sending it to the model.

    ```bash
    fabric -u https://github.com/danielmiessler/fabric/ -p analyze_claims
    ```

## Just use the Patterns

<img width="1173" alt="fabric-patterns-screenshot" src="https://github.com/danielmiessler/fabric/assets/50654/9186a044-652b-4673-89f7-71cf066f32d8">

<br />
<br />

If you're not looking to do anything fancy, and you just want a lot of great prompts, you can navigate to the [`/patterns`](https://github.com/danielmiessler/fabric/tree/main/patterns) directory and start exploring!

We hope that if you used nothing else from Fabric, the Patterns by themselves will make the project useful.

You can use any of the Patterns you see there in any AI application that you have, whether that's ChatGPT or some other app or website. Our plan and prediction is that people will soon be sharing many more than those we've published, and they will be way better than ours.

The wisdom of crowds for the win.

### Prompt Strategies

Fabric also implements prompt strategies like "Chain of Thought" or "Chain of Draft" which can
be used in addition to the basic patterns.

See the [Thinking Faster by Writing Less](https://arxiv.org/pdf/2502.18600) paper and
the [Thought Generation section of Learn Prompting](https://learnprompting.org/docs/advanced/thought_generation/introduction) for examples of prompt strategies.

Each strategy is available as a small `json` file in the [`/strategies`](https://github.com/danielmiessler/fabric/tree/main/strategies) directory.

The prompt modification of the strategy is applied to the system prompt and passed on to the
LLM in the chat session.

Use `fabric -S` and select the option to install the strategies in your `~/.config/fabric` directory.

## Custom Patterns

You may want to use Fabric to create your own custom Patterns—but not share them with others. No problem!

Just make a directory in `~/.config/custompatterns/` (or wherever) and put your `.md` files in there.

When you're ready to use them, copy them into `~/.config/fabric/patterns/`

You can then use them like any other Patterns, but they won't be public unless you explicitly submit them as Pull Requests to the Fabric project. So don't worry—they're private to you.

## Helper Apps

Fabric also makes use of some core helper apps (tools) to make it easier to integrate with your various workflows. Here are some examples:

### `to_pdf`

`to_pdf` is a helper command that converts LaTeX files to PDF format. You can use it like this:

```bash
to_pdf input.tex
```

This will create a PDF file from the input LaTeX file in the same directory.

You can also use it with stdin which works perfectly with the `write_latex` pattern:

```bash
echo "ai security primer" | fabric --pattern write_latex | to_pdf
```

This will create a PDF file named `output.pdf` in the current directory.

### `to_pdf` Installation

To install `to_pdf`, install it the same way as you install Fabric, just with a different repo name.

```bash
go install github.com/danielmiessler/fabric/plugins/tools/to_pdf@latest
```

Make sure you have a LaTeX distribution (like TeX Live or MiKTeX) installed on your system, as `to_pdf` requires `pdflatex` to be available in your system's PATH.

### `code_helper`

`code_helper` is used in conjunction with the `create_coding_feature` pattern.
It generates a `json` representation of a directory of code that can be fed into an AI model
with instructions to create a new feature or edit the code in a specified way.

See [the Create Coding Feature Pattern README](./patterns/create_coding_feature/README.md) for details.

Install it first using:

```bash
go install github.com/danielmiessler/fabric/plugins/tools/code_helper@latest
```

## pbpaste

The [examples](#examples) use the macOS program `pbpaste` to paste content from the clipboard to pipe into `fabric` as the input. `pbpaste` is not available on Windows or Linux, but there are alternatives.

On Windows, you can use the PowerShell command `Get-Clipboard` from a PowerShell command prompt. If you like, you can also alias it to `pbpaste`. If you are using classic PowerShell, edit the file `~\Documents\WindowsPowerShell\.profile.ps1`, or if you are using PowerShell Core, edit `~\Documents\PowerShell\.profile.ps1` and add the alias,

```powershell
Set-Alias pbpaste Get-Clipboard
```

On Linux, you can use `xclip -selection clipboard -o` to paste from the clipboard. You will likely need to install `xclip` with your package manager. For Debian based systems including Ubuntu,

```sh
sudo apt update
sudo apt install xclip -y
```

You can also create an alias by editing `~/.bashrc` or `~/.zshrc` and adding the alias,

```sh
alias pbpaste='xclip -selection clipboard -o'
```

## Web Interface

Fabric now includes a built-in web interface that provides a GUI alternative to the command-line interface and an out-of-the-box website for those who want to get started with web development or blogging.
You can use this app as a GUI interface for Fabric, a ready to go blog-site, or a website template for your own projects.

The `web/src/lib/content` directory includes starter `.obsidian/` and `templates/` directories, allowing you to open up the `web/src/lib/content/` directory as an [Obsidian.md](https://obsidian.md) vault. You can place your posts in the posts directory when you're ready to publish.

### Installing

The GUI can be installed by navigating to the `web` directory and using `npm install`, `pnpm install`, or your favorite package manager. Then simply run the development server to start the app.

_You will need to run fabric in a separate terminal with the `fabric --serve` command._

**From the fabric project `web/` directory:**

```shell
npm run dev

## or ##

pnpm run dev

## or your equivalent
```

### Streamlit UI

To run the Streamlit user interface:

```bash
# Install required dependencies
pip install -r requirements.txt

# Or manually install dependencies
pip install streamlit pandas matplotlib seaborn numpy python-dotenv pyperclip

# Run the Streamlit app
streamlit run streamlit.py
```

The Streamlit UI provides a user-friendly interface for:

- Running and chaining patterns
- Managing pattern outputs
- Creating and editing patterns
- Analyzing pattern results

#### Clipboard Support

The Streamlit UI supports clipboard operations across different platforms:

- **macOS**: Uses `pbcopy` and `pbpaste` (built-in)
- **Windows**: Uses `pyperclip` library (install with `pip install pyperclip`)
- **Linux**: Uses `xclip` (install with `sudo apt-get install xclip` or equivalent for your distro)

## Meta

> [!NOTE]
> Special thanks to the following people for their inspiration and contributions!

- _Jonathan Dunn_ for being the absolute MVP dev on the project, including spearheading the new Go version, as well as the GUI! All this while also being a full-time medical doctor!
- _Caleb Sima_ for pushing me over the edge of whether to make this a public project or not.
- _Eugen Eisler_ and _Frederick Ros_ for their invaluable contributions to the Go version
- _David Peters_ for his work on the web interface.
- _Joel Parish_ for super useful input on the project's Github directory structure..
- _Joseph Thacker_ for the idea of a `-c` context flag that adds pre-created context in the `./config/fabric/` directory to all Pattern queries.
- _Jason Haddix_ for the idea of a stitch (chained Pattern) to filter content using a local model before sending on to a cloud model, i.e., cleaning customer data using `llama2` before sending on to `gpt-4` for analysis.
- _Andre Guerra_ for assisting with numerous components to make things simpler and more maintainable.

### Primary contributors

<a href="https://github.com/danielmiessler"><img src="https://avatars.githubusercontent.com/u/50654?v=4" title="Daniel Miessler" width="50" height="50"></a>
<a href="https://github.com/xssdoctor"><img src="https://avatars.githubusercontent.com/u/9218431?v=4" title="Jonathan Dunn" width="50" height="50"></a>
<a href="https://github.com/sbehrens"><img src="https://avatars.githubusercontent.com/u/688589?v=4" title="Scott Behrens" width="50" height="50"></a>
<a href="https://github.com/agu3rra"><img src="https://avatars.githubusercontent.com/u/10410523?v=4" title="Andre Guerra" width="50" height="50"></a>

`fabric` was created by <a href="https://danielmiessler.com/subscribe" target="_blank">Daniel Miessler</a> in January of 2024.
<br /><br />
<a href="https://twitter.com/intent/user?screen_name=danielmiessler">![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/danielmiessler)</a>

## YouTube Video: You&#39;ve been using AI Wrong

### Transcript

I found a new AI tool and I am obsessed. tell me what fabric is. Problems. That&amp;#39;s Daniel Meer, we&amp;#39;ll talk more about them later. Now before we dive too deep, transcript and paste the link, video, the ideas, insights, quotes, like this one man who said that smart guy. which again, here in a bit. Now looking at the command, called patterns. a very specific problem, We don&amp;#39;t know why it works, It&amp;#39;s so amazing. But hold on, AI help you solve problems. the pain of interfacing with AI APIs. which gets all sorts of amazing data. about this world of text. proficient with Vim and the Terminal, humans. by anything, especially ai. And by the way, of other stuff from cybersecurity, really fast. And then best practice, you don&amp;#39;t have to do that, We&amp;#39;re all following along right now. If you&amp;#39;re using ZSH as your default. Those are free to set up. Again, why do we have to do that? Well, remember, It will use whatever favorite AI you have. Put your credit card in there. Pro, but just keep that in mind. Now, So to connect to a remote AI server, specify remote llama server, Specify the model Llama three 70 B, That&amp;#39;s where Twin Gate comes in. and then deploy connector. your Sonology nas like I do at my home. I&amp;#39;m getting out of here. I&amp;#39;ll show you somewhere else. Anyways, So summarize the article, it. And this pattern will be right essay. it&amp;#39;s B tier, consume when time allows. I didn&amp;#39;t really know how to do it. a pattern means solving a problem. We&amp;#39;ll echo something and say you are, I go to church every Sunday. and I miss the sermon. Now, I&amp;#39;m going to take this, copy it. That&amp;#39;s the patterns that fabric we&amp;#39;ll use. and we created a file called System md, you&amp;#39;ll want to update your patterns. That way they&amp;#39;re never deleted, we&amp;#39;ll specify our directory, I should see sermon sensei right there. you can work on yours and keep iterating. Probably one of my favorite things, if we type in fabric help, We&amp;#39;re not going to go over all of them, We now have a context file. Now I&amp;#39;ve got two more features. prompter. Now, to understand that, as of the end of 22. As soon as the ai, I built a VM program over there. and I had been in AI for five, six years. but it became the content for Fabric. many iterations. It does things so well. expected. And that&amp;#39;s so fun. where it&amp;#39;s not about replacing humans, So I&amp;#39;m not stepping away and disengaging, I&amp;#39;m still reading massive number of books, quickly digest it. he designed these prompts, something, And that&amp;#39;s what this emulates. don&amp;#39;t do the AI stuff. Yeah, I think the way to use it is to use the context stuff And importantly, going back to your earlier point, So everything shouldn&amp;#39;t be a summary. you get the most muscle growth. Don&amp;#39;t take the weights out of the gym. or you could wait on that. Again, faster rate than you could before. to help you solve that problem. the week and then it&amp;#39;ll tell me, Keep doing that. see myself growing the fabric. it&amp;#39;s free, and then pipe that into fabric. through. So I have the recording transcribed. That&amp;#39;s a video coming soon. And again, system. So if you&amp;#39;re new to obsidian, And here&amp;#39;s my path to the directory. I&amp;#39;m just going to save this to a file. And then if I jump into my obsidian, Lemme know if you like this too. help of ai. I don&amp;#39;t know.

## YouTube Video: You&#39;ve been using AI Wrong

### Transcript

I found a new AI tool and I am obsessed. tell me what fabric is. Problems. That&amp;#39;s Daniel Meer, we&amp;#39;ll talk more about them later. Now before we dive too deep, transcript and paste the link, video, the ideas, insights, quotes, like this one man who said that smart guy. which again, here in a bit. Now looking at the command, called patterns. a very specific problem, We don&amp;#39;t know why it works, It&amp;#39;s so amazing. But hold on, AI help you solve problems. the pain of interfacing with AI APIs. which gets all sorts of amazing data. about this world of text. proficient with Vim and the Terminal, humans. by anything, especially ai. And by the way, of other stuff from cybersecurity, really fast. And then best practice, you don&amp;#39;t have to do that, We&amp;#39;re all following along right now. If you&amp;#39;re using ZSH as your default. Those are free to set up. Again, why do we have to do that? Well, remember, It will use whatever favorite AI you have. Put your credit card in there. Pro, but just keep that in mind. Now, So to connect to a remote AI server, specify remote llama server, Specify the model Llama three 70 B, That&amp;#39;s where Twin Gate comes in. and then deploy connector. your Sonology nas like I do at my home. I&amp;#39;m getting out of here. I&amp;#39;ll show you somewhere else. Anyways, So summarize the article, it. And this pattern will be right essay. it&amp;#39;s B tier, consume when time allows. I didn&amp;#39;t really know how to do it. a pattern means solving a problem. We&amp;#39;ll echo something and say you are, I go to church every Sunday. and I miss the sermon. Now, I&amp;#39;m going to take this, copy it. That&amp;#39;s the patterns that fabric we&amp;#39;ll use. and we created a file called System md, you&amp;#39;ll want to update your patterns. That way they&amp;#39;re never deleted, we&amp;#39;ll specify our directory, I should see sermon sensei right there. you can work on yours and keep iterating. Probably one of my favorite things, if we type in fabric help, We&amp;#39;re not going to go over all of them, We now have a context file. Now I&amp;#39;ve got two more features. prompter. Now, to understand that, as of the end of 22. As soon as the ai, I built a VM program over there. and I had been in AI for five, six years. but it became the content for Fabric. many iterations. It does things so well. expected. And that&amp;#39;s so fun. where it&amp;#39;s not about replacing humans, So I&amp;#39;m not stepping away and disengaging, I&amp;#39;m still reading massive number of books, quickly digest it. he designed these prompts, something, And that&amp;#39;s what this emulates. don&amp;#39;t do the AI stuff. Yeah, I think the way to use it is to use the context stuff And importantly, going back to your earlier point, So everything shouldn&amp;#39;t be a summary. you get the most muscle growth. Don&amp;#39;t take the weights out of the gym. or you could wait on that. Again, faster rate than you could before. to help you solve that problem. the week and then it&amp;#39;ll tell me, Keep doing that. see myself growing the fabric. it&amp;#39;s free, and then pipe that into fabric. through. So I have the recording transcribed. That&amp;#39;s a video coming soon. And again, system. So if you&amp;#39;re new to obsidian, And here&amp;#39;s my path to the directory. I&amp;#39;m just going to save this to a file. And then if I jump into my obsidian, Lemme know if you like this too. help of ai. I don&amp;#39;t know.

## YouTube Video: You&#39;ve been using AI Wrong

### Transcript

I found a new AI tool and I am obsessed. tell me what fabric is. Problems. That&amp;#39;s Daniel Meer, we&amp;#39;ll talk more about them later. Now before we dive too deep, transcript and paste the link, video, the ideas, insights, quotes, like this one man who said that smart guy. which again, here in a bit. Now looking at the command, called patterns. a very specific problem, We don&amp;#39;t know why it works, It&amp;#39;s so amazing. But hold on, AI help you solve problems. the pain of interfacing with AI APIs. which gets all sorts of amazing data. about this world of text. proficient with Vim and the Terminal, humans. by anything, especially ai. And by the way, of other stuff from cybersecurity, really fast. And then best practice, you don&amp;#39;t have to do that, We&amp;#39;re all following along right now. If you&amp;#39;re using ZSH as your default. Those are free to set up. Again, why do we have to do that? Well, remember, It will use whatever favorite AI you have. Put your credit card in there. Pro, but just keep that in mind. Now, So to connect to a remote AI server, specify remote llama server, Specify the model Llama three 70 B, That&amp;#39;s where Twin Gate comes in. and then deploy connector. your Sonology nas like I do at my home. I&amp;#39;m getting out of here. I&amp;#39;ll show you somewhere else. Anyways, So summarize the article, it. And this pattern will be right essay. it&amp;#39;s B tier, consume when time allows. I didn&amp;#39;t really know how to do it. a pattern means solving a problem. We&amp;#39;ll echo something and say you are, I go to church every Sunday. and I miss the sermon. Now, I&amp;#39;m going to take this, copy it. That&amp;#39;s the patterns that fabric we&amp;#39;ll use. and we created a file called System md, you&amp;#39;ll want to update your patterns. That way they&amp;#39;re never deleted, we&amp;#39;ll specify our directory, I should see sermon sensei right there. you can work on yours and keep iterating. Probably one of my favorite things, if we type in fabric help, We&amp;#39;re not going to go over all of them, We now have a context file. Now I&amp;#39;ve got two more features. prompter. Now, to understand that, as of the end of 22. As soon as the ai, I built a VM program over there. and I had been in AI for five, six years. but it became the content for Fabric. many iterations. It does things so well. expected. And that&amp;#39;s so fun. where it&amp;#39;s not about replacing humans, So I&amp;#39;m not stepping away and disengaging, I&amp;#39;m still reading massive number of books, quickly digest it. he designed these prompts, something, And that&amp;#39;s what this emulates. don&amp;#39;t do the AI stuff. Yeah, I think the way to use it is to use the context stuff And importantly, going back to your earlier point, So everything shouldn&amp;#39;t be a summary. you get the most muscle growth. Don&amp;#39;t take the weights out of the gym. or you could wait on that. Again, faster rate than you could before. to help you solve that problem. the week and then it&amp;#39;ll tell me, Keep doing that. see myself growing the fabric. it&amp;#39;s free, and then pipe that into fabric. through. So I have the recording transcribed. That&amp;#39;s a video coming soon. And again, system. So if you&amp;#39;re new to obsidian, And here&amp;#39;s my path to the directory. I&amp;#39;m just going to save this to a file. And then if I jump into my obsidian, Lemme know if you like this too. help of ai. I don&amp;#39;t know.