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



## Architecture: FastAPI + Uvicorn

The application is built on a modern Python stack:

- **FastAPI**: Handles API routes, request validation, and response formatting.  
- **Uvicorn**: ASGI server that runs FastAPI, managing incoming HTTP requests.

**Flow:**

Client (OpenWebUI) -> Uvicorn (Server) -> FastAPI (App Logic) -> LLM/RAG Core

swift
Copy code

---

## API Version and Endpoints

- **Base URL:** `http://<server_ip>:9000/v1`  
- **Endpoints:**
  - `/v1/models` → List available models
  - `/v1/chat/completions` → Send user messages and receive LLM responses
  - `/v1/give_apikey` → Issue or validate API keys (optional for private usage)

## Installation
### Option 1: Docker (recommended)
You can download the Docker.tar from releases or build it from the Container folder.

#### Run the container

```bash
docker run -d \
  -e NOMIC_API_KEY=your_key \
  -e CEREBRAS_API_KEY=your_key \
  -p 9000:9000 \
  portable-ta
```
#### Issue an API key

```bash
curl -X POST http://<ServerIp>:9000/v1/give_apikey \
     -H "Content-Type: application/json" \
     -d '{"key": ""}'
```
#### Connect to OpenWebUI

- Open OpenWebUI in your browser → Admin Panel → Settings → Connections → Add Connection → OpenAI Compatible API

- API URL: http://<ServerIp>:9000/v1

- Add API Key you've issued

- Save connection

### Tip: Turn off “auto-title” and “flowing question” features in OpenWebUI for better memory management.

### Option 2: Local Python Setup
Clone the repository

```bash
git clone https://github.com/Alireza-Sobhdoost/Portable_TA.git
cd Portable_TA
```
#### Install dependencies

```bash
pip install -r requirements.txt
```
#### Start the API server

```bash
uvicorn MainLLMApp:app --host 0.0.0.0 --port 9000
```
## Features

- RAG-Powered Answers: Retrieve context-rich responses from documents and textbooks.

- Dual Memory System: Long-term + short-term memory for coherent reasoning.

- OpenAI-Compatible API: Works with any client or frontend that supports OpenAI API specs.

- Code Execution Tool: Can execute Python code through an agent.

- Modular & Extensible: Easily integrate with other tools or pipelines.

- Widget Support: Compatible with OpenWebUI chat widgets for immediate deployment.
## Usage
- Run the container with Docker or set up locally.

- Issue an API key.

- Send chat requests via /v1/chat/completions.

- Connect OpenWebUI for interactive sessions.

## Future Work
- Enable autonomous multi-document reasoning (agentic capabilities).

- Support additional frontends and embedding sources.

- Expand dual-memory logic for better long-session context retention.

## Contributing
Contributions are welcome! Fork the repository, create a branch, and submit a pull request.

##License
This project is licensed under the MIT License.