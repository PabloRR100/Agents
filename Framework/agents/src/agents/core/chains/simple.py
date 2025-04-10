import logging
from typing import Type, TypeVar, Generic

import yaml
from pydantic import BaseModel, ConfigDict,  model_validator

from agents.core.chains import Chain


LOG = logging.getLogger(__name__)

# Define type variables for input and output types.
InputType = TypeVar('InputType', bound=BaseModel)
OutputType = TypeVar('OutputType')



class SimpleChain(Chain):
    """
    A SimpleChain is a basic implementation of a Chain that sends a request to an LLM and returns the response.
    It doesn't support Chat or complex workflows, just a simple request-response cycle.
    """

    model_config = ConfigDict(arbitrary_types_allowed = True)

    @model_validator(mode="before")
    def init_client(cls, values):
        """
        Validate the client configuration.
        """
        LOG.info("Initializing client for the chain.")
        client = ClientLoader.load(values.get("client", None))
        values["client"] = client
        return values

    def from_yaml(self):
        raise NotImplementedError

    def _validate_inputs(self, inputs: dict) -> dict:
        try:
            inputs = self.input_model(**inputs)
            return inputs.model_dump()
        except Exception as e:
            raise ValueError("Invalid Inputs") from e

    @staticmethod
    def _parse_inputs(input_prompt: Prompt) -> ClientRequest:
        return ClientRequest.from_user_message(input_prompt)

    def _parse_output(self, client_response: ClientResponse) -> OutputType:
        response = client_response.message.content
        if isinstance(response, dict) and issubclass(self.output_model, BaseModel):
            output_instance = self.output_model(**response)
        else:
            # For non-dict outputs (e.g. str), assume direct construction.
            output_instance = self.output_model(response)
        return output_instance

    def run_chain(self, inputs: dict) -> OutputType:
        inputs = self._validate_inputs(inputs)
        prompt = self.prompt.format(**inputs)
        client_request = self._parse_inputs(prompt)
        client_response = self.client._send_request(client_request)
        response = self._parse_output(client_response)
        return response
