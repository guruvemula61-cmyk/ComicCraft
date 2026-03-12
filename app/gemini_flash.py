import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Latest fast Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_outline(user_prompt: str):

    prompt = f"""
You are a professional comic storyboard planner.

Create a structured 5 panel comic outline.

Story Idea:
{user_prompt}

Return ONLY a valid JSON array.

Format:

[
  {{
    "panel": 1,
    "title": "Panel title",
    "scene_description": "Short scene description",
    "image_prompt": "Detailed visual prompt for comic style illustration"
  }}
]

Rules:
- Always return exactly 5 panels
- Output must be valid JSON
- Do not include explanations
"""

    try:

        response = model.generate_content(prompt)

        if not response or not response.text:
            raise ValueError("Empty response from Gemini")

        output = response.text.strip()

        # Remove markdown if Gemini returns code blocks
        output = output.replace("```json", "")
        output = output.replace("```", "")
        output = output.strip()

        outline = json.loads(output)

        # Basic validation
        if not isinstance(outline, list):
            raise ValueError("Gemini returned invalid format")

        if len(outline) < 5:
            raise ValueError("Gemini returned insufficient panels")

        return outline

    except Exception as e:

        print("Gemini Outline Error:", e)

        # Safe fallback outline
        return [
            {
                "panel": 1,
                "title": "Introduction",
                "scene_description": "The main character appears in the story setting.",
                "image_prompt": "comic style introduction scene"
            },
            {
                "panel": 2,
                "title": "Discovery",
                "scene_description": "The character discovers something surprising.",
                "image_prompt": "comic style discovery moment"
            },
            {
                "panel": 3,
                "title": "Conflict",
                "scene_description": "A challenge or obstacle appears.",
                "image_prompt": "comic style dramatic conflict"
            },
            {
                "panel": 4,
                "title": "Climax",
                "scene_description": "The hero faces the biggest challenge.",
                "image_prompt": "comic style intense action scene"
            },
            {
                "panel": 5,
                "title": "Resolution",
                "scene_description": "The story ends with a satisfying conclusion.",
                "image_prompt": "comic style happy ending"
            }
        ]