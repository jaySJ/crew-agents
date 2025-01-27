# AI agents using Crew AI agentic framework
Three quick examples of creating sequential and collaborative AI agents.

- Use Ollama for a locally hosted solution
- Uses recently released Deepseek R1 model
- Uses tools (website scraping and web search) and human-in-the-loop interactions

# To run

1. Install Ollama
2. Pull LLM models
   ```ollama pull deepseek-r1:8b```
   ```ollama pull llama3.2```
3. Install dependencies ```pip install -r requirements.txt ```
4. Run each module file

# Key Learnings
### Agents as an alternative to fine-tuning
- Fine-tuning LLMs for custom decision-making tasks is both resource intensive and can diminish the models’ generalization capabilities
- Agentic frameworks are AI agent architectures that use tool calling and orchestration for AI applications. 
- Agentic systems use planning, iterative refinement, reflection and other control mechanisms to fully leverage the model’s built-in ‘reasoning’ capabilities to complete tasks end-to-end.

### Options for building Agents
**[LangGraph](https://www.langchain.com/langgraph)**
- Stateful multi-actor apps (with LLMs)
- Directed Acyclic Graphs where each node represents a specific task or function
- Sutiable for complex workflows that require advanced memory features, error recovery, and human-in-the-loop interactions [https://www.galileo.ai/blog/mastering-agents-langgraph-vs-autogen-vs-crew ]
   
**[CrewAI](https://www.crewai.com/)**

- A crew embodies a collective ensemble of agents collaborating to accomplish a predefined set of tasks
- Each crew defines the strategy for task execution, agent execution and the overall workflow. 
- Crews have several attributes that help assemble agents with complementary roles and tools, assign tasks and select a process that dictates their execution order and interaction
- Robustness and graceful recovery when agents fail
- Allows tool calling
   
**[AutoGen 0.4](https://microsoft.github.io/autogen/dev//index.html)**
- Treats workflows as conversations between agents
- Intuitive for users who prefer interactive ChatGPT-like interfaces.
- Supports code executors, function callers, perform complex tasks autonomously
- Highly customizable
- Extend agents with additional components and define custom workflows

### Options for multi-agent collaboration
- Sequential
- Hierarchical
- Collaborative (direct acyclic graph)

 ### Key principles/concepts when designing AI agents
 Get LLM to engage itself in the thinking process – kay idea of an agent. It can ask questions and answer them by itself to get better outcomes.

1. Role playing
    - Agents do better when they role play
2. Focus
    - Focus on specific topics, tools, amount of content they get sent, and tasks they are trying to accomplish – having an agent do a broad role or many topics leads to dilution (losing important information) and hallucinations – even with larger context windows
    - Do not rely on one agent to do it all – similar to Single Responsibility Principle in object oriented design ('S' in SOLID principles)
3. Tools
    - Giving too many tools also has a similar problem – confusing / overloading – have trouble chosing a tool – especially if you give them smaller models – not able to distinguish 
4. Cooperation
    - Conversation and feedback and role-playing provides better results
5. Guardrails
    - Fuzzy inputs / transformation /outputs - 
    - Don’t want to take too long, or stuck trying to use same tool, 
    - Crew implement guardrails – to get reliable consistent results
6. Memory 
    - Remembers what the agent has done previously when making new decisions – and learns from it
    - Short-term (shared context – during execution – learnings shared between agents)
    - Long-term – stored in database locally – ppersists even after crew finishes.  Self critiques to improve for next tasks, learning from previous executions.
    - Entity memory - short-lived - remembers the specific entitties or subjects (think, named entity recognition in NLP) – for example stores a company name as an entity in the database.

## Examples
[Blog post writing agent](blog-post-writer-agent.png)
[Custormer support agent](customer_support_agent_output.png)
