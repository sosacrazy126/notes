---
tags:
  - MCP_compliance
  - FastAPI
  - AI_integration
---
# create_coding_project

---

# PROJECT:
Create a production-ready MCP server using FastMCP and Python, integrating Mem0 for AI agent long-term memory capabilities.

# SUMMARY:
This project sets up a Model Context Protocol (MCP) server using the FastMCP library. It provides tools (`save_memory`, `get_all_memories`, `search_memories`) for AI agents to interact with Mem0, enabling long-term memory storage and retrieval. The server fetches configuration from environment variables, connects to Mem0 via a utility function, handles API calls with error checking, and supports both SSE and stdio transport methods for flexible client integration. Containerization is provided via Docker.

# STEPS:
1.  Clone the project repository to your local machine.
2.  Copy the `.env.example` file to `.env` for configuration.
3.  Fill in your environment variables, including API keys and database URL.
4.  Install the necessary Python dependencies using `uv pip install -e .`.
5.  Run the server using `uv run src/main.py` for SSE transport.
6.  Configure your MCP client to connect via SSE or stdio.

# STRUCTURE:

```
mcp-mem0/
├── .env.example
├── .venv/
├── Dockerfile
├── pyproject.toml
├── README.md
├── setup.sh
└── src/
    ├── __init__.py
    ├── main.py
    └── utils.py
```

# DETAILED EXPLANATION:
*   `.env.example`: Lists required environment variables for configuration.
*   `Dockerfile`: Defines instructions to build a container image for the application.
*   `pyproject.toml`: Specifies project metadata and dependencies for Python packaging using `uv`.
*   `README.md`: Provides setup instructions, features, and usage details for developers.
*   `setup.sh`: Automates project setup including dependency installation and environment file creation.
*   `src/__init__.py`: Makes the `src` directory a Python package.
*   `src/main.py`: Initializes the FastMCP server, defines tools, and manages the application lifecycle.
*   `src/utils.py`: Contains helper functions, like setting up the Mem0 client configuration.

# CODE:

