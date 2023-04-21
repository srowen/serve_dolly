# Adapted from https://huggingface.co/docs/transformers/pipeline_webserver

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from transformers import pipeline
import asyncio
import torch


async def homepage(request):
    payload = await request.body()
    string = payload.decode("utf-8")
    response_q = asyncio.Queue()
    await request.app.model_queue.put((string, response_q))
    output = await response_q.get()
    return JSONResponse(output)


async def server_loop(q):
    # See https://github.com/databrickslabs/dolly#generating-on-other-instances for notes on how to use the 12b model
    pipe = pipeline(model="databricks/dolly-v2-7b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")
    while True:
        (string, response_q) = await q.get()
        out = pipe(string)
        await response_q.put(out)

def startup():
    q = asyncio.Queue()
    app.model_queue = q
    asyncio.create_task(server_loop(q))

app = Starlette(
    routes=[
        Route("/", homepage, methods=["POST"]),
    ],
    on_startup=[startup]
)
