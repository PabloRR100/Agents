"""
Vision Evaluator Agent
"""

from agents.core.chains import Chain
from schemas import (
    EvaluationFlow,
    EvaluationRequest,
    EvaluationTurn,
    EvaluationResponse
)


class VisionEvaluator(Chain[EvaluationRequest, EvaluationResponse]):
    """
    Vision Evaluator Agent
    """

    def evaluate_turn(self, turn: EvaluationTurn) -> EvaluationResponse:
        """
        Evaluate a single turn of the conversation
        """
        client_request = self.client._send_request(turn)
        return EvaluationResponse(
            reasoning="This is a mock reasoning for the evaluation",
            evaluation="PASS"
        )

    @staticmethod
    def aggregate_turns(evaluated_turns: list[EvaluationResponse]) -> EvaluationResponse:
        """
        Aggregate the evaluations of all turns
        """
        # Implement the logic to aggregate evaluation
        evaluation = "PASS" if all([turn.evaluation == "PASS" for turn in evaluated_turns]) else "FAIL"
        return EvaluationResponse(
            reasoning="Aggregated reasoning based on all turns' evaluations",
            evaluation=evaluation
        )

    def evaluate_conversation(self, inputs: EvaluationRequest) -> EvaluationResponse:
        """
        Evaluate the entire conversation.
        If evaluation_flow is ACCUMULATIVE, the score will only be asked for the last turn.
        If evaluation_flow is SINGLE PASS, the score will be asked to be provided for all the turns.
        """
        grade_last_interaction = True if inputs.evaluation_flow == EvaluationFlow.ACCUMULATIVE else False
        response = self.run_chain(inputs)
        return response

    def run_chain(self, inputs: EvaluationRequest) -> EvaluationResponse:
        """
        Run the vision evaluator with the given inputs and return the outputs
        """
        # Implement the logic to evaluate the vision inputs
        match inputs.evaluation_flow:
            case EvaluationFlow.SINGLE_PASS | EvaluationFlow.ACCUMULATIVE:
                return self.evaluate_conversation(inputs)
            case EvaluationFlow.PER_TURN:
                evaluated_turns = [
                    self.evaluate_turn(turn) for turn in inputs.conversation
                ]
                return self.aggregate_turns(evaluated_turns)
            case _:
                raise ValueError(f"Unknown evaluation flow: {inputs.evaluation_flow}")


def run_vision_evaluator(
    config: dict,
    inputs: dict,
) -> EvaluationResponse:
    """
    Run the vision evaluator with the given inputs and return the outputs
    """
    evaluator = VisionEvaluator(config)
    response = evaluator.run_chain(inputs)
    return response