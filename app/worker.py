import os
import time
import pandas as pd
from celery import Celery
import pandas as pd
import json
from sklearn.linear_model import LogisticRegression

# from cpu_load_generator import load_all_cores
from loguru import logger

def logistic_regression_to_json(lrmodel, file=None):
    if file is not None:
        serialize = lambda x: json.dump(x, file)
    else:
        serialize = json.dumps
    data = {}
    data['init_params'] = lrmodel.get_params()
    data['model_params'] = mp = {}
    for p in ('coef_', 'intercept_','classes_', 'n_iter_'):
        mp[p] = getattr(lrmodel, p).tolist()
    return serialize(data)

def _short_task(payload):
    df = pd.DataFrame(payload['data'])
    X = df[payload['independent_variables']]
    y = df[payload['target_variable']]
    lr_model = LogisticRegression()
    lr_model.fit(X, y)
    model_response = logistic_regression_to_json(lr_model)
    response_dict = json.loads(model_response)
    logger.info("Short task")
    time.sleep(10)
    return {"task_duration": "Short task", "model_result": response_dict}


def _medium_task(payload):
    df = pd.DataFrame(payload['data'])
    X = df[payload['independent_variables']]
    y = df[payload['target_variable']]
    lr_model = LogisticRegression()
    lr_model.fit(X, y)
    model_response = logistic_regression_to_json(lr_model)
    response_dict = json.loads(model_response)
    logger.info("Medium task")
    time.sleep(20)
    return {"task_duration": "Medium task", "model_result": response_dict}


def _long_task(payload):
    df = pd.DataFrame(payload['data'])
    X = df[payload['independent_variables']]
    y = df[payload['target_variable']]
    lr_model = LogisticRegression()
    lr_model.fit(X, y)
    model_response = logistic_regression_to_json(lr_model)
    response_dict = json.loads(model_response)
    logger.info("Long task")
    time.sleep(30)
    return {"task_duration": "Long task", "model_result": response_dict}


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@celery.task(name="create_task")
def create_task(task_type, payload):
    if int(task_type) == 1:
        out = _short_task(payload)
    elif int(task_type) == 2:
        out = _medium_task(payload)
    elif int(task_type) == 3:
        out = _long_task(payload)
    return out
