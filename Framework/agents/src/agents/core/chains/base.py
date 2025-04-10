from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic

from pydantic import BaseModel, ConfigDict,  model_validator

from agents.core.clients import BaseClient, ClientRequest, ClientResponse
from agents.core.clients.loader import ClientLoader


# Define type variables for input and output types.
InputType = TypeVar('InputType', bound=BaseModel)
OutputType = TypeVar('OutputType', bound=BaseModel | str)


class Chain(ABC, BaseModel, Generic[InputType, OutputType]):
    """
    A Chain is a sequence of operations on top of an LLM client.
    They are responsible for receiving an input, process it, and produce an output.
    """
    client: BaseClient
    model_config = ConfigDict(arbitrary_types_allowed = True)

    @abstractmethod
    def run_chain(self, inputs: dict) -> OutputType:
        """
        Run the chain with the given inputs.
        """
        pass


def build_chain(
    config: dict,
    input_model: Type[InputType],
    output_model: Type[OutputType],
    prompt: PromptTemplate,
) -> Chain[InputType, OutputType]:
    new_chain = Chain[InputType, OutputType](
        prompt=prompt,
        input_model=input_model,
        output_model=output_model,
        **config
    )
    return new_chain