**src/main.py**
```python
# File: src/main.py
# Purpose: Defines the FastMCP server, tools, and main execution logic.

from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv
from mem0 import Memory
import asyncio
import json
import os

# Import helper function to get the Mem0 client
from utils import get_mem0_client

# Load environment variables from .env file
load_dotenv()

# Define a default user ID for memory operations
DEFAULT_USER_ID = "user"

# Create a dataclass to hold application context, specifically the Mem0 client
@dataclass
class Mem0Context:
    """Context for the Mem0 MCP server."""
    mem0_client: Memory

# Define an async context manager for the server's lifespan
@asynccontextmanager
async def mem0_lifespan(server: FastMCP) -> AsyncIterator[Mem0Context]:
    """
    Manages the Mem0 client lifecycle. Initializes the client on startup.
    
    Args:
        server: The FastMCP server instance (unused in this specific lifespan function).
        
    Yields:
        Mem0Context: The context containing the initialized Mem0 client.
    """
    # Initialize the Mem0 client using the helper function
    mem0_client = get_mem0_client()
    
    try:
        # Yield the context object containing the client to the server
        yield Mem0Context(mem0_client=mem0_client)
    finally:
        # Perform any necessary cleanup here (Mem0 client doesn't require explicit cleanup)
        pass

# Initialize the FastMCP server instance
mcp = FastMCP(
    # Unique name for the MCP server
    "mcp-mem0",
    # Description of the server's purpose
    description="MCP server for long term memory storage and retrieval with Mem0",
    # Use the defined lifespan context manager
    lifespan=mem0_lifespan,
    # Get host from environment variable or default to 0.0.0.0
    host=os.getenv("HOST", "0.0.0.0"),
    # Get port from environment variable or default to 8050
    port=int(os.getenv("PORT", "8050"))
)        

# Define the 'save_memory' tool
@mcp.tool()
async def save_memory(ctx: Context, text: str) -> str:
    """Save information to your long-term memory.

    This tool is designed to store any type of information that might be useful in the future.
    The content will be processed and indexed for later retrieval through semantic search.

    Args:
        ctx: The MCP server provided context which includes the Mem0 client.
        text: The content to store in memory, including relevant details and context.
        
    Returns:
        A string indicating success or detailing the encountered error.
    """
    try:
        # Access the Mem0 client from the context
        mem0_client = ctx.request_context.lifespan_context.mem0_client
        # Format the input text as messages for Mem0
        messages = [{"role": "user", "content": text}]
        # Add the memory using the Mem0 client
        mem0_client.add(messages, user_id=DEFAULT_USER_ID)
        # Return a success message (truncated if text is long)
        return f"Successfully saved memory: {text[:100]}..." if len(text) > 100 else f"Successfully saved memory: {text}"
    except Exception as e:
        # Return an error message if saving fails
        return f"Error saving memory: {str(e)}"

# Define the 'get_all_memories' tool
@mcp.tool()
async def get_all_memories(ctx: Context) -> str:
    """Get all stored memories for the user.
    
    Call this tool when you need complete context of all previously stored memories.

    Args:
        ctx: The MCP server provided context which includes the Mem0 client.

    Returns: 
        A JSON formatted string list of all stored memories, or an error message.
    """
    try:
        # Access the Mem0 client from the context
        mem0_client = ctx.request_context.lifespan_context.mem0_client
        # Retrieve all memories for the default user
        memories = mem0_client.get_all(user_id=DEFAULT_USER_ID)
        # Extract the memory content from the results structure
        if isinstance(memories, dict) and "results" in memories:
            flattened_memories = [memory["memory"] for memory in memories["results"]]
        else:
            flattened_memories = memories
        # Return the memories as a JSON string
        return json.dumps(flattened_memories, indent=2)
    except Exception as e:
        # Return an error message if retrieval fails
        return f"Error retrieving memories: {str(e)}"

# Define the 'search_memories' tool
@mcp.tool()
async def search_memories(ctx: Context, query: str, limit: int = 3) -> str:
    """Search memories using semantic search.

    This tool should be called to find relevant information from your memory. Results are ranked by relevance.
    Always search your memories before making decisions to ensure you leverage your existing knowledge.

    Args:
        ctx: The MCP server provided context which includes the Mem0 client.
        query: Search query string describing what you're looking for. Can be natural language.
        limit: Maximum number of results to return (default: 3).
        
    Returns:
        A JSON formatted string list of relevant memories, or an error message.
    """
    try:
        # Access the Mem0 client from the context
        mem0_client = ctx.request_context.lifespan_context.mem0_client
        # Perform a search using the Mem0 client
        memories = mem0_client.search(query, user_id=DEFAULT_USER_ID, limit=limit)
        # Extract the memory content from the results structure
        if isinstance(memories, dict) and "results" in memories:
            flattened_memories = [memory["memory"] for memory in memories["results"]]
        else:
            flattened_memories = memories
        # Return the search results as a JSON string
        return json.dumps(flattened_memories, indent=2)
    except Exception as e:
        # Return an error message if search fails
        return f"Error searching memories: {str(e)}"

# Define the main asynchronous function to run the server
async def main():
    # Determine the transport method from environment variables (defaulting to 'sse')
    transport = os.getenv("TRANSPORT", "sse")
    # Run the server using the selected transport method
    if transport == 'sse':
        print(f"Starting MCP server with SSE transport on {mcp.host}:{mcp.port}")
        # Run the MCP server with SSE transport
        await mcp.run_sse_async()
    else:
        print("Starting MCP server with stdio transport")
        # Run the MCP server with stdio transport
        await mcp.run_stdio_async()

# Standard Python entry point
if __name__ == "__main__":
    # Run the main async function using asyncio
    asyncio.run(main())
```

