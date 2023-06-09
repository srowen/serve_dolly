# Adapted from https://huggingface.co/docs/transformers/pipeline_webserver

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import asyncio
import torch
import huggingface_hub
from langchain import SQLDatabase
import re
import os

async def homepage(request):
    payload = await request.body()
    string = payload.decode("utf-8")
    response_q = asyncio.Queue()
    await request.app.model_queue.put((string, response_q))
    output = await response_q.get()
    return JSONResponse(output)


async def server_loop(q):
    os.environ['TRANSFORMERS_CACHE'] = "/dbfs/..."
    huggingface_hub.login(token="...")
    model_ckpt = "bigcode/starcoderbase"
    model = AutoModelForCausalLM.from_pretrained(model_ckpt, use_auth_token=True, torch_dtype=torch.bfloat16, device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained(model_ckpt, use_auth_token=True)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=128)

    while True:
        (string, response_q) = await q.get()
        (catalog, schema) = re.search("""`(\w+)\.(\w+)`""", string).groups()
        db = SQLDatabase.from_databricks(catalog, schema, host="...", api_token="dapi...", warehouse_id="...")
        table_info = db.get_table_info()
        prompt = f"<fim_prefix>{table_info}\n-- This is ANSI SQL query that does the following: {string}\n<fim_suffix><fim_middle>"
        out = pipe(prompt)[0]['generated_text'][len(prompt):]
        end = out.find(";")
        if (end > 0):
          out = out[:end]
        await response_q.put(out)

def startup():
    q = asyncio.Queue()
    app.model_queue = q
    asyncio.create_task(server_loop(q))

app = Starlette(
    routes=[
        Route("/", homepage, methods=["GET", "POST"]),
    ],
    on_startup=[startup]
)
