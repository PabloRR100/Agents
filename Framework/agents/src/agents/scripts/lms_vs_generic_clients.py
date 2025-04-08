"""
Compare the exact same prompt on the same model using the two different clients.
The model is served locally with LMS.
We will call it using the generic client and the lmstudio client
"""

from agents.core.clients import ClientRequest, Client
from agents.core.clients.generic import GenericClient
from agents.core.clients.lms import LMStudio


def compare_clients(
    prompt: str,
    client_1: Client,
    client_2: Client,
):
    """
    Compare the responses from the two clients.
    """
    # Send the request to both clients
    client_request = ClientRequest.from_user_message(prompt)
    generic_response = client_1.send_request(client_request)
    lmstudio_response = client_2.send_request(client_request)

    # Print the responses
    print("Generic Client Response:", generic_response)
    print("LMStudio Client Response:", lmstudio_response)


generic_client = GenericClient(**{
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
        "endpoint_url": "http://localhost:11434"
    }
})

question = "What is the capital of France?"
compare_clients(
    prompt=question,
    client_1=generic_client,
    client_2=lmstudio_client
)