**src/utils.py**
```python
# File: src/utils.py
# Purpose: Provides helper functions, primarily for initializing the Mem0 client.

from mem0 import Memory
import os

# Custom instructions for memory processing (Example, currently unused)
# These aren't being used right now but Mem0 does support adding custom prompting
# for handling memory retrieval and processing.
CUSTOM_INSTRUCTIONS = """
Extract the Following Information:  

- Key Information: Identify and save the most important details.
- Context: Capture the surrounding context to understand the memory's relevance.
- Connections: Note any relationships to other topics or memories.
- Importance: Highlight why this information might be valuable in the future.
- Source: Record where this information came from when applicable.
"""

# Function to configure and return a Mem0 client instance
def get_mem0_client():
    """
    Configures and initializes the Mem0 client based on environment variables.
    
    Reads configuration for LLM provider, API keys, models, embedding models,
    and vector store from environment variables.
    
    Returns:
        An initialized Mem0 Memory client instance.
    """
    # Retrieve LLM provider, API key, model, and embedding model from environment variables
    llm_provider = os.getenv('LLM_PROVIDER')
    llm_api_key = os.getenv('LLM_API_KEY')
    llm_model = os.getenv('LLM_CHOICE')
    embedding_model = os.getenv('EMBEDDING_MODEL_CHOICE')
    
    # Initialize the configuration dictionary
    config = {}
    
    # --- LLM Configuration ---
    # Configure based on the selected LLM provider
    if llm_provider == 'openai' or llm_provider == 'openrouter':
        # Set up configuration for OpenAI or compatible providers (like OpenRouter)
        config["llm"] = {
            "provider": "openai",  # Use the 'openai' provider setting in Mem0
            "config": {
                "model": llm_model,
                "temperature": 0.2,
                "max_tokens": 2000,
            }
        }
        
        # Set the appropriate API key environment variable if provided
        if llm_api_key:
            if llm_provider == 'openrouter':
                os.environ["OPENROUTER_API_KEY"] = llm_api_key
            elif not os.environ.get("OPENAI_API_KEY"): # Avoid overwriting existing key
                 os.environ["OPENAI_API_KEY"] = llm_api_key
            
        # Set base URL if provided (useful for OpenRouter or other compatible APIs)
        llm_base_url = os.getenv('LLM_BASE_URL')
        if llm_base_url:
            config["llm"]["config"]["base_url"] = llm_base_url

    elif llm_provider == 'ollama':
        # Set up configuration for Ollama
        config["llm"] = {
            "provider": "ollama",
            "config": {
                "model": llm_model,
                "temperature": 0.2,
                "max_tokens": 2000,
            }
        }
        
        # Set base URL for Ollama if provided (e.g., http://localhost:11434)
        llm_base_url = os.getenv('LLM_BASE_URL')
        if llm_base_url:
            config["llm"]["config"]["ollama_base_url"] = llm_base_url
    
    # --- Embedder Configuration ---
    # Configure based on the selected LLM provider (assuming embedder matches LLM provider)
    embedding_dims = 1536 # Default dimension
    if llm_provider == 'openai' or llm_provider == 'openrouter':
         # Determine embedding dimensions based on model choice (defaulting to text-embedding-3-small)
        chosen_embedding_model = embedding_model or "text-embedding-3-small"
        if chosen_embedding_model == "text-embedding-3-large":
            embedding_dims = 3072
        elif chosen_embedding_model == "text-embedding-ada-002":
            embedding_dims = 1536
        else: # Default to text-embedding-3-small dimensions
            embedding_dims = 1536

        config["embedder"] = {
            "provider": "openai", # Use the 'openai' provider setting in Mem0
            "config": {
                "model": chosen_embedding_model,
                "embedding_dims": embedding_dims
            }
        }

        # Set the API key if needed and not already set for OpenAI
        if llm_api_key and llm_provider == 'openai' and not os.environ.get("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = llm_api_key
            
        # Set base URL if provided (applies to both embedder and LLM)
        llm_base_url = os.getenv('LLM_BASE_URL')
        if llm_base_url:
            config["embedder"]["config"]["base_url"] = llm_base_url

    elif llm_provider == 'ollama':
        # Determine embedding dimensions based on model choice (defaulting to nomic-embed-text)
        chosen_embedding_model = embedding_model or "nomic-embed-text"
        # Add specific known Ollama model dimensions here if needed
        if "mxbai-embed-large" in chosen_embedding_model:
            embedding_dims = 1024
        else: # Default to nomic-embed-text dimensions
            embedding_dims = 768

        config["embedder"] = {
            "provider": "ollama",
            "config": {
                "model": chosen_embedding_model,
                "embedding_dims": embedding_dims
            }
        }
        
        # Set base URL for Ollama embedding if provided
        llm_base_url = os.getenv('LLM_BASE_URL')
        if llm_base_url:
            config["embedder"]["config"]["ollama_base_url"] = llm_base_url
    
    # --- Vector Store Configuration ---
    # Configure Supabase as the vector store provider
    db_url = os.environ.get('DATABASE_URL', '')
    if db_url: # Only add vector store config if DATABASE_URL is set
        config["vector_store"] = {
            "provider": "supabase", # Use Supabase
            "config": {
                "connection_string": db_url, # Get connection string from environment
                "collection_name": "mem0_memories", # Name of the table/collection
                "embedding_model_dims": embedding_dims # Use determined dimensions
            }
        }
    else:
        print("Warning: DATABASE_URL not set. Mem0 will use in-memory storage.")


    # --- Optional Custom Prompt ---
    # Uncomment the line below to add custom instructions for fact extraction
    # config["custom_fact_extraction_prompt"] = CUSTOM_INSTRUCTIONS
    
    # Print the final config for debugging (optional)
    # print("Mem0 Config:", config)

    # Create and return the Memory client instance using the generated configuration
    return Memory.from_config(config)
```

