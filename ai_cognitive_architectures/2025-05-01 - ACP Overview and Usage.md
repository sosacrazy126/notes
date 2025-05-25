---
nexus: nexus-ai-chat-importer
provider: chatgpt
aliases: ACP Overview and Usage
conversation_id: 68138cf0-a6c0-8009-a782-6ebdf3958195
create_time: 05/01/2025 at 8:02 AM
update_time: 05/01/2025 at 8:04 AM
tags:
  - agent-communication-protocol
  - multi_agent_system
  - API_integration
---

# Title: ACP Overview and Usage

Created: 05/01/2025 at 8:02 AM
Last Updated: 05/01/2025 at 8:04 AM


### User, on 05/01/2025 at 8:02 AM;
> what is and explain its usage https://github.com/i-am-bee/acp
<!-- UID: 266814d7-1608-4630-825a-e6f05002911a -->


#### ChatGPT, on 05/01/2025 at 8:02 AM;
>> The [Agent Communication Protocol (ACP)](https://github.com/i-am-bee/acp) is an open standard designed to facilitate seamless communication between AI agents across diverse frameworks and platforms. Developed under the BeeAI project and governed by the Linux Foundation AI & Data initiative, ACP aims to unify agent interactions through a standardized RESTful API, supporting synchronous, asynchronous, and streaming exchanges. citeturn0search0
>> 
>> ### Key Concepts
>> 
>> - **Agent Detail**: Describes an agent's capabilities, including its name, description, metadata, and status, enabling discovery and composition without revealing internal implementations.
>> 
>> - **Run**: Represents a single execution instance of an agent with specific inputs, accommodating both synchronous and streaming outputs.
>> 
>> - **Message**: The fundamental communication unit, comprising a sequence of ordered components that form a complete, structured, and multimodal information exchange.
>> 
>> - **MessagePart**: Individual content units within a `Message`, such as text, images, or JSON, which collectively enable structured, multimodal communication.
>> 
>> - **Await**: Allows agents to pause and request information from the client, resuming once the necessary input is received, thus supporting interactive exchanges.
>> 
>> ### Usage Overview
>> 
>> ACP provides SDKs in both Python and TypeScript, facilitating the creation and interaction with ACP-compliant agents. The Python SDK includes server implementations, client libraries, and model definitions. A typical workflow involves:
>> 
>> 1. **Project Initialization**:
>>    Use `uv` to set up the project environment:
>>    ```bash
>>    uv init --python '>=3.11' my_acp_project
>>    cd my_acp_project
>>    uv add acp-sdk
>>    ```
>> 
>> 
>> 2. **Agent Creation**:
>>    Develop an agent, such as an "echo agent" that returns received messages:
>>    ```python
>>    # agent.py
>>    import asyncio
>>    from collections.abc import AsyncGenerator
>>    from acp_sdk.models import Message
>>    from acp_sdk.server import Context, RunYield, RunYieldResume, Server
>> 
>>    server = Server()
>> 
>>    @server.agent()
>>    async def echo(
>>        input: list[Message], context: Context
>>    ) -> AsyncGenerator[RunYield, RunYieldResume]:
>>        """Echoes everything"""
>>        for message in input:
>>            await asyncio.sleep(0.5)
>>            yield {"thought": "I should echo everything"}
>>            await asyncio.sleep(0.5)
>>            yield message
>> 
>>    server.run()
>>    ```
>> 
>> 
>> 3. **Server Execution**:
>>    Run the agent server:
>>    ```bash
>>    uv run agent.py
>>    ```
>> 
>> 
>> 4. **Agent Verification**:
>>    Confirm the agent's availability:
>>    ```bash
>>    curl http://localhost:8000/agents
>>    ```
>> 
>> 
>> 5. **Agent Interaction**:
>>    Send a message to the agent and receive a response:
>>    ```bash
>>    curl -X POST http://localhost:8000/runs \
>>      -H "Content-Type: application/json" \
>>      -d '{
>>            "agent_name": "echo",
>>            "input": [
>>              {
>>                "parts": [
>>                  {
>>                    "content": "Howdy!",
>>                    "content_type": "text/plain"
>>                  }
>>                ]
>>              }
>>            ]
>>          }'
>>    ```
>> 
>> 
>> 6. **Client Development**:
>>    Create a client to interact with the agent:
>>    ```python
>>    # client.py
>>    import asyncio
>>    from acp_sdk.client import Client
>>    from acp_sdk.models import Message, MessagePart
>> 
>>    async def example() -> None:
>>        async with Client(base_url="http://localhost:8000") as client:
>>            run = await client.run_sync(
>>                agent="echo",
>>                input=[
>>                    Message(
>>                        parts=[MessagePart(content="Howdy to echo from client!!", content_type="text/plain")]
>>                    )
>>                ],
>>            )
>>            print(run.output)
>> 
>>    if __name__ == "__main__":
>>        asyncio.run(example())
>>    ```
>> 
>> 
>> 7. **Client Execution**:
>>    Run the client script:
>>    ```bash
>>    uv run client.py
>>    ```
>> 
>> 
>> This setup demonstrates the ease of creating and interacting with agents using ACP, promoting interoperability and streamlined communication across diverse AI systems.
>> 
>> For more detailed information and advanced usage, refer to the [ACP GitHub repository](https://github.com/i-am-bee/acp) and the [official documentation](https://agentcommunicationprotocol.dev/). 
<!-- UID: a77a7546-9345-4b7f-bba0-ed0c90baf494 -->

---


### User, on 05/01/2025 at 8:04 AM;
> always respond with clear direct no fluff response  and formatt in a paragh block with code snippets below it this is so i can play audio aloud without having to listen to code snippet parts 
<!-- UID: 9127ceed-21bf-4d13-9020-c397a5b8fa41 -->


#### ChatGPT, on 05/01/2025 at 8:04 AM;
>> The Agent Communication Protocol (ACP) is an open standard developed by BeeAI and IBM to enable seamless communication between AI agents across diverse frameworks and platforms. It defines a standardized RESTful API that supports synchronous, asynchronous, and streaming interactions, allowing agents to exchange multimodal messages without exposing their internal implementations. ACP is designed to facilitate interoperability, scalability, and efficient interactions among AI agents, promoting automation, collaboration, and integration with various systems. citeturn0search0
>> 
>> **Quickstart Guide:**
>> 
>> **1. Initialize your project:**
>> 
>> ```bash
>> uv init --python '>=3.11' my_acp_project
>> cd my_acp_project
>> ```
>> 
>> **2. Add the ACP SDK:**
>> 
>> ```bash
>> uv add acp-sdk
>> ```
>> 
>> **3. Create an agent (`agent.py`):**
>> 
>> ```python
>> import asyncio
>> from collections.abc import AsyncGenerator
>> from acp_sdk.models import Message
>> from acp_sdk.server import Context, RunYield, RunYieldResume, Server
>> 
>> server = Server()
>> 
>> @server.agent()
>> async def echo(input: list[Message], context: Context) -> AsyncGenerator[RunYield, RunYieldResume]:
>>     for message in input:
>>         await asyncio.sleep(0.5)
>>         yield {"thought": "I should echo everything"}
>>         await asyncio.sleep(0.5)
>>         yield message
>> 
>> server.run()
>> ```
>> 
>> **4. Start the ACP server:**
>> 
>> ```bash
>> uv run agent.py
>> ```
>> 
>> **5. Verify your agent is available:**
>> 
>> ```bash
>> curl http://localhost:8000/agents
>> ```
>> 
>> **6. Run the agent via HTTP:**
>> 
>> ```bash
>> curl -X POST http://localhost:8000/runs \
>>   -H "Content-Type: application/json" \
>>   -d '{
>>         "agent_name": "echo",
>>         "input": [
>>           {
>>             "parts": [
>>               {
>>                 "content": "Howdy!",
>>                 "content_type": "text/plain"
>>               }
>>             ]
>>           }
>>         ]
>>       }'
>> ```
>> 
>> **7. Create a client (`client.py`):**
>> 
>> ```python
>> import asyncio
>> from acp_sdk.client import Client
>> from acp_sdk.models import Message, MessagePart
>> 
>> async def example() -> None:
>>     async with Client(base_url="http://localhost:8000") as client:
>>         run = await client.run_sync(
>>             agent="echo",
>>             input=[
>>                 Message(
>>                     parts=[MessagePart(content="Howdy to echo from client!!", content_type="text/plain")]
>>                 )
>>             ],
>>         )
>>         print(run.output)
>> 
>> if __name__ == "__main__":
>>     asyncio.run(example())
>> ```
>> 
>> **8. Run the ACP client:**
>> 
>> ```bash
>> uv run client.py
>> ```
>> 
>> 
>> This setup demonstrates how to create and interact with agents using ACP, promoting interoperability and streamlined communication across diverse AI systems. citeturn0search0 
<!-- UID: 4f5de24c-e9ec-4f0d-8227-9cae5178d562 -->

---


