from pydantic import BaseModel

from agents.core.clients.adapters import Adapter, register_adapter
from agents.core.clients import ClientResponse, ClientResponseMetadata


class OpenAIMessage(BaseModel):
    role: str
    content: str


class OpenAIChoice(BaseModel):
    index: int
    message: OpenAIMessage
    finish_reason: str | None = None


class OpenAIUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class OpenAIChatResponse(BaseModel):
    id: str
    model: str
    choices: list[OpenAIChoice]


@register_adapter
class OpenAIAdapter(Adapter[OpenAIChatResponse]):
    """
    Adapter for OpenAI API responses.
    """
    provider: str = "openai"
    @staticmethod
    def parse_response(response: OpenAIChatResponse) -> ClientResponse:
        """
        Parse the OpenAI API response and convert it to a ClientResponse.
        """
        choice = response.choices[0]
        return ClientResponse(
            message=choice.message.content,
            metadata=ClientResponseMetadata(
                **{
                    "model": response.model,
                    "usage": {
                        "prompt_tokens": choice.usage.prompt_tokens,
                        "completion_tokens": choice.usage.completion_tokens,
                        "total_tokens": choice.usage.total_tokens,
                    },
                }
            )
        )
