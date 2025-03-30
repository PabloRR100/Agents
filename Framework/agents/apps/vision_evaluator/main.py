"""
"""
from agent import VisionEvaluator
from schemas import EvaluationRequest, EvaluationResponse


class VisionEvaluatorApp:
    """
    Vision Evaluator app for evaluating images.
    """

    def __init__(self):
        self.agent = VisionEvaluator()

    def run(self, inputs: dict) -> EvaluationResponse:
        """
        Evaluate an image using the Vision Evaluator agent.
        """
        # Convert the inputs to the appropriate format for the agent
        request = EvaluationRequest(**inputs)
        # Run the agent with the request
        response = self.agent.run(request)
        return response


if __name__ == "__main__":
    # Example usage
    app = VisionEvaluatorApp()
    sample_inputs = {
        "conversation":
            [
                {
                    "user_query": "When is Real Madrid playing next?",
                    "siri_response_screenshot": "./data/sports.jpeg",
                },
                {
                    "user_query": "And Barcelona?",
                    "siri_response_screenshot": "./data/sports.jpeg",
                }
            ]
    }
    sample_response = app.run(sample_inputs)
    print(sample_response)
