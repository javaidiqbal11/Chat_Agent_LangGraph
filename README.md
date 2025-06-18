# 🤖 Chat Agent with LangGraph

This project demonstrates how to build **multi-step, memory-enabled conversational agents** using [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), and [FastAPI](https://fastapi.tiangolo.com/) with optional [Gradio](https://gradio.app/) interface for testing.

It is designed for **multi-agent reasoning and orchestration**, ideal for AI-powered customer support or information retrieval systems.

---

## 📁 Project Structure

```
Chat_Agent_LangGraph/
│
├── agents/
│   └── tools.py              # Custom tools/functions used by the agents
│
├── graphs/
│   └── agent_executor.py     # LangGraph flow: graph construction & execution logic
│
├── prompts/
│   └── prompts.py            # Prompt templates for agents
│
├── app.py                    # FastAPI backend for external access
├── ui.py                     # Optional Gradio frontend interface
├── .env                      # Environment variables (e.g., API keys)
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation (this file)
```

---

## 🚀 Features

* 🔁 **LangGraph**-powered agent orchestration
* 🧠 Memory-enabled context handling
* ⚙️ Custom agent tools and chains
* 🌐 FastAPI for backend API access
* 🧪 Gradio UI for interactive testing (optional)
* 🔐 Secure configuration using `.env` variables

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/javaidiqbal11/Chat_Agent_LangGraph.git
cd Chat_Agent_LangGraph
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

> If you face any issues with `llama_index`, `langgraph`, or `langchain`, ensure you are using Python 3.10+.

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
touch .env
```

Add the following:

```
OPENAI_API_KEY=your_openai_key_here
```

---

## ▶️ Running the App

### 1. Start FastAPI Backend

```bash
uvicorn app:app --reload
```

This will start the API server at `http://127.0.0.1:8000`.

### 2. (Optional) Start Gradio UI

```bash
python ui.py
```

This launches a Gradio interface for testing the chat interface visually.

---

## 🧠 Agent Architecture (LangGraph)

The system uses **LangGraph** to build a multi-node agent graph. Each node may represent:

* A specific **task agent** (e.g., summarizer, QA bot)
* A **router** to choose the next action
* A **memory retriever** or document chunker

The `graphs/agent_executor.py` defines:

* The **graph nodes** (tools, agents, decisions)
* The **edges** (transitions based on output)
* The **runner** to execute a conversational session

---

## 🛠️ Custom Tools

Defined in `agents/tools.py`, these allow the agent to:

* Search knowledge
* Query documents
* Call APIs
* Fetch summaries

Each tool is integrated using LangChain’s `Tool` abstraction.

---

## 🧪 Prompt Templates

Located in `prompts/prompts.py`, these define:

* Base agent prompt
* Specialized prompts (e.g., retrieval, QA)
* System-level instructions

These templates are loaded dynamically into LangGraph agents.

---

## 📂 API Endpoints

### `POST /chat`

Runs the agent graph on a given user message.

**Request Example:**

```json
{
  "message": "What are the features of the JazzCash app?"
}
```

**Response Example:**

```json
{
  "response": "The JazzCash app includes bill payment, mobile top-ups, QR payments..."
}
```

---

## 💡 Use Cases

* Customer support agents
* Interactive document Q\&A
* AI-powered assistants with memory
* Product/service FAQ bots

---

## 🧪 Sample .env (For Testing)

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🔍 Troubleshooting

* **ModuleNotFoundError**: Ensure all packages in `requirements.txt` are installed.
* **LangGraph warnings**: Follow updated import paths and LangChain best practices.
* **API timeout**: Use async FastAPI calls and avoid long agent execution times.

---

## 🧱 Built With

* [LangGraph](https://github.com/langchain-ai/langgraph)
* [LangChain](https://github.com/langchain-ai/langchain)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Gradio](https://www.gradio.app/)
* [OpenAI](https://platform.openai.com/)

---

## 🙌 Acknowledgments

Thanks to the LangChain and LangGraph teams for enabling composable multi-agent systems. This repo builds on community ideas and best practices for AI agents.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
