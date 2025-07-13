
# The Sweden Project

This project is a creative tool that transforms your old Minecraft worlds into a personalized, nostalgic experience. It identifies areas where you've spent the most time, captures images of your creations, and presents them in a beautiful web interface, complete with AI-generated captions and music by C418. It's like a digital scrapbook of your Minecraft adventures.

## Why Did I Make This?
Like a lot of kids, I grew up playing Minecraft and its a game that I hold quite dear to my heart. To me, it was more than just a game; it was a world where I made some of my best memories, building, exploring, and laughing with friends. I built this project as a sort of tribute to the game and to help others revisit the adventures they once had in those pixelated landscapes.

This project was built solo during the [OSDHack](https://hack.osdc.dev/) Hackathon where the theme was to build something to reimagine something from your past. I built this solo because lately I've been feeling pretty out of touch with my creative and technical side and It is by all means a labour of love, hope you like it :)

## How It Works

The process is broken down into three main steps:

1.  **Scanning:** The `scanner.py` script analyzes your Minecraft world save and identifies "chunks" where you've spent a significant amount of time. This is based on the `InhabitedTime` data stored in the NBT data of the world files. It filters out chunks that are too close to each other to avoid redundancy.

2.  **Rendering:** For each identified chunk, the `mcrender` library is used to generate a high-quality 3D render of the area. This creates a visual snapshot of your creations.

3.  **Interpretation:** The rendered image is then passed to an AI model (`interpreter.py`) that generates a poetic and emotionally resonant caption for the scene. It also selects a fitting C418 song based on the "vibe" of the image.

4.  **Web Interface:** The final output is a beautiful, interactive web page (`index.html`) that displays the rendered images, captions, and associated music. You can click on each entry to see a larger view and get lost in the memories.

## How to Use

1.  **Installation:**
    *   Clone this repository.
    *   Install the required Python libraries:
        ```bash
        pip install -r requirements.txt
        ```
    *   Set up your Gemini API key by creating a `.env` file with the following content:
        ```
        GEMINI_API_KEY=your_api_key
        ```

2.  **Execution:**
    *   Run the main script with the path to your Minecraft world:
        ```bash
        python main.py
        ```
    *   The script will then process your world and generate the necessary files.

3.  **Viewing the Results:**
    *   Once the script has finished, open the `index.html` file in your web browser to view your personalized Minecraft scrapbook.

## Project Structure

*   `main.py`: The main script that orchestrates the entire process.
*   `scanner.py`: Scans the Minecraft world for inhabited chunks.
*   `interpreter.py`: Uses an AI model to generate captions and select music.
*   `requirements.txt`: A list of the Python libraries required for this project.
*   `index.html`: The web interface for displaying the final results.
*   `demo_map/`: A sample Minecraft world for testing purposes.
*   `renders/`: The directory where the rendered images are saved.

## Customization

You can customize the behavior of the project by modifying the following:

*   **`INHABITED_THRESHOLD` in `scanner.py`:** This value determines the minimum time (in ticks) a player must have spent in a chunk for it to be considered "inhabited."
*   **`MIN_DIST` in `scanner.py`:** This value sets the minimum distance (in chunks) between two selected chunks.
*   **`emotion_to_song` in `interpreter.py`:** This dictionary maps emotions to C418 songs. You can add or modify these mappings to your liking.
*   **The prompt in `interpreter.py`:** You can change the prompt to guide the AI in generating different styles of captions.

## Future Ideas

*   **User-Uploaded Worlds:** A web interface could be created to allow users to upload their own worlds directly.
*   **More Music Options:** The music selection could be expanded to include other artists or even allow users to choose their own.
