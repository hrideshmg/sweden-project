import glob
import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcrender import render
from pydantic import BaseModel

from interpreter import interpret
from scanner import scan_chunks

RENDER_SIZE = (100, 160, 100)
DEPTH = 40

app = FastAPI()
origins = [
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WorldPath(BaseModel):
    world_path: str


def prep_render_folder():
    os.makedirs("./renders/", exist_ok=True)
    files = glob.glob("./renders/*")
    for f in files:
        os.remove(f)


@app.post("/start_render")
def start_process(path: WorldPath):
    prep_render_folder()
    chunks = scan_chunks(path.world_path)
    result = []

    # Start rendering
    for index, chunk in enumerate(chunks):
        print(f"Rendering Chunk: {index+1}/{len(chunks)}")
        render(
            f"./renders/{index}.png",
            path.world_path,
            chunk.x,
            DEPTH,
            chunk.z,
            RENDER_SIZE[0],
            RENDER_SIZE[1],
            RENDER_SIZE[2],
        )

        summary = interpret(f"./renders/{index}.png")
        result.append(
            {
                "id": index,
                "image": f"./renders/{index}.png",
                "title": f"Chunk {index+1}",
                "description": summary.caption,
                "song": summary.song,
            }
        )
    return result


if __name__ == "__main__":
    path = WorldPath(world_path="./demo_map/")
    start_process(path)
