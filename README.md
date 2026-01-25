# ai-sidekick

Personal AI Assistant with knowledge base integration

## Overview
Open-source solution for creating a personal AI assistant with:
- RAG baseline
- knowledge base management via QDrant and python
- simple docker-based deployment
- telegram bot dialog window

_This solution is recommended for testing and experimenting with various RAG approaches._
## Requirements
- Docker and Docker Compose
- [UV](https://github.com/astral-sh/uv) Python package manager (`pip install uv`)

---

## Quick Start

### prepare configs

properly fill `configs.py` and `.env` files (see the configurations section below)

### start services

```bash
docker compose up -d --build
```

### init uv

```bash
uv venv .venv && uv sync
```

### Initialize knowledge base

generate data to .json file
```bash
uv run data/generate_data.py
```

upsert generated data to a QDrant
```bash
uv run data/upload_data.py
```

check upserted data in your collection (http://localhost:6333/dashboard#/collections)

### Engoy your personal AI-assistant at telegram bot!


## Configurations
Project configured via `configs.py` and `.env` files in `app/`, `bot/`, `data/` directories

_To make filling in environment variables easier, you can find example of .env files in the project root `env_examples`, as well as recommendations in the notes below_

### app/configs.py
```env
# main LLM (must support tools) for generating answer (LLM must support google/gemini-2.0-flash-001)
MODEL
# the API key of the provider you are using (openrouter etc)
MODEL_API_KEY 
# provider's API URL (https://openrouter.ai/api/v1) 
MODEL_BASE_URL
# URL for qdrant (http://qdrant:6333)
QDRANT_URL
# Collection of knowledges in QDrant (my_collection)
QDRANT_COLLECTION_NAME=my_collection
# Prompt for LLM before starting a dialogue
MASTER_PROMPT
# Encoder-model inside container (/tmp/ai_sidekick/app/frida)
ENCODER
# the number of documents that will be found by semantic search from the total document pool (the more documents, the larger this window should be) (10 is good for start)
TOP_K_SEMANTIC_POINTS
```

### bot/configs.py
```env
# URL for core API (http://client:8000 by default it is inside the container)
CLIENT_URL
# The token the bot's father gives you after creating a bot
TELEGRAM_BOT_TOKEN
# List of telegram users that can use your bot (this is your telegram username's after @) 
WHITELIST
```

### data/configs.py
```env
# Path for knowledge base (data/kbase by default)
KBASE_PATH
# Path for .json file with generated payloads (data/payloads by default)
FILE_PATH
# main LLM for generating payloads (tngtech/deepseek-r1t2-chimera:free)
MODEL
# the API key of the provider you are using (openrouter etc)
MODEL_API_KEY 
# provider's API URL (https://openrouter.ai/api/v1) 
MODEL_BASE_URL
# Encoder-model (must be the same model as for app -- app/frida)
ENCODER
# URL for qdrant (http://localhost:6333)
QDRANT_URL
# Collection of knowledges in QDrant (my_collection)
QDRANT_COLLECTION_NAME=my_collection
# Prompt for LLM for generating payloads properly
MASTER_PROMPT
```

## Notes

1. You can easily create a telegram bot using [@BotFather](https://telegram.me/BotFather)

2. Currently, the knowledge base is assumed to be a set of folders containing .md files. These easily can be edited and viewed using [Obsidian](https://obsidian.md/)

3. To update data after editing your knowledge base -- clear your [QDrant collection](http://localhost:6333/dashboard#/collections) and reinitialize knowledge base

4. You can experiment with different models (in the case of [openrouter](https://openrouter.ai/) it's quite simple: just select the desired model from the web catalog) by changing .env and re-running `docker compose up --build`

5. frida was added to the repository for simplicity, as many users may experience problems when using or downloading it. You can use any other encoder model according to your needs and discretion.

6. Using Python, you can easily experiment with new mcp-tools to suit your needs `app/tools`

7. This solution is primarily designed for the Russian knowledge base. To rebuild it in your language, it would be advisable to make the appropriate adjustments: 
    1. modify the master prompts
    2. change language in retrieve tool
    3. change the encoder model