**pyproject.toml**
```toml
# File: pyproject.toml
# Purpose: Defines project metadata, dependencies, and build system information.

[project]
# Name of the Python package
name = "mem0-mcp-server"
# Version of the package
version = "0.1.0"
# Short description of the project
description = "MCP server for integrating long term memory into AI agents with Mem0"
# Specify the README file
readme = "README.md"
# Minimum required Python version
requires-python = ">=3.12"
# List of runtime dependencies
dependencies = [
    "httpx>=0.28.1",       # Required by mcp and mem0ai for HTTP requests
    "mcp[cli]>=1.3.0",     # MCP library with command-line interface features
    "mem0ai>=0.1.88",      # Mem0 AI client library
    "vecs>=0.4.5",         # Used by mem0ai for Supabase vector store interaction
    "python-dotenv>=1.0.1" # For loading environment variables from .env file
]

[project.scripts]
# Defines entry points for command-line scripts (if any)
# Example: mem0-mcp-server = src.main:main

[build-system]
# Specifies the build backend (standard setuptools)
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
# Automatically find packages under the 'src' directory
where = ["src"]

[tool.uv]
# Configuration specific to the 'uv' package manager (optional)
```

**Dockerfile**
```dockerfile
# File: Dockerfile
# Purpose: Defines the steps to build a Docker container image for the application.

# Use an official Python runtime as a parent image (slim version for smaller size)
FROM python:3.12-slim

# Argument to define the port the container will expose, defaulting to 8050
ARG PORT=8050

# Set the working directory inside the container
WORKDIR /app

# Install uv, a fast Python package installer and resolver
# Using pip here as uv is not pre-installed in the base image
RUN pip install uv

# Copy the project files into the container's working directory
# This includes pyproject.toml, src/, etc.
COPY . .

# Create a virtual environment within the container
RUN python -m venv .venv
# Activate the virtual environment for subsequent RUN commands (optional but good practice)
ENV PATH="/app/.venv/bin:$PATH"

# Install Python dependencies using uv into the virtual environment
# '-e .' installs the project in editable mode, including dependencies from pyproject.toml
RUN uv pip install -e .

# Make port ${PORT} available to the host machine
EXPOSE ${PORT}

# Define the command to run the application when the container starts
# Uses 'uv run' which manages the virtual environment activation automatically
# Assumes main.py is inside the 'src' directory
CMD ["uv", "run", "src/main.py"]
```

