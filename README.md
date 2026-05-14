# Simple LLM Chatbot with Ollama / HuggingFace, LangChain & Streamlit

A lightweight, open-source chatbot built with two interchangeable backends — **Ollama** (local inference) and **HuggingFace** (pipeline-based inference) — wired together with **LangChain** and served through a **Streamlit** web UI.

![llm_chatbot](https://github.com/tonytsoi/LLM_chatbot/blob/main/llm_chatbot.jpg?raw=true)

---

## Features

- Chat with **Llama 3.2** entirely on your own machine — no external API keys required
- Two drop-in backends: swap between Ollama and HuggingFace
- Persistent **chat history** within a session (maintained via Streamlit session state)
- **Streaming** responses rendered word-by-word in the browser
- Configurable generation parameters (temperature, max tokens)

---

## Project Structure

```text
LLM_chatbot/
├── chat_ollama.py        # Backend: Ollama (local model server)
├── chat_huggingface.py   # Backend: HuggingFace Transformers pipeline
├── llm_chatbot.jpg       # Screenshot
└── README.md
```

---

## Prerequisites

- Python 3.9+
- `pip` (or a virtual-environment manager such as `conda` / `venv`)

### For `chat_ollama.py`

- [Ollama](https://ollama.com) installed and running locally
- The Llama 3.2 model pulled:

  ```bash
  ollama pull llama3.2
  ```

### For `chat_huggingface.py`

- A [HuggingFace account](https://huggingface.co) with access granted to [meta-llama/Llama-3.2-1B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct)
- `HF_TOKEN` environment variable set to your HuggingFace access token:

  ```bash
  export HF_TOKEN=hf_...        # macOS / Linux
  set HF_TOKEN=hf_...           # Windows Command Prompt
  $env:HF_TOKEN="hf_..."        # Windows PowerShell
  ```

- A GPU is recommended for reasonable inference speed; CPU-only inference is supported but slow

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/tonytsoi/LLM_chatbot.git
cd LLM_chatbot

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install streamlit langchain-ollama langchain-huggingface transformers accelerate
```

---

## Usage

### Option A — Ollama backend

Make sure the Ollama service is running (`ollama serve`), then:

```bash
streamlit run chat_ollama.py
```

### Option B — HuggingFace backend

```bash
streamlit run chat_huggingface.py
```

Both commands open the chat interface at `http://localhost:8501` in your browser.

---

## Configuration

Both scripts expose the following generation parameters near the top of `generate_response()`:

| Parameter | Default | Description |
| --- | --- | --- |
| `temperature` | `0.3` | Controls response randomness; lower = more deterministic |
| `num_predict` / `max_new_tokens` | `2048` | Maximum number of tokens in each response |

To use a different model, update the `model` / `model_id` variable in the relevant script.

For GPU acceleration in the HuggingFace backend, uncomment the `device="cuda"` line inside the `pipeline(...)` call in [chat_huggingface.py](chat_huggingface.py).

---

## How It Works

```text
User input (Streamlit)
        │
        ▼
 generate_response()
        │
        ├─ Ollama path  →  ChatOllama  →  local Ollama server  →  Llama 3.2
        │
        └─ HF path      →  HuggingFacePipeline → ChatHuggingFace → Llama 3.2
        │
        ▼
Streaming output (st.write_stream)
        │
        ▼
Chat history appended to st.session_state
```

LangChain's chat model interface (`model.invoke()`) provides a unified API across both backends, making it straightforward to swap in any other supported model provider.

---

## Dependencies

| Package | Purpose |
| --- | --- |
| `streamlit` | Web UI and session state management |
| `langchain-ollama` | LangChain integration for Ollama |
| `langchain-huggingface` | LangChain integration for HuggingFace |
| `transformers` | HuggingFace model loading and inference pipeline |
| `accelerate` | Efficient model loading (required by `transformers`) |

---

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).
