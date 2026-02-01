# ai-sidekick

Personal AI Assistant with knowledge base integration

## Overview
Open-source solution for creating a personal AI assistant with:
- RAG (Retrieval Augmented Generation) baseline
- knowledge base management via Qdrant and python
- simple docker-based deployment
- telegram bot dialog window

_This solution is recommended for testing and experimenting with various RAG approaches._
## Requirements
- [Docker](https://www.docker.com/get-started/) and Docker Compose
- [UV](https://github.com/astral-sh/uv) Python package manager (`pip install uv`)

---

## Start

### 1. Prepare configs and encoder

Project configured via `configs.py` and `.env` files in `app/`, `bot/`, `data/` directories. You shod **properly** fill it.

suggested pipeline:
1. use ready-made templates from `env_examples` directory
2. from [openrouter](https://openrouter.ai/) register and get API key (_you can try with free models first_)
3. from [@BotFather](https://telegram.me/BotFather) create and get bot API key
4. copy each `.env` file to the appropriate directory (`/app`, `/bot`, `/data`)
5. download encoder `frida.zip` from [here](https://drive.google.com/file/d/1uLCgPd7doJtO8ICcOcZqocLJ2juJU3Oz/view?usp=drive_link) and extract it to `app/encoders/` or use it via [HiggingFace](https://huggingface.co/ai-forever/FRIDA/tree/main)

_For more detailed configuration of environment variables see configurations section below_
### 2. Start docker services

```bash
docker-compose up -d --build
```
or (for debug)

```bash
docker-compose up --build
```
### 3. Initialize knowledge base

install dependencies
```bash
uv venv .venv && uv sync
```

generate data to .json file
```bash
uv run data/generate_data.py
```

upsert generated data to a QDrant
```bash
uv run data/upload_data.py
```

check upserted data in your [collection](http://localhost:6333/dashboard#/collections)

### 4. Enjoy your personal AI-assistant at telegram bot!


## Configurations

### app/configs.py
```env
# main LLM (must support tools) for generating answer (google/gemini-2.0-flash-001)
MODEL
# the API key of the provider you are using (openrouter etc)
MODEL_API_KEY 
# provider's API URL (https://openrouter.ai/api/v1) 
MODEL_BASE_URL
# URL for qdrant (http://qdrant:6333)
QDRANT_URL
# Collection of knowledges in QDrant (my_collection)
QDRANT_COLLECTION_NAME
# System prompt for LLM before starting a dialogue
MASTER_PROMPT
# Encoder-model inside container (/tmp/ai_sidekick/app/encoders/frida)
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
QDRANT_COLLECTION_NAME
# Prompt for LLM for generating payloads properly
MASTER_PROMPT
```

## Notes

1. You can experiment with different configs, llms, encoders or tools. Just properly change it and restart containers `docker-compose restart` _(and also `docker compose up` attaching for debug)_. In the case of llms, it's quite easy via [openrouter](https://openrouter.ai/). (_Please note that openrouter is a cloud platform and there is no guarantee that your data will be completely anonymous. They're working hard to ensure this, though, and you can minimize this risk_).

2. The quality of semantic search is greatly affected by the choice of encoder model. In this implementation, the frida model is selected by default. You can work with the model locally by downloading it from [here](https://drive.google.com/file/d/1uLCgPd7doJtO8ICcOcZqocLJ2juJU3Oz/view?usp=drive_link) or use it via [HiggingFace](https://huggingface.co/ai-forever/FRIDA/tree/main) directly. _(The use of the model locally is due to the fact that some users may experience problems when using it via HF or same way)_. You can use any other encoder model according to your needs and discretion.

3. Currently, the knowledge base is assumed to be a set of folders containing `.md` files. These easily can be edited and viewed using [Obsidian](https://obsidian.md/). _By the way everything is limited only by your imagination._

4. To update data after editing your knowledge base: clear your [Qdrant collection](http://localhost:6333/dashboard#/collections) and reinitialize it.

5. You can easily create a telegram bot using [@BotFather](https://telegram.me/BotFather).

6. This solution is primarily designed for the Russian knowledge base. To rebuild it in your language, it would be advisable to make the appropriate adjustments:
    1. change the encoder model
    2. change docs language in retrieve tool
    3. modify the master prompts







