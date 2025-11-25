# Portable_TA

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LLM](https://img.shields.io/badge/Powered%20by-LLM-FF6F00?style=for-the-badge&logo=openai&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0A0E1B?style=for-the-badge&logo=uvicorn&logoColor=white)

Portable_TA is a flexible, API-first LLM service designed to provide intelligent, context-aware responses to user queries. It supports **Retrieval-Augmented Generation (RAG)** for accurate answers from documents or course materials and offers a dual-memory system for coherent conversations.

## Overview

Portable_TA exposes an **OpenAI-compatible API**, allowing seamless integration with frontends like **OpenWebUI** or other tools. The bot uses Nomic AI embeddings to perform RAG searches, combining **long-term memory** (user data and history) with **short-term memory** (current session reasoning) to provide context-rich answers.

## Motivation

TA stands for Teaching Assistant. In many academic environments, students often need to ask their TAs about exercises, assignments, or course questions. However, TAs are not always available, and some students may feel uncomfortable reaching out to them directly. Portable_TA addresses this by providing an AI-driven assistant that possesses the knowledge and expertise of an instructor and is always accessible. This system helps ensure that students can get the support they need, whenever they need it, in a comfortable and reliable manner.

### Architecture: FastAPI and Uvicorn

The application is built on a modern and robust Python stack:

*   **FastAPI**: This is the web framework that powers the API. It handles defining the routes (like `/v1/chat/completions`), validating incoming requests, and formatting the responses. It's the "brain" of the service, providing the logic and structure.
*   **Uvicorn**: This is an ASGI (Asynchronous Server Gateway Interface) server. It acts as the "engine" that runs the FastAPI application. Uvicorn listens for incoming HTTP traffic on a specified host and port (e.g., `0.0.0.0:9000`) and passes the requests to FastAPI for processing.

**Flow:**
`Client (OpenWebUI) -> Uvicorn (Server) -> FastAPI (App Logic) -> LLM/RAG Core`

## API Version and Endpoints

Portable_TA uses **API v1** with the following endpoints:

- **Base URL:** `http://<server_ip>:9000/v1`
- **Endpoints:**
  - `/v1/models` → List available models
  - `/v1/chat/completions` → Send user messages and receive LLM responses
  - `/v1/give_apikey` → Issue or validate API keys (optional for private usage)

### Example Request

```bash
curl -X POST "http://<server_ip>:9000/v1/chat/completions" \
-H "Content-Type: application/json" \
-H "X-OpenWebUI-User-ID: PT-1234" \
-d '{
    "model": "PortableTA",
    "messages": [{"role": "user", "content": "Explain a^n b^n language"}],
    "max_tokens": 300
}'
```

## Connecting to OpenWebUI

To connect your Portable_TA server to the OpenWebUI frontend, follow these steps:

1.  Open the OpenWebUI interface in your browser.
2.  Navigate to the **Admin Panel**.
3.  Go to **Settings** -> **Connections**.
4.  Click on **Add Connection** and select the **OpenAI Compatible API** option.
5.  In the "API URL" field, enter the address of your running Portable_TA server:
    ```
    http://<your_server_ip>:9000/v1
    ```
6.  If your setup requires an API key, you can add it in the "API Key" field. Otherwise, you can leave it blank.
7.  Save the connection. You can now start chatting with your Portable_TA model through the OpenWebUI interface.

## Features

-   **RAG-Powered Answers**: Retrieve context-rich responses from documents and textbooks.
-   **Dual Memory System**: Long-term user memory + short-term session memory for coherent reasoning.
-   **OpenAI-Compatible API**: Works with any client or frontend that supports OpenAI API specifications.
-   **Modular & Extensible**: Easily integrate with other tools, widgets, or custom pipelines.
-   **Widget Support**: Compatible with OpenWebUI chat widgets for immediate deployment.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Alireza-Sobhdoost/Portable_TA.git
    cd Portable_TA
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the API server:**
    ```bash
    uvicorn MainLLMApp:app --host 0.0.0.0 --port 9000
    ```

## Usage

Once the API server is running, you can:

-   Send messages through the `/v1/chat/completions` endpoint.
-   Use the OpenWebUI widget to chat with the model in a browser interface.
-   Issue or validate API keys via `/v1/give_apikey` for multi-user setups.

## Future Work

-   Add agentic capabilities to enable autonomous multi-document reasoning.
-   Support additional frontends and embedding sources.
-   Expand dual-memory logic to improve context retention over long sessions.

## Contributing

Contributions are welcome! Fork the repository, create a branch, and submit a pull request.

## License

This project is licensed under the MIT License.
