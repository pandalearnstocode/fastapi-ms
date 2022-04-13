import json

import requests
from celery.result import AsyncResult
from fastapi import Body, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from pydantic import BaseModel
import pandas as pd
import pickle
from worker import create_task

description = """
ML Engine API to trigger ML endpoints (lightweight process) and ML jobs/tasks (batch processing). 🚀

## Endpoint description in ML Engine API

In this REST API service we have the following items,

* Show a minimalistic UI to trigger a sample ML job.
* A endpoint to trigger a ML job.
* A endpoint to get the status of a ML job.
* A endpoint to run lightweight ML workload and return the result.

## ML endpoints (lightweight process): prediction

You will be able to:

* **prediction** (POST: This is a endpoint to demo real time inference like prediction.).


## ML jobs/tasks (batch processing): model training

You will be able to:

* **/tasks** (POST: This is to submit a long running celery task.).
* **/tasks/{task_id}** (GET: For a submitted task_id this endpoint is to check the status and result of the task.).
"""

tags_metadata = [
    {
        "name": "prediction",
        "description": "Light weight ML endpoint to take input and predict the output using a pre-trained model.",
        "externalDocs": {
            "description": "Creating a Machine Learning Inference API with FastAPI",
            "url": "https://rb.gy/vhdb32",
        },
    },
    {
        "name": "jobs",
        "description": "Collection of ML endpoints to trigger a batch processing job, status tracking and fetching results.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "utils",
        "description": "Any other endpoint to help the jobs and prediction endpoints."
    },
]

pkl_filename = "./iris_model.pkl"
with open(pkl_filename, 'rb') as file:
	lr_model = pickle.load(file)
with open('./model_train_payload.json', 'r') as fp:
    model_payload = json.load(fp)
app = FastAPI(
    title="Analytical App ML Engine",
    description=description,
    version="0.0.1",
    contact={
        "name": "Analytical App ML Engine Dev Owner",
        "url": "http://subapp.app.com/contact/",
        "email": "app-dl@app.com",
    },
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json"
)

class Iris(BaseModel):
	sepal_length: float
	sepal_width: float
	petal_length: float
	petal_width: float

	class Config:
		schema_extra = {"example":{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}}

class PredictResponse(BaseModel):
	predicted_target: float

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", tags=["utils"])
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})

@app.post("/prediction/", tags=["prediction"], response_model=PredictResponse)
async def predict(iris: Iris):
	input_df = pd.DataFrame([iris.dict()])
	pred = lr_model.predict(input_df)[0]
	return {"predicted_target":pred}

@app.post("/tasks", status_code=201, tags=["jobs"])
def run_task(payload=Body(...)):
    task_type = payload["type"]
    logger.info(f"Task type: {str(task_type)} received.")
    url = "http://crud:8000/task"
    logger.info(f"Task type: {str(task_type)} received.")
    task = create_task.delay(int(task_type), model_payload)
    logger.info(f"Task type: {task_type} submitted. Generated task id: {task.id}")
    payload = {
        "task_id": str(task.id),
        "task_type": str(task_type),
        "task_status": "SUBMITTED",
        "task_result": {"result": None},
    }
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        logger.info(f"Task for {str(task.id)} registered in DB successfully.")
    else:
        logger.warning(f"Task for {str(task.id)} not registered in DB.")
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}", tags=["jobs"])
def get_status(task_id):
    url = f"http://crud:8000/id/{task_id}"
    logger.info(f"Checking status for task id: {task_id}.")
    r = requests.get(url)
    res = r.json()
    res_id = res["id"]
    task_type = res["task_type"]
    task_result = AsyncResult(task_id)
    logger.info(f"Task id: {task_id} status requested.")
    logger.info(f"Task id: {task_id} status: {task_result.status}")
    url = f"http://crud:8000/task/{res_id}"

    result = {
        "task_id": str(task_result.task_id),
        "task_status": str(task_result.status),
        "task_result": {"result": None},
        "task_type": str(task_type),
    }
    if task_result.status == "SUCCESS":
        logger.info(f"{type(task_result.result)}")
        result["task_result"] = {"result": task_result.result}

    r = requests.put(url, json=result)
    result["task_result"] = {"result": task_result.result}
    if r.status_code == 200:
        logger.info(f"Task for {str(task_id)} registered in DB successfully.")
    else:
        logger.warning(f"Task for {str(task_id)} not registered in DB.")
    return JSONResponse(result)
