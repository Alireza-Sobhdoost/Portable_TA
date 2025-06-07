# Portable_TA

Portable_TA is a flexible and extensible Telegram bot designed to simplify and automate technical analysis workflows, and to provide intelligent, context-aware responses to user queries.

## Overview

Portable_TA connects Telegram users with advanced AI-powered search and reasoning capabilities. It leverages Nomic AI embeddings to perform Retrieval-Augmented Generation (RAG) searches over course materials or documents, enabling users to get accurate, context-rich answers to their questions. When you ask a question, one AI model retrieves and answers your query, while another dedicated reasoning model creates a concise summary of the ongoing conversation, allowing the bot to maintain short-term memory and context within the limits of the model.

## Motivation

TA stands for Teaching Assistant. In many academic environments, students often need to ask their TAs about exercises, assignments, or course questions. However, TAs are not always available, and some students may feel uncomfortable reaching out to them directly. Portable_TA addresses this by providing an AI-driven assistant that possesses the knowledge and expertise of an instructor and is always accessible. This system helps ensure that students can get the support they need, whenever they need it, in a comfortable and reliable manner.

## What is Portable_TA?

- **Telegram Bot:** This project is a Telegram bot connected to a Large Language Model (LLM).
- **RAG-powered Answers:** The LLM uses Retrieval-Augmented Generation (RAG) techniques, powered by Nomic AI embeddings, to search reference materials (such as textbooks like "FLA") and answer user questions with relevant, up-to-date context.
- **Contextual Memory:** The bot remembers the conversation for a short period, with a dedicated reasoning model generating conversation summaries within the context window allowed by the LLM.
- **Technical Analysis Automation:** In addition to LLM features, the bot offers automation for technical analysis, making it ideal for developers, traders, and analysts seeking a portable solution for algorithmic trading, data analysis, or signal processing tasks.

## Features

- **RAG Search with Nomic AI Embeddings:** Accurate answers from designated books or documents via retrieval-augmented generation.
- **Short-term Memory:** Maintains short-term conversation history for more natural interaction, using a reasoning model for summaries.
- **Modular Architecture:** Easily extend or customize components to suit your workflow.
- **Portable:** Designed to run on various platforms with minimal dependencies.
- **Automation:** Streamline repetitive technical analysis and data processing operations.
- **Integration Friendly:** Easily integrate with other tools and APIs.

## Installation

Clone the repository:
```bash
git clone https://github.com/Alireza-Sobhdoost/Portable_TA.git
cd Portable_TA
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Detailed usage instructions and examples will be provided soon. Please refer to the source code and comments for now.

## Markdown Decoding

This project uses [`telegramify-markdown`](https://github.com/sudoskys/telegramify-markdown.git) for decoding and processing Markdown content. This allows for seamless conversion and formatting of messages, especially when integrating with Telegram bots or messaging services.

## Future Work

Currently, Portable_TA is designed to operate on a non-agentic (non-autonomous) search capabilities. In the future, we aim to generalize the bot so it can perform agentic searches across the entire Computer Engineering (CE) curriculum. This would enable users to query and receive intelligent responses spanning multiple courses, leveraging autonomous multi-document retrieval and reasoning.

## Contributing

Contributions are welcome! Feel free to fork the repository, create a new branch, and submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [telegramify-markdown](https://github.com/sudoskys/telegramify-markdown.git) for Markdown decoding utilities.
