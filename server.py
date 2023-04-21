# Adapted from https://huggingface.co/docs/transformers/pipeline_webserver

from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route
import torch
import asyncio
from io import BytesIO
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler


async def homepage(request):
    payload = await request.body()
    string = payload.decode("utf-8")
    response_q = asyncio.Queue()
    await request.app.model_queue.put((string, response_q))
    output = await response_q.get()
    return Response(output, media_type="image/jpeg")


async def server_loop(q):
    pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.bfloat16)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")

    while True:
        (string, response_q) = await q.get()
        out = pipe(string).images[0]
        img_jpg = BytesIO()
        out.save(img_jpg, format='JPEG')
        await response_q.put(img_jpg.getvalue())

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