**.env.example**
```dotenv
# File: .env.example
# Purpose: Template for environment variables needed by the application. Copy to .env and fill in values.

# --- MCP Server Configuration ---

# The transport for the MCP server - either 'sse' or 'stdio' (defaults to SSE if left empty)
TRANSPORT=sse

# Host to bind to if using sse as the transport (defaults to 0.0.0.0)
# Leave empty or set to 0.0.0.0 to listen on all interfaces. Use 127.0.0.1 for localhost only.
HOST=0.0.0.0

# Port to listen on if using sse as the transport (defaults to 8050)
# Ensure this port is not already in use.
PORT=8050

# --- Mem0 Configuration ---

# The provider for your LLM ('openai', 'openrouter', or 'ollama')
# This determines how Mem0 interacts with the language model. Required.
LLM_PROVIDER=

# Base URL for the LLM API endpoint.
# OpenAI: https://api.openai.com/v1 (Usually not needed unless using Azure OpenAI)
# Ollama (example): http://localhost:11434 (No /v1 needed for Mem0's Ollama integration)
# OpenRouter: https://openrouter.ai/api/v1
LLM_BASE_URL=

# API Key for the LLM Provider.
# OpenAI: Find at https://platform.openai.com/api-keys
# OpenRouter: Find at https://openrouter.ai/keys
# Ollama: Usually not required unless you have specific auth configured.
LLM_API_KEY=

# The specific LLM model ID to use for processing memories.
# OpenAI example: gpt-4o-mini
# OpenRouter example: anthropic/claude-3.5-sonnet
# Ollama example: llama3:8b
LLM_CHOICE=

# The specific embedding model ID to use for storing memories. Should match LLM_PROVIDER.
# If left empty, reasonable defaults will be used based on the provider.
# OpenAI example: text-embedding-3-small (default) or text-embedding-3-large
# Ollama example: nomic-embed-text (default) or mxbai-embed-large
EMBEDDING_MODEL_CHOICE=

# --- Vector Store Configuration (Supabase Postgres) ---

# Full PostgreSQL connection URL for storing Mem0 vector embeddings. Required for persistent memory.
# If commented out or empty, Mem0 will use non-persistent in-memory storage.
# Format: postgresql://[user]:[password]@[host]:[port]/[database_name]
# Example Supabase (Transaction Pooler): postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:6543/postgres
# Example Local Postgres: postgresql://postgres:mypassword@localhost:5432/mydb
DATABASE_URL=

```

**README.md**
```markdown
# Mem0 MCP Server

This MCP server provides tools for AI agents to interact with Mem0 for long-term memory capabilities, following the [Model Context Protocol](https://modelcontextprotocol.io) specification by Anthropic.

## Features

*   **save_memory**: Store information in long-term memory with semantic indexing.
*   **get_all_memories**: Retrieve all stored memories for the default user.
*   **search_memories**: Find relevant memories using semantic search.
*   Supports SSE and stdio transport methods.
*   Configurable LLM and embedding models (OpenAI, OpenRouter, Ollama).
*   Uses Supabase/Postgres or in-memory vector store via Mem0.
*   Containerized deployment using Docker.

## Prerequisites

*   Python 3.12+
*   `uv` (recommended for installation: `pip install uv`)
*   API keys for your chosen LLM provider (OpenAI, OpenRouter) if applicable.
*   PostgreSQL database URL (e.g., from Supabase) if using persistent vector storage.
*   Docker (optional, for containerized deployment).

## Installation

### Using uv (Recommended)

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url> mcp-mem0-server
    cd mcp-mem0-server
    ```

