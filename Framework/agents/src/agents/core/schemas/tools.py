import json
import logging

from pydantic import BaseModel


LOG = logging.getLogger(__name__)


class ToolParameter(BaseModel):
    """
    A ToolParameter is a parameter for a tool.
    """
    type: str
    description: str
    required: bool = False
    default: str | None = None
    enum: list[str] | None = None


class Tool(BaseModel):
    """
    A Tool is a tool that can be used by an agent.
    """
    name: str
    description: str
    parameters: dict[str, ToolParameter] | None = None


class Toolbox(BaseModel):
    """
    A Toolbox is a collection of tools that can be used by an agent.

    This can be used with different flavours.
    - The agent can get access to the full list of tools at once.
    - If the Toolbox is too big, the agent can get access to a subset of tools.
        For this we can use a ToolRetriever system to retrieve the relevant tools for a given task.
    """
    tools: list[Tool]

    @classmethod
    def load_from_json_file(cls, json_path: str) -> "Toolbox":
        """
        Load a Toolbox from a JSON string.
        """
        LOG.info(f"Loading Toolbox from {json_path}")
        with open(json_path, "r") as f:
            tools = json.load(f)
            LOG.info(f"Loaded Toolbox with {len(tools)} tools")
            return cls(**tools)

    def get_tool(self, name: str) -> Tool | None:
        """
        Get a tool by name.
        """
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None

    def dump(self, json_path: str):
        """
        Dump the Toolbox to a JSON file.
        """
        with open(json_path, "w") as f:
            json.dump(self.model_dump(), f, indent=4)
        LOG.info(f"Toolbox dumped to {json_path}")
