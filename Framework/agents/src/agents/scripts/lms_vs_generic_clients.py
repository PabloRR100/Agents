"""
Compare the exact same prompt on the same model using the two different clients.
The model is served locally with LMS.
We will call it using the generic client and the lmstudio client
"""

from agents.core.clients import ClientRequest, BaseClient
from agents.core.clients.internal import Client
from agents.core.clients.sdks.lms import LMStudio


def compare_clients(
    prompt: str,
    client_1: BaseClient,
    client_2: BaseClient,
):
    """
    Compare the responses from the two clients.
    """
    # Send the request to both clients
    client_request = ClientRequest.from_user_message(prompt)
    generic_response = client_1._send_request(client_request)
    lmstudio_response = client_2._send_request(client_request)

    # Print the responses
    print("Generic Client Response:", generic_response)
    print("LMStudio Client Response:", lmstudio_response)


generic_client = Client(**{
    "provider": "generic",
    "config": {
        "llm_name": "llama-3.2-3b-instruct",
        "endpoint_url": "http://localhost:11434"
    }
})

lmstudio_client = LMStudio(**{
    "provider": "lmstudio",
    "config": {
        "llm_name": "llama-3.2-3b-instruct",
        "endpoint_url": "http://localhost:11434",
        "framework": "lms"
    }
})

question = "What is the capital of France?"
compare_clients(
    prompt=question,
    client_1=generic_client,
    client_2=lmstudio_client
)

