from fastapi import FastAPI

from payload_generator import (
    _bar_payload_generator,
    _donut_payload_generator,
    _hist_payload_generate,
    _line_payload_generator,
    _scatter_payload_generator,
    _waterfall_payload_generator,
)

app = FastAPI()


@app.get("/donut")
async def donut():
    return _donut_payload_generator()


@app.get("/bar")
async def bar():
    return _bar_payload_generator()


@app.get("/line")
async def line():
    return _line_payload_generator()


@app.get("/histogram")
async def hist():
    return _hist_payload_generate()


@app.get("/scatter")
async def scatter():
    return _scatter_payload_generator()


@app.get("/waterfall")
async def waterfill():
    return _waterfall_payload_generator()
