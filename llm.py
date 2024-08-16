

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


llm_openai = ChatOpenAI(model="gpt-4o-mini", api_key="api_key", max_tokens=4000, temperature=0.4)
llm_ollama = ChatOllama(model="deepseek-coder-v2:16b-lite-instruct-q8_0",  max_tokens=4000, temperature=0.4)
llm_anthropic = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    api_key = "api_key",
    temperature=0,
    max_tokens=4000)
