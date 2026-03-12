def build_comic_layout(image_paths, story, outline):

    layout = []

    for i, panel in enumerate(outline):

        dialogue = ""

        # story list format lo undi
        if isinstance(story, list) and i < len(story):

            item = story[i]

            dialogue = item.get("dialogue", "")

        layout.append({
            "panel": panel.get("panel", i+1),
            "title": panel.get("title", ""),
            "image_path": image_paths[i] if i < len(image_paths) else "",
            "scene_description": panel.get("scene_description", ""),
            "text": dialogue
        })

    return layout