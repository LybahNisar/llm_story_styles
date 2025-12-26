import os
import textwrap
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# ---------------- Config ----------------
DEFAULT_MAX_TOKENS = 300      # Output length fixed in code
DEFAULT_TEMPERATURE = 0.7     # Creativity level fixed

# ---------------- Load API Key ----------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in .env")
    exit()

client = OpenAI(api_key=api_key)

# ---------------- User Input ----------------
story = input("Enter your short story (max 300 chars): ").strip()
if not story:
    print("Story cannot be empty.")
    exit()
if len(story) > 300:
    print("Story is too long. Please keep it under 300 characters.")
    exit()

styles_input = input(
    "\nEnter style(s) you want (comma-separated, e.g. formal, humorous, poetic): "
).strip()
if not styles_input:
    print("Style cannot be empty.")
    exit()

styles = [s.strip() for s in styles_input.split(",")]

# ---------------- Prompt Template ----------------
def build_prompt(story, style):
    return f"""
You are a professional and creative storyteller.

Instructions:
- Rewrite the following story in a {style} style.
- Follow the {style} tone strictly and make it immediately recognizable.
- Keep the original meaning intact.
- Keep all original names as they are in the story.

Examples:
Formal: "The sun set over the horizon, casting a golden glow."
Humorous: "The cat walked in like it owned the house."
Suspenseful: "A shadow moved, and her breath stopped."

Story:
{story}
"""

# ---------------- LLM Call ----------------
generated_stories = []

for style in styles:
    prompt = build_prompt(story, style)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional storyteller."},
            {"role": "user", "content": prompt}
        ],
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS
    )

    output = response.choices[0].message.content.strip()
    generated_stories.append((style, output))

# ---------------- Output ----------------
wrapper = textwrap.TextWrapper(width=80)
print("\n=== GENERATED STORIES ===\n")

for style, text in generated_stories:
    print(f"--- {style.upper()} ---\n")
    for para in text.split("\n\n"):
        print(wrapper.fill(para))
        print()

# ---------------- Save to Files ----------------
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("generated_story.txt", "w", encoding="utf-8") as f:
    f.write(f"=== GENERATED STORIES ({timestamp}) ===\n\n")
    for style, text in generated_stories:
        f.write(f"--- {style.upper()} ---\n{text}\n\n")

with open("stories_output.txt", "a", encoding="utf-8") as f:
    f.write(f"[{timestamp}]\nStory: {story}\nStyles: {', '.join(styles)}\n\n")
    for style, text in generated_stories:
        f.write(f"{style.upper()}:\n{text}\n\n")
    f.write("-" * 50 + "\n")

print("Stories saved successfully.")
