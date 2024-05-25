from openai import OpenAI
import os
import sys
import requests

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_image(prompt):
    response = client.images.generate(
        prompt="Here are the requirements for the image:\n"
        + "---\n"
        + "Fantasy theme\n"
        + "Glamourous\n"
        + "No creepy image\n"
        + "No NSFW content\n"
        + "No text on the image\n"
        + "---\n"
        + "Here's the text description:\n"
        + "---\n"
        + prompt
        + "---\n"
        + "Create an image based on the requirements and the description above.",
        n=1,
        size="1024x1024",
        model="dall-e-3",
        quality="standard",
    )
    return response.data[0].url


def download_image(image_url, save_path):
    response = requests.get(image_url)
    with open(save_path, "wb") as file:
        file.write(response.content)


def update_markdown(file_path, image_path):
    with open(file_path, "r") as file:
        content = file.read()

    content = f"![Episode Image]({image_path})\n\n" + content

    with open(file_path, "w") as file:
        file.write(content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_image_and_update_md.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, "r") as file:
        content = file.read()
        image_url = generate_image(content)

        image_name = os.path.basename(file_path).replace(".md", ".png")
        image_path = os.path.join("images", image_name)

        download_image(image_url, image_path)
        update_markdown(file_path, image_path)