2.  **Create and configure the environment file:**
    ```bash
    cp .env.example .env
    # Edit .env with your specific configuration (API keys, DB URL, etc.)
    nano .env
    ```

3.  **Install dependencies:**
    ```bash
    uv pip install -e .
    ```

### Using Docker

1.  **Clone the repository and configure `.env`** as described above.

2.  **Build the Docker image:**
    ```bash
    # You can change the port exposed by the container if needed
    docker build -t mem0-mcp-server --build-arg PORT=8050 .
    ```

## Running the Server

### SSE Transport (Default)

Ensure `TRANSPORT=sse` (or leave it empty) and `PORT` / `HOST` are set correctly in your `.env` file.

**With `uv`:**
```bash
uv run src/main.py
```
The server will start, typically listening on `http://0.0.0.0:8050/sse`.

**With Docker:**
```bash
# Make sure your .env file is configured
docker run -p 8050:8050 --env-file .env mem0-mcp-server
```
The server runs inside the container, accessible on port `8050` of your host machine.

### Stdio Transport

Ensure `TRANSPORT=stdio` in your `.env` file.

With stdio, the MCP *client* application manages the server process directly. You don't run the server manually beforehand. Configure your client as shown in the Integration section.

## Integration with MCP Clients

Configure your AI agent or MCP client application to use this server.

### SSE Configuration Example

```json
{
  "mcpServers": {
    "mem0Memory": {
      "transport": "sse",
      "url": "http://localhost:8050/sse" // Adjust host/port if needed
    }
  }
}
```

### Stdio Configuration Example

```json
{
  "mcpServers": {
    "mem0Memory": {
      "transport": "stdio",
      // Path to your python executable (ideally within the venv)
      "command": "/path/to/your/mcp-mem0-server/.venv/bin/python",
      // Arguments to pass to the command
      "args": ["/path/to/your/mcp-mem0-server/src/main.py"],
      // Environment variables required by the server process
      "env": {
        "TRANSPORT": "stdio",
        "LLM_PROVIDER": "...", // Copy necessary vars from your .env
        "LLM_API_KEY": "...",
        "LLM_CHOICE": "...",
        "DATABASE_URL": "..."
        // Add other required environment variables here
      }
    }
  }
}
```
*Note: Ensure the paths in `command` and `args` are correct for your setup.*

## Available Tools

*   **`save_memory(text: str)`**: Saves the provided text to the long-term memory associated with the default user.
*   **`get_all_memories()`**: Retrieves all memories stored for the default user as a JSON string.
*   **`search_memories(query: str, limit: int = 3)`**: Searches stored memories using the query and returns the top `limit` relevant results as a JSON string.

## Environment Variables

*   `TRANSPORT`: `sse` or `stdio`. Determines the communication method (default: `sse`).
*   `HOST`: Host address for SSE server (default: `0.0.0.0`).
*   `PORT`: Port for SSE server (default: `8050`).
*   `LLM_PROVIDER`: `openai`, `openrouter`, or `ollama`. Selects the language model provider.
*   `LLM_BASE_URL`: Optional override for the LLM API endpoint.
*   `LLM_API_KEY`: API key for the selected LLM provider (if required).
*   `LLM_CHOICE`: Specific model ID for the LLM (e.g., `gpt-4o-mini`).
*   `EMBEDDING_MODEL_CHOICE`: Specific model ID for embeddings (e.g., `text-embedding-3-small`). Defaults based on provider.
*   `DATABASE_URL`: PostgreSQL connection string for persistent memory storage (required for persistence).

## License

MIT
```

**setup.sh**
```bash
#!/bin/bash
# File: setup.sh
# Purpose: Automates the initial setup of the project environment.

echo "Starting project setup..."

# Variables
PROJECT_DIR=$(pwd)
VENV_DIR=".venv"
REQ_FILE="pyproject.toml" # Using pyproject.toml for dependencies with uv
ENV_EXAMPLE=".env.example"
ENV_FILE=".env"

