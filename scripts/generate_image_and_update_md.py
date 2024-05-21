from openai import OpenAI
import os
import glob
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_image(prompt):
    response = client.image.generate(
        prompt=prompt, n=1, size="1024x1024", model="dall-e-3", quality="standard"
    )
    return response.data[0].url


def update_markdown(file_path, image_url):
    with open(file_path, "r") as file:
        content = file.read()

    content = f"![Episode Image]({image_url})\n\n" + content

    with open(file_path, "w") as file:
        file.write(content)


episode_files = glob.glob("episodes/*.md")
latest_file = max(episode_files, key=os.path.getmtime)
with open(latest_file, "r") as file:
    content = file.read()
    title_match = re.search(r"^#\s*(.+)", content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
        image_url = generate_image(title)
        update_markdown(latest_file, image_url)
