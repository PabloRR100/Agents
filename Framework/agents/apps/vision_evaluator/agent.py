"""
Vision Evaluator Agent
"""

from agents.schemas.chains import Chain
from apps.vision_evaluator.schemas import (
    EvaluationFlow,
    EvaluationRequest,
    EvaluationTurn,
    EvaluationResponse
)


class VisionEvaluator(Chain[EvaluationRequest, EvaluationResponse]):
    """
    Vision Evaluator Agent
    """

    @staticmethod
    def evaluate_turn(turn: EvaluationTurn) -> EvaluationResponse:
        """
        Evaluate a single turn of the conversation
        """
        # Implement the logic to evaluate a single turn
        return EvaluationResponse(
            reasoning="This is a mock reasoning for the evaluation",
            evaluation="PASS"
        )

    @staticmethod
    def aggregate_turns(evaluated_turns: list[EvaluationResponse]) -> EvaluationResponse:
        """
        Aggregate the evaluations of all turns
        """
        # Implement the logic to aggregate evaluations
        return EvaluationResponse(
            reasoning="Aggregated reasoning goes here",
            evaluation="Aggregated score goes here"
        )

    @classmethod
    def evaluate_conversation(cls, inputs: EvaluationRequest) -> EvaluationResponse:
        """
        Evaluate the entire conversation.
        If evaluation_flow is ACCUMULATIVE, the score will only be asked for the last turn.
        If evaluation_flow is SINGLE PASS, the score will be asked to be provided for all the turns.
        """
        grade_last_interaction = True if inputs.evaluation_flow == EvaluationFlow.ACCUMULATIVE else False
        return EvaluationResponse(
            reasoning="This is a mock reasoning for the conversation evaluation",
            evaluation="PASS",
        )


    def run(self, inputs: EvaluationRequest) -> EvaluationResponse:
        """
        Run the vision evaluator with the given inputs and return the outputs
        """
        # Implement the logic to evaluate the vision inputs
        return EvaluationResponse(
            reasoning="Evaluation reasoning goes here",
            evaluation="Evaluation score goes here"
        )
