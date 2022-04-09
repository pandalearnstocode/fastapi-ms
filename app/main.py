import json

import requests
from celery.result import AsyncResult
from fastapi import Body, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from worker import create_task

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    task_type = payload["type"]
    logger.info(f"Task type: {str(task_type)} received.")
    url = "http://crud:8000/task"
    logger.info(f"Task type: {str(task_type)} received.")
    task = create_task.delay(int(task_type))
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


@app.get("/tasks/{task_id}")
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
        result["task_result"] = {"result": task_result.result}

    r = requests.put(url, json=result)
    result["task_result"] = json.dumps({"result": task_result.result})
    if r.status_code == 200:
        logger.info(f"Task for {str(task_id)} registered in DB successfully.")
    else:
        logger.warning(f"Task for {str(task_id)} not registered in DB.")
    return JSONResponse(result)
