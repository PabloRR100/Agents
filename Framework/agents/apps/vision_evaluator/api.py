import fastapi

from fastapi.responses import JSONResponse

from constants import PROJECT_ROOT
from main import VisionEvaluatorApp

app = fastapi.FastAPI()
CONFIG = PROJECT_ROOT / "configs/lmstudio.yaml"


@app.post("/evaluate")
async def evaluate(inputs: dict):
    evaluator_app = VisionEvaluatorApp()
    response = evaluator_app.run(inputs)
    return JSONResponse(content=response.model_dump())


if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
