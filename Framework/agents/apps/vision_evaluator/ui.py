import streamlit as st
from PIL import Image

from agent import VisionEvaluator
from schemas import EvaluationRequest, EvaluationTurn, EvaluationFlow

evaluator = VisionEvaluator()# Streamlit interface

st.title("Vision Evaluator App")
st.write("Upload images and evaluate the conversation turns.")# Input fields

user_query = st.text_input("User Query")
siri_response_screenshot = st.file_uploader("Upload Siri Response Screenshot", type=["png", "jpg", "jpeg"])
expected_behavior = st.text_input("Expected Behavior (optional)")
evaluation_flow = st.selectbox("Evaluation Flow", [e.value for e in EvaluationFlow])

# Process the inputs and run the evaluator
if st.button("Evaluate"):
    if user_query and siri_response_screenshot:
        image = Image.open(siri_response_screenshot)
        turn = EvaluationTurn(
            turn_ix=0,
            user_query=user_query,
            siri_response_screenshot=image,
            expected_behavior=expected_behavior
        )
        request = EvaluationRequest(
            conversation=[turn],
            evaluation_flow=EvaluationFlow(evaluation_flow)
        )
        response = evaluator.run(request)
        st.write("Reasoning:", response.reasoning)
        st.write("Evaluation:", response.evaluation)
    else:
        st.error("Please provide both a user query and a screenshot.")