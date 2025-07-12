from dataclasses import dataclass
from typing import List

import amulet

# Set threshold in ticks (20 ticks = 1 second)
# 1 hour = 3600 seconds × 20 = 72000 ticks
INHABITED_THRESHOLD = 50000

# Minimum distance between chunks
MIN_DIST = 32


@dataclass
class ChunkData:
    x: int
    z: int
    score: int


def is_far_enough(c1, c2) -> bool:
    return abs(c1.x - c2.x) >= MIN_DIST or abs(c1.z - c2.z) >= MIN_DIST


# Filter close chunks
def filter_close_chunks(chunks) -> List[ChunkData]:
    filtered = []
    for candidate in chunks:
        if all(is_far_enough(candidate, existing) for existing in filtered):
            filtered.append(candidate)
    return filtered


# Returns a sorted list of active chunks
def scanner(world_path) -> List[ChunkData]:
    level = amulet.load_level(world_path)
    active_chunks = []

    for dimension in level.dimensions:
        for chunk, _, _ in level.get_chunk_slice_box(dimension):
            # Chunk is not generated, skip
            if chunk.status == -1:
                continue

            if chunk.misc["inhabited_time"] > INHABITED_THRESHOLD:
                active_chunks.append(
                    ChunkData(chunk.cx, chunk.cz, chunk.misc["inhabited_time"])
                )

            # temp
            if len(active_chunks) > 2:
                break

    filtered_chunks = filter_close_chunks(active_chunks)

    return sorted(filtered_chunks, key=lambda x: x.score)


if __name__ == "__main__":
    print(scanner("./demo_map/"))
