import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_story(outline):

    try:

        formatted_outline = "\n".join(
            [f"{p['panel']}. {p['title']} - {p['scene_description']}" for p in outline]
        )

        prompt = f"""
You are a comic script writer.

Convert the outline into comic dialogue.

Panel Outline:
{formatted_outline}

Rules:
- Write SHORT dialogue for speech bubbles
- Maximum 1 or 2 sentences
- Focus on character speech
- Avoid long narration

Format strictly as JSON:

[
{{
"panel":1,
"dialogue":"dialogue text here"
}},
{{
"panel":2,
"dialogue":"dialogue text here"
}}
]
"""

        response = model.generate_content(prompt)

        text = response.text.strip()

        text = text.replace("```json","").replace("```","")

        import json

        story = json.loads(text)

        return story

    except Exception as e:

        print("Story generation error:", e)

        # fallback
        return [
            {"panel":1,"dialogue":"What is happening here?"},
            {"panel":2,"dialogue":"Something strange is going on."},
            {"panel":3,"dialogue":"We must investigate."},
            {"panel":4,"dialogue":"This is the big moment!"},
            {"panel":5,"dialogue":"We did it!"}
        ]