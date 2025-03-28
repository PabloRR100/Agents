from pydantic import BaseModel

from agents.core.schemas.clients import Client, ClientConfig, ClientRequest, ClientResponse


class ChainInputs(BaseModel)
    """
    A ChainInputs is a request to an LLM chain
    """
    pass


class ChainOutputs(BaseModel):
    """
    A ChainOutputs is a response from an LLM chain
    """
    pass


class Chain(BaseModel):
    """
    A Chain is a wrapper around an LLM client
    """
    client: Client

    def run(self, inputs: ChainInputs) -> ChainOutputs:
        """
        Run the chain with the given inputs and return the outputs
        """
        pass





