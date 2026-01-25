from typing import Any

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


class Agent:
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        base_url: str | None = None,
        system_prompt: str | None = None,
        tools: list[BaseTool] = [],
    ) -> None:
        self.tools = tools
        self.llm = ChatOpenAI(
            model=model,
            base_url=base_url,
            api_key=SecretStr(api_key),
        )
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt,
        )

    async def get_response(self, messages: list) -> dict[str, Any] | Any:
        try:
            response = await self.agent.ainvoke({"messages": messages})
            return response
        except Exception as e:
            print(f"Error in agent execution: {e}")
            raise

    def get_response_sync(self, messages: list) -> dict[str, Any] | Any:
        try:
            response = self.agent.invoke({"messages": messages})
            return response
        except Exception as e:
            print(f"Error in agent execution: {e}")
            raise
