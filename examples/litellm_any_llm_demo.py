import os
from enum import StrEnum

import litellm
from dotenv import load_dotenv

load_dotenv()


class LLMProvider(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"


def get_api_key(provider: LLMProvider) -> str:
    env_keys = {
        LLMProvider.OPENAI: "OPENAI_API_KEY",
        LLMProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
        LLMProvider.DEEPSEEK: "DEEPSEEK_API_KEY",
        LLMProvider.GEMINI: "GEMINI_API_KEY",
    }
    key = os.getenv(env_keys[provider])
    if not key:
        raise ValueError(f"API key for {provider} not found in .env file.")
    return key


def call_llm(provider: LLMProvider, model: str, prompt: str) -> str:
    api_key = get_api_key(provider)

    base_urls = {
        LLMProvider.OPENAI: "https://api.openai.com/v1",
        LLMProvider.ANTHROPIC: "https://api.anthropic.com/v1",
        LLMProvider.DEEPSEEK: "https://api.deepseek.com/v1",
        LLMProvider.GEMINI: "https://generativelanguage.googleapis.com/v1",
    }

    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            api_key=api_key,
            base_url=base_urls.get(provider),
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


def demo_openai():
    print("\n--- OpenAI (gpt-4o) ---")
    result = call_llm(
        LLMProvider.OPENAI,
        "gpt-4o",
        "Explain what LiteLLM is in one sentence.",
    )
    print(result)


def demo_anthropic():
    print("\n--- Anthropic (claude-sonnet-4-20250514) ---")
    result = call_llm(
        LLMProvider.ANTHROPIC,
        "claude-sonnet-4-20250514",
        "Explain what LiteLLM is in one sentence.",
    )
    print(result)


def demo_deepseek():
    print("\n--- DeepSeek (deepseek-chat) ---")
    result = call_llm(
        LLMProvider.DEEPSEEK,
        "deepseek-chat",
        "Explain what LiteLLM is in one sentence.",
    )
    print(result)


def demo_gemini():
    print("\n--- Gemini (gemini-2.0-flash) ---")
    result = call_llm(
        LLMProvider.GEMINI,
        "gemini-2.0-flash",
        "Explain what LiteLLM is in one sentence.",
    )
    print(result)


def main():
    demo_openai()
    demo_anthropic()
    demo_deepseek()
    demo_gemini()


if __name__ == "__main__":
    main()
