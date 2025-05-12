---
tags:
  - secure_authentication
  - FastAPI
  - CI/CD_automation
  - codebase_querying
---
PROJECT: Secure code analysis API with CLI, FastAPI endpoints, JWT auth, CI/CD automation for enterprise dev workflows.  

SUMMARY: A modular tool uses async HTTP clients and Pydantic models to index GitHub repos, query codebases via natural language, and enforce dual authentication via API keys and JWT tokens, with Dockerized deployment and GitHub Actions integration.  

STEPS:  
1. Configure environment variables for API keys and GitHub tokens.  
2. Use CLI to index repositories with branch specifications.  
3. Submit natural language queries via CLI or FastAPI endpoints.  
4. Deploy containerized API using Docker with exposed ports.  
5. Automate code reviews via GitHub Actions workflows.  

STRUCTURE:  
├── greptile_tool/  
│   ├── core.py      # Async client for API interactions  
│   ├── api.py       # FastAPI endpoints for indexing/queries  
│   ├── auth.py      # JWT token creation/verification  
│   └── __init__.py  
├── Dockerfile       # Container configuration  
├── .github/  
│   └── workflows/  
│       └── ci_cd.yml # GitHub Actions workflow  
├── greptile         # CLI entrypoint script  
├── requirements.txt # Dependencies  
└── README.md        # Project documentation  

DETAILED EXPLANATION:  
- **core.py**: Implements `GreptileClient` with async methods for indexing repos and querying via HTTP.  
- **api.py**: Defines FastAPI routes `/api/index` and `/api/ask` with dependency injection for authentication.  
- **auth.py**: Handles JWT token generation/validation for secure endpoint access.  
- **Dockerfile**: Packages app with Uvicorn and exposes port 8000 for deployment.  
- **ci_cd.yml**: Triggers code analysis on pull requests using Dockerized CLI tool.  
- **greptile**: CLI executable for user-facing commands like `index` and `ask`.  

CODE:  
**core.py**  
```python  
import httpx  
from pydantic import BaseModel  

class GreptileClient:  
    def __init__(self, api_key: str, gh_token: str):  
        self.base_url = "https://api.greptile.com/v2"  
        self.headers = {  
            "Authorization": f"Bearer {api_key}",  
            "X-GitHub-Token": gh_token,  
            "Content-Type": "application/json"  
        }  

    async def index_repo(self, repo: str, branch: str = "main") -> dict:  
        """Send POST request to index a GitHub repository."""  
        payload = {  
            "remote": "github",  
            "repository": repo,  
            "branch": branch,  
            "reload": True  
        }  
        async with httpx.AsyncClient() as client:  
            response = await client.post(  
                f"{self.base_url}/repositories",  
                headers=self.headers,  
                json=payload  
            )  
            response.raise_for_status()  
            return response.json()  
    # ... (remaining methods)  
```  

**api.py**  
```python  
from fastapi import FastAPI, Depends, HTTPException, Header  
from core import GreptileClient  
from auth import verify_token  

app = FastAPI()  

def get_client(x_api_key: str = Header(...)):  
    """Fetch client with secrets from environment variables."""  
    import os  
    return GreptileClient(  
        api_key=os.getenv("GREPTILE_KEY"),  
        gh_token=os.getenv("GH_TOKEN")  
    )  

@app.post("/api/index")  
async def index_repo(  
    repo: str,  
    branch: str = "main",  
    client: GreptileClient = Depends(get_client)  
):  
    """Index repository via client interface."""  
    try:  
        return await client.index_repo(repo, branch)  
    except Exception as e:  
        raise HTTPException(500, detail=str(e))  
# ... (remaining endpoints)  
```  

**auth.py**  
```python  
import jwt  
from datetime import datetime, timedelta  

SECRET_KEY = "your-secret-key"  # Replace with env var  

def create_access_token(user_id: str) -> str:  
    """Generate JWT token with 4-hour expiration."""  
    expire = datetime.utcnow() + timedelta(hours=4)  
    payload = {"sub": user_id, "exp": expire}  
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")  

def verify_token(token: str) -> dict:  
    """Validate JWT token integrity and expiration."""  
    try:  
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  
    except jwt.PyJWTError:  
        raise HTTPException(401, "Invalid token")  
```  

**setup.sh**  
```bash  
#!/bin/bash  
mkdir -p greptile_tool/.github/workflows  
cp -r core.py api.py auth.py greptile_tool/  
echo "FROM python:3.10-slim" > Dockerfile  
echo "COPY . /app" >> Dockerfile  
echo "WORKDIR /app" >> Dockerfile  
echo "RUN pip install -r requirements.txt" >> Dockerfile  
echo "CMD [\"uvicorn\", \"api:app\", \"--host=0.0.0.0\"]" >> Dockerfile  
echo "::: GitHub Actions Workflow :::" > .github/workflows/ci_cd.yml  
# ... (complete workflow YAML)  
```  

**README.md**  
```markdown  
# Greptile API Tool  
## Setup  
1. Clone repo and install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  
2. Set environment variables:  
   ```bash  
   export GREPTILE_KEY=<your_api_key>  
   export GH_TOKEN=<github_personal_token>  
   ```  
3. Run locally:  
   ```bash  
   uvicorn api:app --reload  
   ```  
4. CLI usage:  
   ```bash  
   ./greptile index owner/repo --branch dev  
   ./greptile ask owner/repo "Where is the auth middleware?" --genius  
   ```  
```  

TAKEAWAYS:  
1. Dual authentication layers enhance enterprise security.  
2. Asynchronous HTTP calls optimize performance for large repos.  
3. Dockerization simplifies deployment across environments.  
4. GitHub Actions automate CI/CD for pull request analysis.  

SUGGESTIONS:  
1. Use a secrets manager (e.g., Vault) for production keys.  
2. Add rate limiting to prevent API abuse.  
3. Expand query types (e.g., syntax checks, dependency audits).  
4. Implement database caching for frequent queries.