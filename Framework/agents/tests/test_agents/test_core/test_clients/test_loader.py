import pytest

from agents.constants import PROJECT_ROOT
from agents.core.clients.loader import ClientLoader
from agents.core.clients.sdks.lms import LMStudio
from agents.core.clients.sdks.gemini import Gemini


class TestClientLoader:

    def test_load_lms(self):
        client = ClientLoader.load(
            config={
                "provider": "lmstudio",
                "config": {
                    "llm_name": "test_model",
                    "endpoint_url": "http://localhost:11434"
                }
            }
        )
        assert isinstance(client, LMStudio), f"Expected LMStudio client, got {type(client).__name__} instead"
        
    def test_load_gemini_client(self):
        client = ClientLoader.load(
            config={
                "provider": "gemini",
                "config": {
                    # "project_id" -> this is loaded from .env file
                    "llm_name": "gemini-1.5-pro",
                    "endpoint_url": "https://gemini.llm.dev.cosmos.siri.g.apple.com/v1/chat/completions"
                }
            }
        )
        assert isinstance(client, Gemini), f"Expected Gemini client, got {type(client).__name__} instead"
        

    def test_load_client_invalid_provider(self):
        """
        Test loading a client with an invalid provider.
        This should raise a ValueError indicating the provider is not supported.
        """
        with pytest.raises(ValueError):
            ClientLoader.load(
                config={
                    "provider": "invalid_provider",
                    "llm_name": "test_model",
                    "endpoint_url": "http://localhost:11434"
                }
            )


    def test_load_client_from_yaml(self):
        """
        Test loading a client from a YAML configuration file.
        This test assumes that there is a valid YAML file at the specified path.
        """
        loader = ClientLoader()

        # Replace 'path/to/client_config.yaml' with the actual path to your YAML file
        try:
            config_file = PROJECT_ROOT / "tests/data/lmstudio_config.yaml"
            client = loader.load_client_from_yaml(config_file)
            assert client is not None, "Client should be loaded successfully"
        except Exception as e:
            pytest.fail(f"Loading client from YAML failed: {e}")