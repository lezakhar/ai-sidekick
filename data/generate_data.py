import json

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from app.agent import Agent

from langchain_core.messages import HumanMessage

import configs

agent = Agent(
    model=configs.MODEL,
    api_key=configs.MODEL_API_KEY,
    base_url=configs.MODEL_BASE_URL,
    system_prompt=configs.MASTER_PROMPT,
)


def _find_knowledges(vault_path) -> list[dict]:
    vault_root = Path(vault_path)
    knowledge_list = []

    for md_file in vault_root.rglob("*.md"):
        rel_path = md_file.relative_to(vault_root)
        context = " > ".join(rel_path.parts[:-1])
        content = md_file.read_text(encoding="utf-8")

        context_string = (
            f"File: {rel_path}\Context: {context}\nContent:\n{content}\n---"
        )

        knowledge_list.append(
            {
                "text": context_string,
                "path": str(rel_path),
            }
        )

    return knowledge_list


def _generate_knowledges(raw_text: str) -> str:
    messages = [HumanMessage(content=raw_text)]
    response = agent.get_response_sync(messages)
    knowledges_json = response["messages"][-1].content

    return knowledges_json


def _generate_payloads(knowledge: dict) -> list[dict]:
    knowledges_json = _generate_knowledges(raw_text=knowledge["text"])

    knowledges_json = knowledges_json.replace("\\n", "")
    knowledges_json = knowledges_json.replace("*", "")
    knowledges_json = knowledges_json.replace("```json", "")
    knowledges_json = knowledges_json.replace("```", "")

    payloads = json.loads(knowledges_json)

    return payloads


def generate():
    knowledge_list = _find_knowledges(configs.KBASE_PATH)

    all_payloads = []

    for knowledge in knowledge_list:
        try:
            payloads = _generate_payloads(knowledge)

            for payload in payloads:
                payload["source_file"] = knowledge["path"]

            all_payloads.extend(payloads)

            print(
                f"✓ File processed: {knowledge['path']} - added {len(payloads)} payloads"
            )

        except Exception as e:
            print(f"✗ Error processing file {knowledge['path']}: {str(e)}")
            continue

    output_file = f"{configs.FILE_PATH}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_payloads, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done! Total generated {len(all_payloads)} payloads")
    print(f"📁 The result is saved to a file: {output_file}")

    return all_payloads


if __name__ == "__main__":
    generate()
