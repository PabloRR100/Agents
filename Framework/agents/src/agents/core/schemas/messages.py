from enum import Enum
from typing import Literal

from pydantic import BaseModel
from PIL.Image import Image as PILImage
from agents.core.schemas.tools import Tool


class Role(str, Enum):
    USER = "user"
    SYSTEM = "system"
    EXECUTOR = "executor"
    ASSISTANT = "assistant"
    TOOL_CALL = "tool_call"
    TOOL_RESPONSE = "tool_response"


class Action(str, Enum):
    SAY = "say"
    ACT = "act"


class Message(BaseModel):
    role: Role
    content: str


class Image(BaseModel, PILImage):
    """
    Wrapper around PIL.Image
    """
    pass


# User Interface


class UserMessage(Message):
    avatar = "👤"
    role: Role = "user"
    text: str | None = None
    images: list[Image] | None = None
    action: Action | None = None


# Assistant Interface

class SystemMessage(Message):
    role: Literal["system"] = "system"


class ToolCall(Message):
    """
    A ToolCall is a message that represents a call to a tool
    """
    avatar = "🛠️"
    role: Literal["tool_call"] = "assistant"
    tool: Tool | None = None
    parameters: dict | None = None


class AssistantMessage(Message):
    """
    An AssistantMessage is a message from the assistant
    """
    avatar = "🤖"
    role: Literal["assistant"] = "assistant"
    text: str | None = None
    images: list[Image] | None = None
    tool_call: ToolCall | None = None


# Executor / Environment Interface

class ToolCallResponse(Message):
    """
    A ToolCallResponse is a message that represents a response from a tool
    """
    avatar = "⚙"
    tool: Tool | None = None
    parameters: dict | None = None


class ExecutorMessage(Message):
    role: Literal["executor"] = "executor"

