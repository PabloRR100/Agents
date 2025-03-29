from typing import TypeVar, Generic, Any

from pydantic import BaseModel

from agents.schemas.clients import Client


# Define type variables for input and output types.
InputType = TypeVar('InputType', bound=BaseModel)
OutputType = TypeVar('OutputType', bound=BaseModel)


class Chain(Generic[InputType, OutputType]):

    client: Client

    def run(self, inputs: InputType) -> OutputType:
        raise NotImplementedError("Subclasses must implement the run method")
