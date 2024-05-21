from openai import OpenAI
import os
import glob

# Ensure the OpenAI API key is set in your environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def translate_text(text, target_language="en"):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"Translate the following text to {target_language}:",
            },
            {"role": "user", "content": text},
        ],
        max_tokens=1000,
    )
    return response.choices[0].message["content"].strip()


def translate_markdown(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    translated_content = translate_text(content)

    translated_file_path = file_path.replace(".md", "_en.md")
    with open(translated_file_path, "w") as file:
        file.write(translated_content)


pr_files = glob.glob("episodes/*.md")
for file_path in pr_files:
    translate_markdown(file_path)
