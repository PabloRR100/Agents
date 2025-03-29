import base64
import requests
from enum import Enum
from io import BytesIO
from PIL import Image
from pydantic import ConfigDict, field_validator, Field, model_validator

from agents.schemas import Serializable


def encode_image(image: Image.Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


class EvaluationFlow(str, Enum):
    """
    Evaluation Flow Enum
    """
    PER_TURN = "per_turn"  # each conversation turn is evaluated separately and then aggregated
    SINGLE_PASS = "single_pass"  # all the conversation turns are evaluated in a single pass
    ACCUMULATIVE = "accumulative"  # all the conversation turns are evaluated in an accumulative manner



class EvaluationTurn(Serializable):
    turn_ix: int  # now required
    user_query: str
    siri_response_screenshot: Image.Image = Field(exclude=True)
    expected_behavior: str | None = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={Image.Image: encode_image}
    )

    @field_validator("siri_response_screenshot", mode="before")
    def load_image(cls, value):
        if isinstance(value, Image.Image):
            return value
        if isinstance(value, str):
            if value.startswith("http"):
                response = requests.get(value)
                return Image.open(BytesIO(response.content))
            return Image.open(value)
        raise ValueError("siri_response_screenshot must be a valid path or URL.")


class EvaluationRequest(Serializable):
    conversation: list[EvaluationTurn]
    evaluation_flow: EvaluationFlow = Field(default=EvaluationFlow.PER_TURN, description="The evaluation flow to be used")

    @model_validator(mode="before")
    def assign_turn_indices(cls, values):
        conversation = values.get("conversation", [])
        for idx, turn in enumerate(conversation):
            if isinstance(turn, dict) and turn.get("turn_ix") is None:
                turn["turn_ix"] = idx
        return values


class EvaluationResponse(Serializable):
    reasoning: str = Field(description="The reasoning behind the evaluation")
    evaluation: str = Field(description="The evaluation of the Siri response. PASS or FAIL")


if __name__ == "__main__":

    inputs = {
        "conversation":
            [
                {
                    "user_query": "When is Real Madrid playing next?",
                    "siri_response_screenshot": "./data/sports.jpeg",
                },
                {
                    "user_query": "And Barcelona?",
                    "siri_response_screenshot": "./data/sports.jpeg",
                }
            ]
    }

    inputs = EvaluationRequest(**inputs)
    print(inputs)
