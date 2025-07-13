import glob
import os

from mcrender import render

from scanner import scan_chunks

RENDER_SIZE = (100, 160, 100)
DEPTH = 40


world_path = "./demo_map2/"


def prep_render_folder():
    os.makedirs("./renders/", exist_ok=True)
    files = glob.glob("./renders/*")
    for f in files:
        os.remove(f)


def main_loop():
    prep_render_folder()
    chunks = scan_chunks(world_path)

    # Start rendering
    for index, chunk in enumerate(chunks):
        print(f"Rendering Chunk: {index+1}/{len(chunks)}")
        render(
            f"./renders/{index}.png",
            world_path,
            chunk.x,
            DEPTH,
            chunk.z,
            RENDER_SIZE[0],
            RENDER_SIZE[1],
            RENDER_SIZE[2],
        )


if __name__ == "__main__":
    main_loop()
