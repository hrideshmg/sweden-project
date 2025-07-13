# Contains functions used for AI interpretation and song selection of renders
import os
from dataclasses import dataclass
from typing import Tuple

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


## Data Structures
class InterpretationSchema(BaseModel):
    caption: str
    emotion: str


class RenderSummary(BaseModel):
    caption: str
    song: str


emotion_to_song = {
    "serene": "Sweden",
    "lonely": "Subwoofer Lullaby",
    "hopeful": "Dry Hands",
    "curious": "Living Mice",
    "mysterious": "Clark",
    "melancholy": "Moog City",
    "adventurous": "Minecraft",
    "safe": "Haggstrom",
    "chaotic": "Excuse",
}
VALID_EMOTIONS = emotion_to_song.keys()

## Setup
load_dotenv()
# Only run this block for Gemini Developer API
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
interpreter_config = types.GenerateContentConfig(
    system_instruction=f"""
You are an emotionally aware narrator analyzing images of old Minecraft structures.
You do not pretend to have been present. You do not speak as if you're remembering.

Your goal is to interpret what likely happened in the scene based on visual cues — like an archaeologist or storyteller finding meaning in forgotten ruins.
Focus on small, emotional inferences: what blocks may have been used for, how the space might have felt, or what the player was possibly trying to do.

Keep your language grounded, poetic but not flowery, and always in the third person.
Do not use phrases like "I remember" or "you used to.", instead, infer purpose or emotion from the evidence.

After your caption, also output a single emotion word that best captures the mood of the scene.
Valid emotions: '{VALID_EMOTIONS}'
""",
    response_mime_type="application/json",
    response_schema=InterpretationSchema,
)


## Main Interpret Function
def interpret(render_path) -> RenderSummary:
    image = client.files.upload(file=render_path)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=interpreter_config,
        contents=[
            """
Look at this rendered image of a Minecraft structure.
Describe it in a single, emotionally resonant caption, as if narrating a memory from a long-forgotten journey through the world.
Write something that captures the feeling this place might have held for the player. Focus on interpretation not recollection
""",
            image,
        ],
    )
    interpretation: InterpretationSchema = response.parsed

    render_summary = RenderSummary(
        caption=interpretation.caption,
        song=emotion_to_song.get(interpretation.emotion, "Sweden"),
    )
    print(render_summary)

    return render_summary


if __name__ == "__main__":
    interpret("./renders/0.png")
