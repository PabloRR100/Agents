"""
Compare the exact same prompt on the same model using the two different clients.
The model is served locally with LMS.
We will call it using the generic client and the lmstudio client
"""

from agents.core.clients import ClientRequest
from agents.core.clients.generic import GenericClient
from agents.core.clients.lms import LMStudio


def compare_clients(
    prompt: str,
    generic_client: GenericClient,
    lmstudio_client: LMStudio,
):
    """
    Compare the responses from the two clients.
    """
    # Send the request to both clients
    client_request = ClientRequest.from_user_message(prompt)
    generic_response = generic_client.send_request(client_request)
    lmstudio_response = lmstudio_client.send_request(client_request)

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
    generic_client=generic_client,
    lmstudio_client=lmstudio_client
)