# Check if uv is installed
if ! command -v uv &> /dev/null
then
    echo "Error: 'uv' command not found."
    echo "Please install uv first:"
    echo "pip install uv"
    exit 1
fi

echo "Creating virtual environment using Python's venv module..."
# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
    echo "Virtual environment created at $VENV_DIR"
else
    echo "Virtual environment already exists at $VENV_DIR"
fi

# # Activate virtual environment - Note: Activation is generally for the current shell,
# # uv handles activation implicitly when run. This line is more for informational purpose.
# echo "Attempting to activate virtual environment (manual activation might be needed)..."
# source $VENV_DIR/bin/activate

echo "Installing dependencies using uv..."
# Install dependencies using uv
uv pip install -e .
if [ $? -ne 0 ]; then
    echo "Error installing dependencies. Please check $REQ_FILE and network connection."
    exit 1
fi
echo "Dependencies installed successfully."

echo "Checking for $ENV_FILE..."
# Create .env file from example if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    echo "Copying $ENV_EXAMPLE to $ENV_FILE..."
    cp $ENV_EXAMPLE $ENV_FILE
    echo "$ENV_FILE created. Please configure it with your settings."
else
    echo "$ENV_FILE already exists. Skipping creation."
fi

echo "-------------------------------------"
echo "Setup complete!"
echo "Next steps:"
echo "1. Edit the '$ENV_FILE' file with your configuration (API keys, DB URL, etc.)."
echo "2. Run the server using: uv run src/main.py (for SSE transport)"
echo "   or configure your MCP client for stdio transport."
echo "-------------------------------------"

exit 0
```

# SETUP:
```bash
#!/bin/bash
# Clones repository (replace placeholder), runs setup script, and informs user.

REPO_URL="<your-repository-url-here>" # Replace with actual repository URL
PROJECT_NAME="mcp-mem0-server"

echo "Cloning repository: $REPO_URL"
git clone "$REPO_URL" "$PROJECT_NAME"

if [ $? -ne 0 ]; then
    echo "Error cloning repository. Please check the URL and your permissions."
    exit 1
fi

cd "$PROJECT_NAME"

echo "Running setup script (setup.sh)..."
chmod +x setup.sh
./setup.sh

if [ $? -ne 0 ]; then
    echo "Setup script failed. Please check the output above for errors."
    exit 1
fi

echo "Project setup finished in directory: $(pwd)"
echo "Remember to configure your .env file before running the server."
```
*(Save the above script as `create_project.sh`, replace `<your-repository-url-here>`, make it executable (`chmod +x create_project.sh`), and run it: `./create_project.sh`)*

# TAKEAWAYS:
1.  The server integrates Mem0, providing persistent long-term memory using LLMs and vector stores.
2.  FastMCP enables rapid development of robust MCP servers with built-in tooling support.
3.  Configuration via environment variables (`.env`) enhances security and deployment flexibility.
4.  Support for both SSE and stdio transport allows integration with various MCP clients.
5.  Helper functions in `utils.py` encapsulate client initialization and improve code organization.
6.  Dockerization simplifies dependency management and ensures consistent deployment environments.
7.  The provided tools (`save_memory`, `get_all_memories`, `search_memories`) offer core memory operations.
8.  Error handling is included in tool definitions for more robust operation.

# SUGGESTIONS:
1.  Implement user-specific memory by passing a `user_id` parameter to tools instead of using `DEFAULT_USER_ID`.
2.  Add more sophisticated error handling, perhaps logging errors to a file or external service.
3.  Explore advanced Mem0 features like memory summarization or custom fact extraction prompts.
4.  Introduce unit and integration tests using `pytest` to ensure tool functionality and reliability.
5.  Consider adding authentication/authorization layers if exposing the server more broadly.
6.  Implement pagination for the `get_all_memories` tool to handle very large memory stores gracefully.
7.  Add a tool for deleting specific memories based on ID or content.
8.  Investigate alternative vector database integrations supported by Mem0 if Supabase isn't suitable.


