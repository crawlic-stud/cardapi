import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Response

import main


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/test")
async def test_image(colors: str):
    colors = map(lambda color: "#" + color, colors.split(","))
    return Response(content=main.get_test_image(
        *colors
    ), media_type="image/png")
