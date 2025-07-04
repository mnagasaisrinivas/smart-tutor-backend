from dotenv import load_dotenv
from langchain.llms.base import LLM
import requests, os
from typing import Optional, List

load_dotenv()

class OpenRouterLLM(LLM):
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    model = "mistralai/mistral-7b-instruct"

    @property
    def _llm_type(self) -> str:
        return "openrouter"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.openrouter_key}", "Content-Type": "application/json"},
            json={"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
        )
        return response.json()["choices"][0]["message"]["content"]