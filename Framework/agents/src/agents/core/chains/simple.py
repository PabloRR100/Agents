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

    def
