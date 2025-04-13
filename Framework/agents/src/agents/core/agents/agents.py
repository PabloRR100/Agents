from abc import ABC, abstractmethod

from agents.core.clients import BaseClient


class BaseAgent(ABC):
    """
    An agent is a type of chain that has agency.
    It works following the ReAct framework, which is a combination of reasoning and acting.
    """

    def __init__(
        self,
        client: BaseClient,
        *args,
        **kwargs
    ):
        self.client = client

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Run the agent for the given task.
        """
        ...


class SingleStepAgent(ABC, BaseAgent):
    """
    A single step agent is a type of agent that can only take one action to give the final response.
    """
    pass


class MultiStepAgent(ABC, BaseAgent):
    """
    A multi step agent is a type of agent that can take multiple actions to give the final response.
    """
    pass