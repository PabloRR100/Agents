from PIL import Image
from pydantic import BaseModel, field_validator
from


class Turn(BaseModel):
    user_query: str
    siri_response_screenshot: Image.Image
    expected_behavior: str | None = None

    @field_validator("siri_response_screenshot", mode="before")
    def load_image(cls, image_path: str):
        return Image.open(image_path)


class Conversation(BaseModel):
    """
    A Conversation is a series of turns in a conversation
    """
    turns: list[Turn]


class EvaluationRequest(BaseModel):
    """
    """
    pass

