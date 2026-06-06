from collections import defaultdict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

from agent import Agent
from tools.retrieve import retrieve

import configs


app = FastAPI()


class QueryRequest(BaseModel):
    user_id: int
    user_query: str


class ChatResponse(BaseModel):
    answer: str
    context: str
    retrieved_docs: list


user_context: dict = defaultdict(list)
user_dialog: dict = defaultdict(int)
agent = Agent(
    api_key=configs.MODEL_API_KEY,
    base_url=configs.MODEL_BASE_URL,
    model=configs.MODEL,
    tools=[retrieve],
)


async def generate_answer(request: QueryRequest) -> tuple[str, str, list]:
    try:
        if not user_context[request.user_id]:
            user_context[request.user_id].append(
                SystemMessage(content=configs.MASTER_PROMPT)
            )

        user_context[request.user_id].append(HumanMessage(content=request.user_query))
        response = await agent.get_response(user_context[request.user_id])

        context = ""
        retrieved_docs = []
        for message in response.get("messages", []):
            if hasattr(message, 'content') and isinstance(message, ToolMessage):
                context = message.content
                if hasattr(message, 'artifact'):
                    retrieved_docs = message.artifact
                break

        answer = response["messages"][-1].content

        if response["messages"][-1].invalid_tool_calls:
            return "Error calling tool. Try fix the prompt, tool or change llm", "", []

        if not answer:
            return "Llm's response is empty, something went wrong.", "", []

        user_context[request.user_id].append(AIMessage(content=answer))
        return answer, context, retrieved_docs

    except Exception as e:
        print(f"error: {e}")
        user_context[request.user_id].pop()
        return f"an error occurred while processing your request: {str(e)}", "", []


@app.post("/chat")
async def chat(request: QueryRequest):
    try:
        answer, context, retrieved_docs = await generate_answer(request)
        user_dialog[request.user_id] += 1

        if user_dialog[request.user_id] >= 3:
            answer = f"{answer} \n 🔄context reset🔄"
            user_dialog[request.user_id] = 0

        print(f"{answer=}")
        print(f"{context=}")
        print(f"{retrieved_docs=}")

        return ChatResponse(
            answer=answer,
            context=context,
            retrieved_docs=retrieved_docs,
        ).model_dump()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clear_context")
async def clear_context(request: QueryRequest):
    user_context.pop(request.user_id, None)

    return {"answer": "the context was successfully cleared!"}


@app.get("/ping")
async def ping():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="debug",
    )
