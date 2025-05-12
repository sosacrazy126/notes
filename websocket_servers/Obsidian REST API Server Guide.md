---
tags:
  - REST_API
  - API_integration
  - secure_authentication
---
# OVERVIEW

What It Does: A REST API server for Obsidian, exposing vault content and functionality via HTTP endpoints for automation and integration.  

Why People Use It: Enables programmatic access to notes, tags, and metadata, supporting workflows like custom dashboards, API-driven automation, and external tool integration.  

# HOW TO USE IT  

Most Common Syntax: `obsidian-mcp-rest start --vault /path/to/vault --port 8080`  

# COMMON USE CASES  

For Fetching Note Content: `GET /api/notes/{noteName}`  
For Listing All Tags: `GET /api/tags`  
For Creating a New Note: `POST /api/notes`  
For Watching Vault Changes: `GET /api/watch`  
For Executing Obsidian Commands: `POST /api/command`  

# MOST IMPORTANT AND USED OPTIONS AND FEATURES  

`--vault [PATH]`: Specifies the Obsidian vault directory to expose via the API.  
`--port [PORT]`: Sets the server port (default often 8080).  
`--api-key [KEY]`: Enforces API token authentication for security.  
`--host [ADDRESS]`: Binds the server to a specific IP address for network access.  
`--watch`: Enables real-time vault change monitoring via WebSocket.  
`--debug`: Adds verbose logging for troubleshooting.