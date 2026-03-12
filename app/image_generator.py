import os
import uuid
import requests
from PIL import Image, ImageDraw
from urllib.parse import quote

# Reuse connection for faster requests
session = requests.Session()


def generate_image(prompt, style="Comic"):

    os.makedirs("static/panels", exist_ok=True)

    filename = f"panel_{uuid.uuid4().hex[:8]}.png"
    path = f"static/panels/{filename}"

    # -----------------------------
    # STYLE PROMPTS
    # -----------------------------

    style_map = {

        "Anime": "anime style illustration, japanese anime art, perfect symmetrical face, detailed anime eyes, clean anime lineart",

        "Manga": "manga panel illustration, black and white manga drawing, strong ink lines",

        "Comic": "western comic book illustration, bold outlines, graphic novel art",

        "Webtoon": "korean webtoon style illustration, colorful digital comic art",

        "Cartoon": "cartoon illustration style, bright colors",

        "Realistic": "cinematic realistic illustration, dramatic lighting"
    }

    style_prompt = style_map.get(style, "comic book illustration")

    # -----------------------------
    # BETTER PROMPT STRUCTURE
    # -----------------------------

    full_prompt = f"""
{style_prompt},
scene: {prompt},
professional comic panel,
perfect face anatomy,
symmetrical eyes,
high detail illustration,
cinematic lighting,
artstation quality,
4k illustration
"""

    encoded_prompt = quote(full_prompt)

    try:

        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=1024&seed={uuid.uuid4().hex[:6]}"

        response = session.get(url, timeout=60)

        if response.status_code == 200 and "image" in response.headers.get("content-type", ""):

            with open(path, "wb") as f:
                f.write(response.content)

            return path

    except Exception as e:
        print("AI image failed:", e)

    # -----------------------------
    # BACKUP IMAGE (REAL PHOTO)
    # -----------------------------

    try:

        backup = session.get("https://picsum.photos/768/1024", timeout=20)

        if backup.status_code == 200:

            with open(path, "wb") as f:
                f.write(backup.content)

            return path

    except Exception as e:
        print("Backup image failed:", e)

    # -----------------------------
    # FINAL FALLBACK PANEL
    # -----------------------------

    img = Image.new("RGB", (768,1024), (230,230,230))

    draw = ImageDraw.Draw(img)

    draw.rectangle([(5,5),(760,1016)], outline="black", width=8)

    draw.text((300,500),"Comic Panel", fill="black")

    img.save(path)

    return path