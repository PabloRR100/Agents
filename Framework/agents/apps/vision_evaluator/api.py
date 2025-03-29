import fastapi

from fastapi.responses import JSONResponse

from apps.vision_evaluator.main import VisionEvaluatorApp

app = fastapi.FastAPI()

@app.post("/evaluate")
async def evaluate(inputs: dict):
    evaluator_app = VisionEvaluatorApp()
    response = evaluator_app.run(inputs)
    return JSONResponse(content=response.model_dump())


if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
