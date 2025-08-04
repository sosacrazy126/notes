---
tags:
  - UI_integration
  - async_programming
  - Streamlit
---
```markdown
# Step-by-Step Guide to Creating an Async Streamlit UI for RA.AID

## Core Requirements:
Execute agent workflows (research/planning/implementation) asynchronously to prevent blocking the UI. Deliver agent outputs in real-time using WebSocket streams. Provide a centralized dashboard to configure agent pipelines and monitor progress.

## Implementation Plan:

### 1. **UI Architecture Design** *(Base: `/webui/app.py`)*
- Initialize core state variables using session_state:
```python
def initialize_session_state():
    if 'ws_connected' not in st.session_state:
        st.session_state.ws_connected = False
    # Add queue management and agent config state
```
- Create environment status sidebar mirroring `/webui/app.py`:
```python
render_environment_status():
    st.sidebar.markdown("### API Connectivity 🌐")
    for provider in get_api_providers():
        status = "🟢" if provider.is_configured() else "🔴"
        st.sidebar.text(f"{status} {provider.name}")
 ```
Include dashboard elements for agent pipeline visualization.

### 2. **WebSocket Communication** *(Base: `/ra_aid/server/server.py`)*
- Implement thread-safe message streaming using producer/consumer pattern:
```python
async def ws_connection(websocket):
    output_queues = {}
    while active:
        payload = await websocket.receive_json()
        if payload['type'] == 'execute':
            task_id = uuid4()
            thread = Thread(
                target=background_agent,
                args=(payload['task'], task_id, output_queues[task_id])
            )
            thread.start()
```
- Standardize output format for agent messages:
```json
{
  "type": "stream",
  "data": {
    "agent_type": "research",
    "incremental_output": "Analyzing [....]",
    "progress": 45
  }
}
```

### 3. **Agent Management System**
- Build modular agent control:
```python
def execute_pipeline(task_spec):
    research_output = run_agent(AgentType.RESEARCH, task_spec)
    plan = planning_agent.generate_plan(research_output)
    run_implementation_agent(plan)
```
- Implement optional configurations:
```python
@dataclass
class AgentConfig:
    use_expert_model: bool = False
    enable_web_search: bool = True
    provider: APIProvider = OpenAI()
```

### 4. **Error Handling & Monitoring**
- Centralized error logging with tracebacks:
```python
def log_agent_failure(agent, error):
    st.error(f"Agent {agent.type} failed: {error}")
    with st.expander("Show Full Traceback"):
        st.code(get_full_traceback())
```
- UI health indicators for API providers:
```python
def health_check():
    statuses = check_api_endpoints()
    if any(s.is_error() for s in statuses.values()):
        st.warning(" degraded services")
```

## Execution Considerations:
- **Concurrency:** Use `threading.Event` for thread lifecycle management
- **Performance:** Cache intermediate agent outputs to Redis
- **Configuration:** Support Tavily/OpenAI/etc through provider plugins

## Deliverables Structure:
1. FSD architecture diagram with component dependencies
2. Session state management flowchart
3. WebSocket protocol specification
4. Agent execution lifecycle overview
5. Performance benchmarking (500ms/agentmsg target)
```

This revised prompt format provides a scaffold with explicit technical specifications using code snippets, establishes clear dependency relationships, and incorporates configuration options from the original codebase. The modular structure encourages implementation in component-based chunks while maintaining system-wide consistency.