from fastapi import FastAPI

from payload_generator import (
    _bar_payload_generator,
    _donut_payload_generator,
    _line_payload_generator,
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
