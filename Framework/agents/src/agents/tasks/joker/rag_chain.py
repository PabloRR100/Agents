"""
Joker Chain which uses a RAG approach to generate jokes.
"""
from pydantic import BaseModel

from agents.core.chains import build_chain


PROMPT_TEMPLATE = (
    """
    You are a comedian and your task is to make people laugh. 
    
    Generate the funnies joke given the this topic {topic}.
    Use maximum {max_words} words to tell the joke. 
    Use only the following language in your response: {language}
    
    Here are some examples of jokes you can use as inspiration:
    {examples}
    
    Your joke:
    """
)


class JokerChainInputs(BaseModel):
    topic: str
    examples: list[str]
    language: str | None = "English"
    max_words: int | None = 50



if __name__ == "__main__":

    joker_config = config={
        "client": {
            "provider": "lmstudio",
            "config": {
                "llm_name": "llama-3.2-3b-instruct",
                "endpoint_url": "http://localhost:11434",
            }
        },
    }

    joker = build_chain(
        config=joker_config,
        input_model=JokerChainInputs,
        output_model=str,
        prompt=PROMPT_TEMPLATE,
    )

    response = joker.run_chain(
        inputs={
            "topic": "animals",
            "language": "Spanish"
        }
    )

    print(response)
