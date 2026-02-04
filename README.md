# Jyotish AI - Vedic Astrology Agent

![Jyotish AI Banner](assets/banner.png)

Jyotish AI is a premium, AI-powered Vedic Astrology application that blends ancient wisdom with modern technology. It provides detailed, mystical, and personalized astrological readings using a LangGraph-based agentic workflow and the Groq inference engine.

## 🌟 Features

-   **Deep Vedic Insights**: Generates readings based on Indian Vedic Astrology principles (Nakshatras, Dashas, Rashis).
-   **Comprehensive Reports**: Covers 12+ aspects including Personality, Career, Relationships, Karmic Debts, and Age-wise predictions.
-   **Instant Responses**: Implements intelligent caching (LRU) to provide instant results for repeated queries.
-   **Premium UI**: A "Mystic" themed interface built with Tailwind CSS, featuring animations, drifting stars, and glassmorphism.
-   **High Performance**: Powered by `FastAPI` for the backend and `Groq` (Llama 3) for ultra-fast inference.
-   **Agentic Workflow**: Uses `LangGraph` to manage state and prompt engineering logic.

## 🏗️ Architecture

```mermaid
graph TD
    User[User (Browser)] -->|POST /api/horoscope| API[FastAPI Backend]
    
    subgraph "Backend System"
        API -->|Invoke| Agent[LangGraph Agent]
        
        Agent -->|Check| Cache[LRU Cache]
        Cache -- Hit --> Agent
        Cache -- Miss --> Generator[Prompt Generator]
        
        Generator -->|Context + Prompt| LLM[Groq Inference Engine]
        LLM -->|Stream Response| Agent
    end
    
    Agent -->|JSON Result| API
    API -->|Formatted Response| User
    
    style User fill:#f9f,stroke:#333,stroke-width:2px
    style API fill:#bbf,stroke:#333,stroke-width:2px
    style Agent fill:#dfd,stroke:#333,stroke-width:2px
    style LLM fill:#ff9,stroke:#333,stroke-width:2px
```

## 🚀 Getting Started

### Prerequisites

-   Python 3.12+
-   Docker (optional)
-   Kubernetes/Helm (optional)
-   Groq API Key (Get one at [console.groq.com](https://console.groq.com))

### Local Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/jyotish-ai.git
    cd jyotish-ai
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    # source .venv/bin/activate # Linux/Mac
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Copy `.env.example` to `.env` and add your API key:
    ```bash
    cp .env.example .env
    # Edit .env and set GROQ_API_KEY=your_key_here
    ```

5.  **Run the application**:
    ```bash
    python main.py
    ```
    Open [http://localhost:8000](http://localhost:8000) in your browser.

## 🐳 Docker Deployment

1.  **Build the image**:
    ```bash
    docker build -t jyotish-ai .
    ```

2.  **Run the container**:
    ```bash
    docker run -p 8000:8000 -e GROQ_API_KEY=your_key_here jyotish-ai
    ```

## ☸️ Kubernetes Deployment

Deploy using the included Helm chart:

```bash
# Install the chart
helm install jyotish-ai ./helm/astro-chart --set env.GROQ_API_KEY=your_key_here
```

## 🛠️ Technology Stack

-   **Frontend**: HTML5, Tailwind CSS, JavaScript (Vanilla), Marked.js
-   **Backend**: Python, FastAPI, Uvicorn
-   **AI/LLM**: LangChain, LangGraph, Groq (Llama 3)
-   **DevOps**: Docker, Kubernetes, Helm

## 📄 License

This project is licensed under the MIT License.
