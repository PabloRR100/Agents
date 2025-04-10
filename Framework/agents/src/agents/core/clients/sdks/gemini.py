import logging
import os
from typing import Literal

import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel, GenerationResponse
from dotenv import load_dotenv
from pydantic import model_validator

from agents.core.clients import ClientResponse
from agents.core.clients.base import BaseClient, ClientConfig


load_dotenv()
LOG = logging.getLogger(__name__)


class GeminiClientConfig(ClientConfig):
    """
    Configuration for the Gemini client.
    """
    # Add any specific configuration fields for the Gemini client here
    project_id: str
    llm_name: str = "gemini-1.5-pro"
    system_prompt: str | None = None

    @model_validator(mode="before")
    def init_vertex(cls, values: dict):
        project_id = os.getenv("GOOGLE_PROJECT_ID") or values.get("project_id")
        if not project_id:
            raise ValueError("Google project ID must be set either in the environment or in the configuration.")
        values["project_id"] = project_id
        LOG.info("Initializing Vertex AI with project ID: %s", project_id)
        vertexai.init(project=project_id, location="us-central1")
        return values


class Gemini(BaseClient):
    """
    Gemini client for interacting with the Gemini API.
    """
    provider: Literal["gemini"]
    config: GeminiClientConfig
    model: GenerativeModel | None = None

    @model_validator(mode="before")
    def initialize_client(cls, values: dict) -> dict:
        """
        Initialize the Ollama client with the provided configuration.
        """
        return values

    def solve_request(self, request):
        """
        Send a request to the Gemini API and return the response.
        """
        prompt, generation_config = self._parse_request(request)
        model = GenerativeModel(
            model_name=self.config.llm_name,
            system_instruction=self.config.system_prompt,
            generation_config=generation_config
        )
        response = model.generate_content(prompt)
        response = self._parse_response(response)
        return response

